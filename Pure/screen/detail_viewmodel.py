#  detail_viewmodel.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import random
from typing import NamedTuple
from PySide6.QtCore import QObject, Signal
from serving import *
from util import async_slot
from model import PersonID, Person
from show import PlainTableModel


class DetailViewModel(QObject):
    test_text = Signal(str)
    photo = Signal(str)
    datasource: 'DetailTableModel'
    _current: Person | None = None
    _load_person_action: LoadPersonUsecase
    _move_here_action: MoveHereUsecase

    def __init__(self, service: Serving, parent=None):
        super().__init__(parent)
        self.datasource = DetailTableModel(
            ["TITLE", "DESCRIPTION"],
            []
        )
        self._bag = list()
        # 액션
        self._load_person_action = service.load_person_action
        self._move_here_action = service.move_here_action
        # 바인딩
        service.appstate.stored(lambda x: x.field.is_region) \
            .methodscribe(self._on_region_changed) \
            .deposit(self._bag)
        service.appstate.stored(lambda x: x.route.uid)\
            .filter(bool)\
            .methodscribe(self._on_route_changed)\
            .deposit(self._bag)

    async def _on_region_changed(self, is_show: bool):
        self.datasource.set_is_region(is_show)

    async def _on_route_changed(self, route: PersonID):
        if person := await self._load_person_action(route):
            sheet = [
                DetailListItem("name", ("Name", person.name)),
                DetailListItem("nick", ("Nick", person.username)),
                DetailListItem("email", ("Email", person.email)),
                DetailListItem("age", ("Age", str(person.age))),
                DetailListItem("region", ("Region", str(person.region))),
                DetailListItem("phone", ("Phone", person.cellphone))
            ]
            self.photo.emit(person.photo)
            self.datasource.reset_sheet(sheet)

    @async_slot
    async def move_here(self):
        text = await self._move_here_action(random.choice([True, False]), random.choice([True, False]))
        self.test_text.emit(text)


class DetailListItem(NamedTuple):
    uid: str
    text: tuple     # Qt.ItemDataRole.DisplayRole


class DetailTableModel(PlainTableModel[DetailListItem]):
    _REGION_IDX = 4
    _region_item = None
    _is_region: bool = False

    # OVERRIDE
    def reset_sheet(self, data: list[DetailListItem]):
        if not self._is_region:
            self._region_item = data.pop(self._REGION_IDX)
        super().reset_sheet(data)

    def set_is_region(self, is_show: bool):
        if is_show == self._is_region or self.rowCount() < self._REGION_IDX:
            self._is_region = is_show
            return
        self._is_region = is_show
        if is_show:
            self.insert_index(self._REGION_IDX, self._region_item)
            self._region_item = None
        else:
            self._region_item = self.pop_index(self._REGION_IDX)
