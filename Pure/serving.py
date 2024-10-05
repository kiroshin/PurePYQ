#  serving.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from abc import ABCMeta, abstractmethod
from typing import Callable, Awaitable
from appstate import AppState
from model import PersonID, Person

__all__ = [
    "Serving",
    "ApplyRegionUsecase",
    "ApplyRouteUsecase",
    "BuildAppDataUsecase",
    "CleanAppCacheUsecase",
    "LoadPersonUsecase",
    "MoveHereUsecase"
]


class Serving(metaclass=ABCMeta):
    @property
    @abstractmethod
    def appstate(self) -> AppState: pass

    @property
    @abstractmethod
    def build_app_data_action(self) -> 'BuildAppDataUsecase': pass

    @property
    @abstractmethod
    def clear_app_cache_action(self) -> 'CleanAppCacheUsecase': pass

    @property
    @abstractmethod
    def load_person_action(self) -> 'LoadPersonUsecase': pass

    @property
    @abstractmethod
    def apply_region_action(self) -> 'ApplyRegionUsecase': pass

    @property
    @abstractmethod
    def apply_route_action(self) -> 'ApplyRouteUsecase': pass

    @property
    @abstractmethod
    def move_here_action(self) -> 'MoveHereUsecase': pass


IsInit = bool
IsShow = bool
IsLeg, IsWing = bool, bool

BuildAppDataUsecase = Callable[[IsInit], Awaitable]
CleanAppCacheUsecase = Callable[[], Awaitable]
LoadPersonUsecase = Callable[[PersonID], Awaitable[Person]]
ApplyRegionUsecase = Callable[[IsShow], Awaitable]
ApplyRouteUsecase = Callable[[PersonID], Awaitable]
MoveHereUsecase = Callable[[IsLeg, IsWing], Awaitable[str]]

