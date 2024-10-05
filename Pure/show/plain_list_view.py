#  plain_list_view.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QListView, QFrame


class PlainListView(QListView):
    enter_key_pressed = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAlternatingRowColors(True)

    # OVERRIDE
    def keyPressEvent(self, event: QKeyEvent):
        current_index = self.currentIndex()
        if current_index.isValid():
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                # Key_Return(엔터키), Key_Enter(숫자키패드)
                self.enter_key_pressed.emit(current_index)
                return
        QListView.keyPressEvent(self, event)

