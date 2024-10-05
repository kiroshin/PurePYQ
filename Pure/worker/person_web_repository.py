#  person_web_repository.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import aiohttp
from gear import HttpAioRandomuserAccess, WEB
from model import Fizzle, WebFizzle
from working import PersonWebWork
from worker import DBStore, DB


class PersonWebRepository(PersonWebWork):
    def __init__(self, access: HttpAioRandomuserAccess, database: DBStore):
        super().__init__()
        self.access = access
        self.database = database

    # OVERRIDE
    async def get_person_all(self):
        try:
            users = await self.access.get_all_user()
            humans = list(map(_human_from_user, users))
            self.database.create_human(humans)
        except aiohttp.ClientConnectorError:
            raise WebFizzle.connection_error()
        except aiohttp.ClientError:
            raise Fizzle()

    # OVERRIDE
    async def walk(self, is_wing: bool) -> str:
        return "LEG" if is_wing else "GEL"


def _human_from_user(user: WEB.User) -> DB.Human:
    return DB.Human(
        uid=user.login.uuid,
        name=f"{user.name.first} {user.name.last}",
        username=user.login.username,
        gender=user.gender,
        email=user.email,
        age=user.dob.age,
        country=user.nat,
        cellphone=user.cell,
        photo=user.picture.large
    )
