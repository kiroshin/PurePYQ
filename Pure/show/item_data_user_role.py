#  item_data_user_role.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from enum import IntEnum
from PySide6.QtCore import Qt


# 타이틀: Qt.ItemDataRole.DisplayRole
# 아이템: Qt.ItemDataRole.UserRole
class ItemDataUserRole(IntEnum):
    Uid = Qt.ItemDataRole.UserRole + 0x01
    Tag = Qt.ItemDataRole.UserRole + 0x02
    Excerpt = Qt.ItemDataRole.UserRole + 0x03
    Date = Qt.ItemDataRole.UserRole + 0x04

