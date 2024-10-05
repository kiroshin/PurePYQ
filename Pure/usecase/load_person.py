#  load_person.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from serving import LoadPersonUsecase
from model import PersonID, Fizzle
from vessel import Vessel


def load_person_action(self: Vessel) -> LoadPersonUsecase:
    async def _action(uid: PersonID):
        try:
            return await self.person_local_work.get_person(uid)
        except Fizzle as e:
            await self.notice(e.msg())
    return _action
