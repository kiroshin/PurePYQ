#  publisher.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2023.

import threading
import weakref
from inspect import iscoroutinefunction
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Callable, Generic, Awaitable

__all__ = ["PubStream", "Ticket", "Pub", "ValuePub", "PubPipe"]

T = TypeVar("T")
K = TypeVar("K")
N = TypeVar("N")
PubStream = Callable[[T], Awaitable | None]
PubPrototype = Callable[[PubStream], PubStream]


def _empty_stream(_):
    return None


# 티켓: 구독 시 최종 반환된다. 리소스를 가지고 있다.
# - bag 에 담긴 ticket 을 버릴 때는 백에서 pop 한 뒤 cancel 을 해준다.
# ------------------------------------------------------------
class Ticket(Generic[T]):
    pubs: list['Pub'] | None
    stream: PubStream

    def __init__(self, stream: PubStream):
        self.pubs = list()
        self.stream = stream

    def set_pub(self, pub: 'Pub'):
        if self.pubs is not None and pub not in self.pubs:
            self.pubs.append(pub)

    def cancel(self):
        for pub in self.pubs:
            pub.unsubscribe(self.stream)
        self.pubs = None
        self.stream = _empty_stream

    def deposit(self, bag: list | set):
        if isinstance(bag, list):
            bag.append(self)
        else:
            bag.add(self)


# 퍼브: 추상클래스
# ------------------------------------------------------------
class Pub(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, stream: PubStream) -> Ticket[T]: pass

    @abstractmethod
    def unsubscribe(self, stream: PubStream): pass

    def methodscribe(self, method) -> Ticket[T]:
        weakmethod = weakref.WeakMethod(method)
        if iscoroutinefunction(method):
            async def _stream(value):
                await weakmethod()(value)
            return self.subscribe(_stream)
        return self.subscribe(lambda v: weakmethod()(v))

    def map(self, fn: Callable[[K], N]) -> 'PubPipe':
        return PubMapPipe(self, fn)

    def filter(self, fn: Callable[[K], bool]) -> 'PubPipe':
        return PubFilterPipe(self, fn)

    def reduce(self, initial: K, fn: Callable[[K, N], K]) -> 'PubPipe':
        return PubReducePipe(self, initial, fn)

    def distinct(self) -> 'PubPipe':
        return PubDistinctPipe(self)


# 밸류퍼브: 값을 가지고 있으며, 구독한 순간부터 값을 준다.
# ------------------------------------------------------------
class ValuePub(Pub[T]):
    _lock: threading.Lock
    _value: T
    _listeners: list  # weak PubStream

    def __init__(self, initial: T = None):
        self._lock = threading.Lock()
        self._listeners = list()
        self._value = initial

    def set(self, value: T):
        if value is None:
            return
        self._lock.acquire()
        self._value = value
        listeners = list(filter(lambda x: x(), self._listeners))
        self._listeners = listeners
        self._lock.release()
        for ltnr in listeners:
            ltnr()(value)   # if ltnr := ltnr(): # weak -> strong

    def _listen(self, ticket: Ticket):
        ticket.set_pub(self)
        weak_stream = weakref.ref(ticket.stream)
        self._lock.acquire()
        self._listeners.append(weak_stream)
        current_value = self._value
        self._lock.release()
        if current_value:
            ticket.stream(current_value)

    # OVERRIDE
    def subscribe(self, fn: PubStream):
        assert not iscoroutinefunction(fn), "** ASSERT: ASYNC METHOD"
        ticket = Ticket(fn)
        self._listen(ticket)
        return ticket

    # OVERRIDE
    def unsubscribe(self, stream):
        weak_stream = weakref.ref(stream)
        self._lock.acquire()
        self._listeners.remove(weak_stream)
        self._lock.release()

    @property
    def value(self) -> T | None:
        self._lock.acquire()
        current_value = self._value
        self._lock.release()
        return current_value


