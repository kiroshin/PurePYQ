#  content_view.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from enum import IntEnum
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter
from serving import *
from screen.home_view import HomeView
from screen.detail_view import DetailView
from screen.style import Style


class _SplitIdx(IntEnum):
    Home = 0
    Detail = 1


class ContentView(QSplitter):
    def __init__(self, service: Serving, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        home = HomeView(service, self)
        home.setMinimumWidth(Style.Layout.SidebarMinWidth)
        home.setMaximumWidth(Style.Layout.SidebarMaxWidth)
        detail = DetailView(service, self)
        self.addWidget(home)
        self.addWidget(detail)
        self.setHandleWidth(1)
        self.setStretchFactor(_SplitIdx.Home, 0)
        self.setStretchFactor(_SplitIdx.Detail, 1)
        self.setChildrenCollapsible(False)
        self.setSizes([Style.Layout.SidebarMinWidth])

