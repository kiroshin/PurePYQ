#  move_here.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from serving import MoveHereUsecase
from vessel import Vessel


def move_here_action(self: Vessel) -> MoveHereUsecase:
    async def _action(is_leg: bool, is_wing_bool: bool):
        txtweb = await self.person_web_work.walk(is_leg)
        txtdb = await self.person_local_work.fly(is_wing_bool)
        return txtweb + txtdb
    return _action

