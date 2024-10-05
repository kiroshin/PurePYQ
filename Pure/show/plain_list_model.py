#  plain_list_model.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import NamedTuple, TypeVar, Generic
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize, QAbstractListModel

T = TypeVar("T")


class PlainListItem(NamedTuple):
    text: str       # Qt.ItemDataRole.DisplayRole


class PlainListModel(Generic[T], QAbstractListModel):
    _sheet_data: list
    size_hint: QSize = None
    font: QFont = None

    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._sheet_data = data if data else []

    @property
    def sheet_data(self):
        return self._sheet_data

    # OVERRIDE
    def rowCount(self, parent=...):
        return len(self._sheet_data)

    # OVERRIDE
    def data(self, index, role=...):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return self._sheet_data[index.row()].text
        if role == Qt.ItemDataRole.SizeHintRole and self.size_hint:
            return self.size_hint
        if role == Qt.ItemDataRole.FontRole and self.font:
            return self.font
        if role == Qt.ItemDataRole.UserRole:
            return self._sheet_data[index.row()]

    def reset_sheet(self, data: list[T]):
        self.beginResetModel()
        self._sheet_data = data
        self.endResetModel()
