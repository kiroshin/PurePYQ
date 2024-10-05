#  person_local_repository.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import logging
import sqlite3
import aiohttp
import random
from model import PersonID, Person, Fizzle, DBFizzle, WebFizzle
from gear import HttpAioRandomuserAccess
from working import PersonLocalWork
from worker import DBStore, DB, FileStore


class PersonLocalRepository(PersonLocalWork):
    def __init__(self, database: DBStore, cache: FileStore, access: HttpAioRandomuserAccess):
        super().__init__()
        self.database = database
        self.cache = cache
        self.access = access

    # OVERRIDE
    async def clear_database(self):
        try:
            self.database.clear_human()
        except sqlite3.OperationalError as e:
            logging.error(e)
            raise DBFizzle.operation_error()
        except Exception as e:
            logging.critical(e)
            raise Fizzle()

    # OVERRIDE
    async def clear_cache(self):
        try:
            self.cache.clear_cache_file()
        except Exception:
            raise Fizzle()

    # OVERRIDE
    async def count(self) -> int:
        return self.database.count_human()

    # OVERRIDE
    async def get_person_meta_all(self) -> list[Person.Meta]:
        try:
            human_metas = self.database.read_human_meta_all(100)
            return list(map(_person_meta_from_human_meta, human_metas))
        except sqlite3.OperationalError as e:
            logging.error(e)
            raise DBFizzle.operation_error()
        except Exception as e:
            logging.critical(e)
            raise Fizzle()

    # OVERRIDE
    async def get_person(self, uid: PersonID) -> Person:
        try:
            human = self.database.read_human(uid)
            person = _person_from_human(human)
            photo_name = self.cache.get_cache_path(person.photo)
            if not photo_name:
                photo_raw = await self.access.get_picture(human.photo)
                photo_name = self.cache.set_cache_file(human.photo, photo_raw)
            person.photo = photo_name
            return person
        except sqlite3.OperationalError as e:
            logging.error(e)
            raise DBFizzle.operation_error()
        except aiohttp.ClientError as e:
            logging.error(e)
            raise WebFizzle.connection_error()
        except Exception as e:
            logging.critical(e)
            raise Fizzle()

    # OVERRIDE
    async def fly(self, is_wing: bool) -> str:
        num = random.randint(0, 100)
        return f"WING{num}" if is_wing else f"FIZZ{num}"


def _person_from_human(hum: DB.Human) -> Person:
    return Person(
        uid=hum.uid,
        name=hum.name,
        username=hum.username,
        gender=hum.gender,
        email=hum.email,
        age=hum.age,
        region=hum.country,
        cellphone=hum.cellphone,
        photo=hum.photo
    )


def _person_meta_from_human_meta(hum: DB.Human.Meta) -> Person.Meta:
    return Person.Meta(
        uid=hum.uid,
        name=hum.name,
        region=hum.country
    )
