#  asyncio_helper.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import asyncio
from functools import wraps

__all__ = ["async_task", "async_exec", "async_slot", "async_debounce", "async_throttle"]


# 편의함수
# 런루프가 돌지 않으면 create_task() 나 get_running_loop() 는 뻑난다.
# asyncio.get_event_loop() 로 확인 가능.
# ------------------------------------------------------------
def async_task(func):
    return asyncio.create_task(func)


def async_exec(func, *args):
    return asyncio.get_running_loop().run_in_executor(None, func, *args)


# 데코레이터: Async 함수를 일반 함수로 포장
# ------------------------------------------------------------
def async_slot(func):
    @wraps(func)
    def _decorator(*args, **kwargs):
        return asyncio.create_task(func(*args, **kwargs))
    return _decorator


# 데코레이터: 디바운스 -  첫 이벤트 후 액션을 wait 대기 후 마지막 액션을 실행한다.
# https://gist.github.com/medihack/7af1f98ea468aa7ad00102c7d84c65d8
# ------------------------------------------------------------
def async_debounce(wait):
    def decorator(func):
        task: asyncio.Task | None = None
        @wraps(func)
        async def debounced(*args, **kwargs):
            nonlocal task
            if task and not task.done():
                task.cancel()
            async def call_func():
                await asyncio.sleep(wait)
                await func(*args, **kwargs)
            task = asyncio.create_task(call_func())
            return task
        return debounced
    return decorator


# 데코레이터: 쓰로틀 - 첫 이벤트 후 액션을 바로 실행 wait 내 이벤트 무시.
# ------------------------------------------------------------
def async_throttle(wait):
    def decorator(func):
        task: asyncio.Task | None = None
        @wraps(func)
        async def throttle(*args, **kwargs):
            nonlocal task
            if task and not task.done():
                return
            async def call_func():
                await func(*args, **kwargs)
                await asyncio.sleep(wait)
            task = asyncio.create_task(call_func())
            return task
        return throttle
    return decorator
