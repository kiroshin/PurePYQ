#  apply_region.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from serving import ApplyRegionUsecase
from appstate import Roger
from vessel import Vessel


def apply_region_action(self: Vessel) -> ApplyRegionUsecase:
    async def _action(is_show: bool):
        await self.update(_update, is_show)
    return _action


def _update(value: Roger, is_show: bool) -> Roger:
    field = value.field._replace(is_region=is_show)
    return value._replace(field=field)
