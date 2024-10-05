#  person.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from dataclasses import dataclass
from typing import NamedTuple

PersonID = str


@dataclass(slots=True, eq=False)
class Person:
    uid: PersonID
    name: str
    username: str
    gender: str
    email: str
    age: int
    region: str
    cellphone: str | None
    photo: str | None

    def __eq__(self, other: 'Person'):
        return self.uid == other.uid

    class Meta(NamedTuple):
        uid: PersonID
        name: str
        region: str

