#  apply_route.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from serving import ApplyRouteUsecase
from model import PersonID
from appstate import Roger
from vessel import Vessel


def apply_route_action(self: Vessel) -> ApplyRouteUsecase:
    async def _action(uid: PersonID):
        await self.update(_update, uid)
    return _action


def _update(value: Roger, uid: str) -> Roger:
    route = value.route._replace(uid=uid)
    return value._replace(route=route)
