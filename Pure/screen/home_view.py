#  home_view.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, QSize, QSortFilterProxyModel
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from serving import *
from show import Toggle, PlainSearchBar, PlainListView, PlainListModel, TextItemDelegate
from screen.style import Style
from screen.home_viewmodel import HomeViewModel


class HomeView(QWidget):
    _viewmodel: HomeViewModel
    _searchbar: PlainSearchBar
    _listview: PlainListView

    def __init__(self, service: Serving, parent=None):
        super().__init__(parent)
        viewmodel = HomeViewModel(service, self)
        # LAYOUT
        self.setObjectName("HomeView")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        # LAYOUT FILL
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Style.Color.DarkBack)
        self.setPalette(palette)
        # HEADER-SEARCHBAR
        header = _wide_deco_paper(Style.Color.LightBack, 0.1, self)
        searchbar = PlainSearchBar(height=Style.Layout.CellLineHeight, parent=header)
        header.layout().addWidget(searchbar)
        layout.addWidget(header)
        # LISTVIEW
        sortfilter = _sortfilter(_datasource(viewmodel))
        listview = PlainListView(parent=self)
        listview.setModel(sortfilter)
        listview.setItemDelegate(TextItemDelegate(0.15, self))
        layout.addWidget(listview)
        # FOOTER
        footer = _wide_deco_paper(Style.Color.TailBack, 1.0, self)
        footer_layout: QHBoxLayout = footer.layout()
        footer_layout.addWidget(QLabel("Show Region"))
        toggle = Toggle(checked_color=Style.Color.Accent)
        footer_layout.addWidget(toggle, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
        # BIND
        self._viewmodel = viewmodel
        self._listview = listview
        self._searchbar = searchbar
        searchbar.textChanged.connect(sortfilter.setFilterFixedString)
        listview.doubleClicked.connect(viewmodel.select_person)
        listview.enter_key_pressed.connect(viewmodel.select_person)
        toggle.stateChanged.connect(viewmodel.show_region)

    # OVERRIDE
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F:
            self._searchbar.setFocus()
        if event.key() == Qt.Key.Key_Escape:
            self._searchbar.clear()
            self._listview.clearSelection()


def _wide_deco_paper(color: str, alpha: float, parent=None) -> QWidget:
    widget = QWidget(parent=parent)
    widget.setFixedHeight(Style.Layout.BarLineHeight)
    layout = QHBoxLayout()
    layout.setSpacing(Style.Space.Tiny)
    widget.setLayout(layout)
    # FILL
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    color = QColor(color)
    color.setAlphaF(alpha)
    palette.setColor(widget.backgroundRole(), color)
    widget.setPalette(palette)
    return widget


def _sortfilter(datasource) -> QSortFilterProxyModel:
    proxy = QSortFilterProxyModel()
    proxy.setSourceModel(datasource)
    proxy.setFilterRole(Qt.ItemDataRole.DisplayRole)   # DEFAULT
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    return proxy


def _datasource(viewmodel: HomeViewModel) -> PlainListModel:
    datasource = viewmodel.datasource
    datasource.size_hint = QSize(100, Style.Layout.CellLineHeight)
    font = QFont()
    font.setPixelSize(Style.Font.TextSize)
    datasource.font = font
    return datasource

