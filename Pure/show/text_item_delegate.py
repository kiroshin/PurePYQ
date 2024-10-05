#  text_item_delegate.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, QSize, QRect, QModelIndex, QPoint
from PySide6.QtGui import QColor, QPalette, QPainter
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from show.item_data_user_role import ItemDataUserRole

_INTRINSIC_SIZE = (80, 28)
_PADDING = 8


class TextItemDelegate(QStyledItemDelegate):
    def __init__(self, ratio: float, parent):
        super().__init__(parent=parent)
        self._ratio = ratio

    # OVERRIDE
    def sizeHint(self, option, index):
        if size := index.data(Qt.ItemDataRole.SizeHintRole):
            return size
        return QSize(_INTRINSIC_SIZE[0], _INTRINSIC_SIZE[1])

    # OVERRIDE
    # - QPainter: https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html
    # - QStyleOptionViewItem: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QStyleOptionViewItem.html
    # - QModelIndex: https://doc.qt.io/qtforpython-6/PySide6/QtCore/QModelIndex.html
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        # 데이터
        item_tag = index.data(ItemDataUserRole.Tag)
        item_title = index.data(Qt.ItemDataRole.DisplayRole)
        # 폰트
        font = index.data(Qt.ItemDataRole.FontRole)
        # 글자공간
        title_rect = QRect(option.rect)
        title_rect.setTopLeft(title_rect.topLeft() + QPoint(_PADDING, 0))
        tag_rect = QRect(option.rect) if item_tag else None
        if tag_rect:
            tag_rect.setTopLeft(tag_rect.topLeft() + QPoint(_PADDING, 0))
            tag_rect.setWidth(option.rect.width() * self._ratio)
            title_rect.setTopLeft(tag_rect.topRight())
        title_rect.setWidth(title_rect.width() - _PADDING)
        # 상태
        state = _are_active_selected(option)
        # 칠하기
        _draw_background(painter, option, state)
        _draw_text(painter, option, state, tag_rect, font, item_tag)
        _draw_text(painter, option, state, title_rect, font, item_title)


def _are_active_selected(option) -> int:
    if option.state & QStyle.StateFlag.State_Selected and \
            option.state & QStyle.StateFlag.State_Active:
        return 1
    if option.state & QStyle.StateFlag.State_Selected and \
            not option.state & QStyle.StateFlag.State_Active:
        return -1
    return 0


def _draw_background(painter, option, state):
    if not state:
        return
    painter.save()
    pen = painter.pen()
    pen.setColor(QColor(Qt.GlobalColor.transparent))
    painter.setPen(pen)  # 이슈: 선을 뭐라도 칠하지 않으면 셀렉션 시 줄이 생긴다.
    if 1 == state:
        painter.fillRect(option.rect, option.palette.color(QPalette.ColorRole.Link))
    elif -1 == state:
        painter.fillRect(option.rect, option.palette.color(QPalette.ColorRole.Mid))
    painter.restore()


def _draw_text(painter, option, state, rect, font, text):
    if not rect:
        return
    painter.save()
    pen = painter.pen()
    if 1 == state:
        pen.setColor(option.palette.color(QPalette.ColorRole.BrightText))
    painter.setPen(pen)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    painter.setFont(font)
    painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
    painter.restore()
