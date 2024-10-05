#  plain_table_model.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from typing import NamedTuple, TypeVar, Generic
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize, QModelIndex, QAbstractTableModel

__all__ = ['PlainTableModel', 'PlainTableItem']
T = TypeVar("T")


class PlainTableItem(NamedTuple):
    text: tuple  # Qt.ItemDataRole.DisplayRole


class PlainTableModel(Generic[T], QAbstractTableModel):
    _sheet_column: list
    _sheet_data: list
    size_hint: QSize = None
    font: QFont = None

    def __init__(self, column=None, data=None, parent=None):
        super().__init__(parent)
        self._sheet_column = column if column is not None else []
        self._sheet_data = data if data is not None else []

    @property
    def sheet_data(self):
        return self._sheet_data

    # OVERRIDE
    def columnCount(self, parent=...):
        return len(self._sheet_column)

    # OVERRIDE
    def rowCount(self, parent=...):
        return len(self._sheet_data)

    # OVERRIDE
    def data(self, index, role=...):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._sheet_data[index.row()].text[index.column()])
        if role == Qt.ItemDataRole.SizeHintRole and self.size_hint:
            return self.size_hint
        if role == Qt.ItemDataRole.FontRole and self.font:
            return self.font
        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 0:
            return Qt.AlignmentFlag.AlignCenter
        if role == Qt.ItemDataRole.UserRole:
            return self._sheet_data[index.row()]

    # OVERRIDE
    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._sheet_column[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(section)
        return None

    def reset_sheet(self, data: list[T]):
        self.beginResetModel()
        self._sheet_data = data
        self.endResetModel()

    def pop_index(self, idx: int) -> T:
        self.beginRemoveRows(QModelIndex(), idx, idx)
        obj = self._sheet_data.pop(idx)
        self.endRemoveRows()
        return obj

    def insert_index(self, idx: int, item: T):
        self.beginInsertRows(QModelIndex(), idx, idx)
        self._sheet_data.insert(idx, item)
        self.endInsertRows()
