#  plain_searchbar.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtWidgets import QLineEdit


class PlainSearchBar(QLineEdit):
    def __init__(self, height: int, parent=None):
        super().__init__(parent)
        self.setFixedHeight(height)
        self.setObjectName("PlainSearchBar")
        self.setStyleSheet("#PlainSearchBar {border: 2px solid white; border-radius: 5px;} #PlainSearchBar:focus {border-color: #1E8BFF;}")

