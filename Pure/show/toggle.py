#  toggle.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, QSize, QPoint, QPointF, QRectF, Slot, Property
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from PySide6.QtWidgets import QCheckBox

__all__ = ['Toggle']


# 토글
# 책이 제법 두껍지만 설명도 충분하고 예제도 굉장히 좋다. QT 기본기를 배울 수 있다.
# https://www.pythonguis.com/
# https://github.com/pythonguis/pythonguis-examples
class Toggle(QCheckBox):
    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self,
                 bar_color=Qt.GlobalColor.gray,
                 checked_color="#00B0FF",
                 handle_color=Qt.GlobalColor.white,
                 parent=None):
        super().__init__(parent)
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())
        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self.stateChanged.connect(self.handle_state_change)

    # OVERRIDE
    def sizeHint(self):
        return QSize(58, 45)

    # OVERRIDE
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    # OVERRIDE
    def paintEvent(self, e: QPaintEvent):
        cont_rect = self.contentsRect()
        handle_radius = round(0.24 * cont_rect.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self._transparent_pen)
        bar_rect = QRectF(0, 0, cont_rect.width() - handle_radius, 0.40 * cont_rect.height())
        bar_rect.moveCenter(cont_rect.center())
        rounding = bar_rect.height() / 2
        trail_length = cont_rect.width() - 2 * handle_radius
        x_pos = cont_rect.x() + handle_radius + trail_length * self._handle_position
        if self.isChecked():
            painter.setBrush(self._bar_checked_brush)
            painter.drawRoundedRect(bar_rect, rounding, rounding)
            painter.setBrush(self._handle_checked_brush)
        else:
            painter.setBrush(self._bar_brush)
            painter.drawRoundedRect(bar_rect, rounding, rounding)
            painter.setPen(self._light_grey_pen)
            painter.setBrush(self._handle_brush)
        painter.drawEllipse(QPointF(x_pos, bar_rect.center().y()), handle_radius, handle_radius)
        painter.end()

    @Slot(int)
    def handle_state_change(self, value: int):
        self._handle_position = 1 if value else 0

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos: float):
        self._handle_position = pos
        self.update()
