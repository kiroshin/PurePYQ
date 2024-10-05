#  appstate.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import NamedTuple
from enum import IntEnum
from util import Store
from model import PersonID, Person

__all__ = ["AppState", "Roger"]
AppState = Store['Roger']


class Roger(NamedTuple):
    sys: 'Roger.Sys'
    route: 'Roger.Route'
    query: 'Roger.Query'
    field: 'Roger.Field'

    class Sys(NamedTuple):
        last: 'Roger.Sign'

    class Route(NamedTuple):
        uid: PersonID

    class Query(NamedTuple):
        metas: list[Person.Meta]

    class Field(NamedTuple):
        is_username: bool
        is_region: bool

    class Sign(IntEnum):
        FAILURE = -1
        READY = 0
        SUCCESS = 1

    @staticmethod
    def initial() -> 'Roger':
        sys = Roger.Sys(Roger.Sign.READY)
        route = Roger.Route("")
        query = Roger.Query([])
        field = Roger.Field(True, False)
        return Roger(sys=sys, route=route, query=query, field=field)

