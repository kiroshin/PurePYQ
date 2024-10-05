#  plain_table_view.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QTableView, QFrame


class PlainTableView(QTableView):
    enter_key_pressed = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # 스크롤바는 필요할 때만 보여
        self.setFrameStyle(QFrame.Shape.NoFrame)    # 프레임 없어
        self.setWordWrap(False)                     # 워드랩 끄기
        self.setAlternatingRowColors(True)          # 지브라 칼라
        self.setShowGrid(False)                     # 본문 그리드
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)      # 한줄 전체 선택
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)         # 하나만 선택(다중선택 금지)
        self.setTabKeyNavigation(False)             # 탭 키 탐색 끄기

    # OVERRIDE
    def keyPressEvent(self, event: QKeyEvent):
        current_index = self.currentIndex()
        if current_index.isValid():
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                # Key_Return(엔터키), Key_Enter(숫자키패드)
                self.enter_key_pressed.emit(current_index)
                return
        QTableView.keyPressEvent(self, event)
