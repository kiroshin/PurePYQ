#  clear_app_cache.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import asyncio
from serving import CleanAppCacheUsecase
from vessel import Vessel


def clear_app_cache_action(self: Vessel) -> CleanAppCacheUsecase:
    async def _action():
        await asyncio.gather(
            self.notice("Clearing..."),
            self.person_local_work.clear_cache()
        )
    return _action

