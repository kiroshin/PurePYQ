#  store.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import asyncio
import weakref
from inspect import iscoroutinefunction
from abc import abstractmethod
from typing import TypeVar, NamedTuple, Callable
from util.publisher import *

__all__ = ["Stored", "Store", "MutableStore"]

S = TypeVar("S", bound=NamedTuple)
Stored = PubPipe


# 스토어: 추상클래스. NamedTuple 을 취급한다.
# ------------------------------------------------------------
class Store(Pub[S]):
    @property
    @abstractmethod
    async def value(self): pass

    def stored(self, func: Callable[[S], object]) -> Stored:
        return self.map(func).distinct()


# 뮤터블 스토어: 밸류퍼프와 거의 비슷하다.
# - 이니셜이 반드시 있어야 하며, asyncio 와 NamedTuple 을 취급한다.
# - update 를 사용할 경우 람다 내부에 현재 Value 를 주며, 완성 객체를 반환해야 한다.
# - set 을 사용할 경우 키-값을 줘야 하며, 자료구조와 부합해야 한다.
# ------------------------------------------------------------

class MutableStore(Store[S]):
    _lock: asyncio.Lock
    _value: S
    _listeners: list

    def __init__(self, initial: S):
        self._lock = asyncio.Lock()
        self._listeners = list()
        self._value = initial

    async def update(self, func: Callable[..., S], *args, **kwargs):
        """func 는 첫 인자로 value 를 받으며, 같은 타입으로 반환해야 한다"""
        await self._lock.acquire()
        value = func(self._value, *args, **kwargs)
        if value is None or self._value == value:
            self._lock.release()
            return
        self._value = value
        listeners = list(filter(lambda x: x(), self._listeners))
        self._listeners = listeners
        self._lock.release()
        futures = [ltnr()(value) for ltnr in listeners]
        await asyncio.gather(*futures)

    async def set(self, value: dict):
        """키가 맞지 않으면 터진다. 그래서 내부 함수로만 이용한다."""
        await self._lock.acquire()
        value = self._value._replace(**value)
        if self._value == value:
            self._lock.release()
            return
        self._value = value
        listeners = list(filter(lambda x: x(), self._listeners))
        self._listeners = listeners
        self._lock.release()
        futures = [ltnr()(value) for ltnr in listeners]
        await asyncio.gather(*futures)

    async def _listen(self, ticket: Ticket):
        ticket.set_pub(self)
        weak_stream = weakref.ref(ticket.stream)
        async with self._lock:
            self._listeners.append(weak_stream)
            current_value = self._value
        if current_value:
            await ticket.stream(current_value)

    async def _unlisten(self, stream):
        async with self._lock:
            self._listeners.remove(stream)

    # OVERRIDE
    def subscribe(self, fn: PubStream):
        assert iscoroutinefunction(fn), "** ASSERT: NOT ASYNC METHOD"
        ticket = Ticket(fn)
        asyncio.create_task(self._listen(ticket))
        return ticket

    # OVERRIDE
    def unsubscribe(self, stream):
        weak_stream = weakref.ref(stream)
        asyncio.create_task(self._unlisten(weak_stream))

    # OVERRIDE
    @property
    async def value(self):
        async with self._lock:
            return self._value