# 패쓰퍼브: 값을 가지고 있지 않으며, 구독 이후 값이 변경 준다.
# ------------------------------------------------------------
class PassPub(Pub[T]):
    _lock: threading.Lock
    _listeners: list  # weak PubStream

    def __init__(self):
        self._lock = threading.Lock()
        self._listeners = list()

    def set(self, value: T):
        if value is None:
            return
        self._lock.acquire()
        listeners = list(filter(lambda x: x(), self._listeners))
        self._listeners = listeners
        self._lock.release()
        for ltnr in listeners:
            ltnr()(value)   # if ltnr := ltnr(): # weak -> strong

    def _listen(self, ticket: Ticket):
        ticket.set_pub(self)
        weak_stream = weakref.ref(ticket.stream)
        self._lock.acquire()
        self._listeners.append(weak_stream)
        self._lock.release()

    # OVERRIDE
    def subscribe(self, fn: PubStream):
        assert not iscoroutinefunction(fn), "** ASSERT: ASYNC METHOD"
        ticket = Ticket(fn)
        self._listen(ticket)
        return ticket

    # OVERRIDE
    def unsubscribe(self, stream):
        weak_stream = weakref.ref(stream)
        self._lock.acquire()
        self._listeners.remove(weak_stream)
        self._lock.release()


# 파이프: 퍼브를 연결한다.
# ------------------------------------------------------------
class PubPipe(Pub):
    parant: Pub
    proto: PubPrototype = None

    @staticmethod
    def _stacked(uppipe: 'PubPipe', dnpipe: 'PubPipe'):
        upproto, dnproto = uppipe.proto, dnpipe.proto
        def proto(nextstream):
            return upproto(dnproto(nextstream))
        dnpipe.proto = proto
        return dnpipe

    def __init__(self, parant: Pub):
        super().__init__()
        self.parant = parant

    # OVERRIDE
    def subscribe(self, stream: PubStream) -> Ticket[T]:
        if self.proto:
            stream = self.proto(stream)
        return self.parant.subscribe(stream)

    # OVERRIDE
    def unsubscribe(self, stream: PubStream):
        self.parant.unsubscribe(stream)

    # OVERRIDE
    def map(self, fn: Callable[[K], N]) -> 'PubPipe':
        return PubPipe._stacked(self, PubMapPipe(self.parant, fn))

    # OVERRIDE
    def filter(self, fn: Callable[[K], bool]) -> 'PubPipe':
        return PubPipe._stacked(self, PubFilterPipe(self.parant, fn))

    # OVERRIDE
    def reduce(self, initial: K, fn: Callable[[K, N], K]) -> 'PubPipe':
        return PubPipe._stacked(self, PubReducePipe(self, initial, fn))

    # OVERRIDE
    def distinct(self) -> 'PubPipe':
        return PubPipe._stacked(self, PubDistinctPipe(self.parant))


# 파이프 오퍼레이터
# ------------------------------------------------------------
class PubMapPipe(PubPipe):
    def __init__(self, parant: Pub, fn):
        super().__init__(parant)
        def prototype(nextstream):
            if iscoroutinefunction(nextstream):
                async def _stream(v):
                    element = fn(v)
                    if element is not None:
                        await nextstream(element)
                return _stream
            def stream(v):
                element = fn(v)
                if element is not None:
                    nextstream(element)
            return stream
        self.proto = prototype


class PubFilterPipe(PubPipe):
    def __init__(self, parant: Pub, fn):
        super().__init__(parant)
        def prototype(nextstream):
            if iscoroutinefunction(nextstream):
                async def _stream(v):
                    if fn(v):
                        await nextstream(v)
                return _stream
            def stream(v):
                if fn(v):
                    nextstream(v)
            return stream
        self.proto = prototype


class PubReducePipe(PubPipe):
    def __init__(self, parant: Pub, initial, fn):
        super().__init__(parant)
        def prototype(nextstream):
            partial = initial
            if iscoroutinefunction(nextstream):
                async def _stream(v):
                    nonlocal partial
                    element = fn(partial, v)
                    if element is not None:
                        partial = element
                        await nextstream(partial)
                return _stream
            def stream(v):
                nonlocal partial
                element = fn(partial, v)
                if element is not None:
                    partial = fn(partial, v)
                    nextstream(partial)
            return stream
        self.proto = prototype


class PubDistinctPipe(PubPipe):
    def __init__(self, parant: Pub):
        super().__init__(parant)
        def prototype(nextstream):
            buffer = None
            if iscoroutinefunction(nextstream):
                async def _stream(v):
                    nonlocal buffer
                    if v is not None and buffer != v:
                        buffer = v
                        await nextstream(v)
                return _stream
            def stream(v):
                nonlocal buffer
                if v is not None and buffer != v:
                    buffer = v
                    nextstream(v)
            return stream
        self.proto = prototype
