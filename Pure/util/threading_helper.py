#  threading_helper.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import threading as th
from typing import final
from functools import wraps
from PySide6.QtCore import QObject, Signal

__all__ = ["MainDispatch", "dispatch_main_return", "dispatch_global_return"]


# 싱글톤: QT 이벤트 루프 디스패치
# ------------------------------------------------------------
@final
class MainDispatch(QObject):
    _instance: 'MainDispatch'
    _init: bool
    _dispatch = Signal(object)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            super().__init__()
            self._dispatch.connect(lambda fn: fn())
            cls._init = True

    def set(self, fn=None):
        if fn:
            self._dispatch.emit(fn)
            # QT 런루프로 밀어넣는다.


# 데코레이터: 쓰레드 디스패치
# ------------------------------------------------------------
def dispatch_main_return(func):
    """메인쓰레드 디스패치: 함수는 현재 쓰레드에서 실행되며, 리턴하는 함수가 메인에서 실행됨"""
    @wraps(func)
    def decorator(*args):
        return MainDispatch().set(func(*args))
    return decorator


def dispatch_global_return(func):
    """데몬 백쓰레드 디스패치: 함수 자체가 백쓰레드에서 실행되며, 리턴값 없음"""
    @wraps(func)
    def decorator(*args):
        return th.Thread(target=func, args=(*args,), daemon=True).start()
    return decorator
