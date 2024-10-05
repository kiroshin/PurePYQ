#  home_viewmodel.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import NamedTuple
from PySide6.QtCore import Qt, QObject, QModelIndex
from serving import *
from model import Person
from util import async_slot
from show import PlainListModel, ItemDataUserRole


class HomeViewModel(QObject):
    datasource: 'HomeListModel'

    def __init__(self, service: Serving, parent=None):
        super().__init__(parent)
        self.datasource = HomeListModel()
        # 액션
        self._apply_region_action = service.apply_region_action
        self._apply_route_action = service.apply_route_action
        # 바인딩
        self._ticket = service.appstate.stored(lambda s: s.query.metas)\
            .filter(bool)\
            .methodscribe(self._on_person_meta_changed)

    @async_slot
    async def select_person(self, index: QModelIndex):
        data: HomeListItem = index.data(Qt.ItemDataRole.UserRole)
        await self._apply_route_action(data.uid)

    @async_slot
    async def show_region(self, state: Qt.CheckState):
        self.datasource.set_is_show_region(bool(state))
        await self._apply_region_action(bool(state))

    async def _on_person_meta_changed(self, metas: list[Person.Meta]):
        self.datasource.reset_sheet(list(map(self._sheet_from_meta, metas)))

    @staticmethod
    def _sheet_from_meta(data: Person.Meta):
        return HomeListItem(
            uid=data.uid,
            text=data.name,
            region=data.region
        )


class HomeListItem(NamedTuple):
    uid: str
    text: str  # Qt.ItemDataRole.DisplayRole
    region: str


class HomeListModel(PlainListModel[HomeListItem]):
    _is_region: bool = False

    # OVERRIDE
    def data(self, index, role=...):
        if self._is_region and role == ItemDataUserRole.Tag:
            return self.sheet_data[index.row()].region
        return super().data(index, role)

    def set_is_show_region(self, is_show: bool):
        self.beginResetModel()
        self._is_region = is_show
        self.endResetModel()

