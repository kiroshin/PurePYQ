#  vessel.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import os
import weakref
from typing import Callable, Awaitable
from asset import Asset
from appstate import *
from serving import *
from working import *
from util import *
from gear import *
from worker import *


class Vessel(MutableStore[Roger], Serving):
    _app_data_path: str
    _app_cache_path: str
    _message_handler: weakref.WeakMethod
    person_web_work: PersonWebWork
    person_local_work: PersonLocalWork

    def __init__(self, data_path: str, cache_path: str, db_filename: str):
        super().__init__(initial=Roger.initial())
        db_path = os.path.join(data_path, db_filename)
        self.create_workers(db_path, cache_path)

    def create_workers(self, db_path, app_cache_path):
        access = HttpAioRandomuserAccess()
        database = DBStore(db_path, Asset.Script.schema)
        cache = FileStore(app_cache_path)
        self.person_web_work = PersonWebRepository(access, database)
        self.person_local_work = PersonLocalRepository(database, cache, access)

    def set_message_handler(self, fn: Callable[[str], Awaitable]):
        self._message_handler = weakref.WeakMethod(fn)

    # 런루프가 시작할 때 처리할 작업
    async def __bootup__(self):
        HttpAioClient.__bootup__()
        await self.build_app_data_action(True)

    # 런루프 종료할 때 처리할 작업
    async def __shutdown__(self):
        await HttpAioClient.__shutdown__()

    # 메시지 핸들러에 전달한다.
    async def notice(self, msg: str):
        if func := self._message_handler():
            await func(msg)

    # OVERRIDE
    @property
    def appstate(self) -> AppState:
        return self

    # OVERRIDE
    @property
    def apply_region_action(self) -> ApplyRegionUsecase:
        from usecase.apply_region import apply_region_action
        return apply_region_action(self)

    # OVERRIDE
    @property
    def apply_route_action(self) -> ApplyRouteUsecase:
        from usecase.apply_route import apply_route_action
        return apply_route_action(self)

    # OVERRIDE
    @property
    def build_app_data_action(self) -> BuildAppDataUsecase:
        from usecase.build_app_data import build_app_data_action
        return build_app_data_action(self)

    # OVERRIDE
    @property
    def clear_app_cache_action(self) -> CleanAppCacheUsecase:
        from usecase.clear_app_cache import clear_app_cache_action
        return clear_app_cache_action(self)

    # OVERRIDE
    @property
    def load_person_action(self) -> LoadPersonUsecase:
        from usecase.load_person import load_person_action
        return load_person_action(self)

    # OVERRIDE
    @property
    def move_here_action(self) -> MoveHereUsecase:
        from usecase.move_here import move_here_action
        return move_here_action(self)

