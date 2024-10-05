#  build_app_data.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import asyncio
from serving import BuildAppDataUsecase
from appstate import Roger
from model import Fizzle
from vessel import Vessel


def build_app_data_action(self: Vessel) -> BuildAppDataUsecase:
    async def _action(is_init: bool):
        try:
            if not is_init:
                await self.person_local_work.clear_database()
            if not await self.person_local_work.count():
                await asyncio.gather(
                    self.notice("Downloading..."),
                    self.person_web_work.get_person_all()
                )
            metas = await self.person_local_work.get_person_meta_all()
        except Fizzle as e:
            await self.notice(e.msg())
        else:
            await self.update(_update, metas)

    return _action


def _update(value: Roger, metas):
    query = value.query._replace(metas=metas)
    return value._replace(query=query)


