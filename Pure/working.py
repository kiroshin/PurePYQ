#  working.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from abc import ABCMeta, abstractmethod
from model.person import Person, PersonID

__all__ = ["PersonWebWork", "PersonLocalWork"]


class PersonWebWork(metaclass=ABCMeta):
    @abstractmethod
    async def get_person_all(self): pass

    @abstractmethod
    async def walk(self, is_wing: bool) -> str: pass


class PersonLocalWork(metaclass=ABCMeta):
    @abstractmethod
    async def clear_database(self): pass

    @abstractmethod
    async def clear_cache(self): pass

    @abstractmethod
    async def count(self) -> int: pass

    @abstractmethod
    async def get_person_meta_all(self) -> list[Person.Meta]: pass

    @abstractmethod
    async def get_person(self, idnt: PersonID) -> Person: pass

    @abstractmethod
    async def fly(self, is_wing: bool) -> str: pass

