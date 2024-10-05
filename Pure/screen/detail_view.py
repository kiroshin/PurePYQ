#  detail_view.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHeaderView,
    QPushButton,
    QLabel,
    QHBoxLayout
)
from asset import Asset
from serving import *
from show import ProfileImgLabel, PlainTableView, PlainTableModel
from screen.detail_viewmodel import DetailViewModel
from screen.style import Style


class DetailView(QWidget):
    def __init__(self, service: Serving, parent=None):
        super().__init__(parent)
        viewmodel = DetailViewModel(service, self)
        # LAYOUT
        self.setObjectName("DetailView")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Style.Space.Tiny)  # 차일드 사이 간격
        self.setLayout(layout)
        # LAYOUT FILL
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Style.Color.LightBack)
        self.setPalette(palette)
        # TOP SPACE
        layout.addSpacing(Style.Space.Medium)
        # IMAGEVIEW
        imageview = ProfileImgLabel(square=128, parent=self)
        layout.addWidget(imageview, 0, Qt.AlignmentFlag.AlignCenter)
        # TABLEVIEW
        datasource = _datasource(viewmodel.datasource)
        tableview = _tableview(datasource, self)
        layout.addWidget(tableview)
        # BIND
        self._viewmodel = viewmodel
        viewmodel.photo.connect(imageview.set_image)
        # BOTTOM TEST BAR
        self.setup_test_widget()

    def setup_test_widget(self):
        test_widget = QWidget(parent=self)
        test_widget.setFixedHeight(Style.Layout.BarLineHeight)
        test_layout = QHBoxLayout()
        test_layout.setSpacing(Style.Space.Tiny)
        test_widget.setLayout(test_layout)
        test_widget.setAutoFillBackground(True)
        palette = test_widget.palette()
        palette.setColor(test_widget.backgroundRole(), Style.Color.TailBack)
        test_widget.setPalette(palette)
        # 하트 버튼
        fav_icon = QIcon()
        fav_icon.addFile(Asset.Icon.fav_fill, size=QSize(16, 16), mode=QIcon.Mode.Normal, state=QIcon.State.On)
        fav_icon.addFile(Asset.Icon.fav, size=QSize(16, 16), mode=QIcon.Mode.Normal, state=QIcon.State.Off)
        favorite = QPushButton(icon=fav_icon)
        favorite.setCheckable(True)
        favorite.setObjectName("Fav")
        favorite.setStyleSheet(r"#Fav {background-color: none; border: 0px;}")
        test_layout.addWidget(favorite, 0, Qt.AlignmentFlag.AlignCenter)
        # 출력 레이블
        label = QLabel("TEST LABEL")
        test_layout.addWidget(label, 2, Qt.AlignmentFlag.AlignCenter)
        # 액션 버튼
        btn = QPushButton("TEST ACTION")
        btn.clicked.connect(self._viewmodel.move_here)
        test_layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignCenter)
        # 바인딩
        self.layout().addWidget(test_widget)
        self._viewmodel.test_text.connect(label.setText)
        def fav_action(isch: bool):
            btn.setText(f"Favorite {isch}")
        favorite.clicked.connect(fav_action)


def _tableview(datasource, parent) -> PlainTableView:
    widget = PlainTableView(parent)
    widget.verticalHeader().setVisible(False)  # 세로 헤더 안 보이게
    widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)  # 고정
    widget.verticalHeader().setDefaultSectionSize(Style.Layout.CellLineHeight)  # 줄높이
    widget.horizontalHeader().setSectionsClickable(False)  # 헤더 클릭 선택 끄기
    widget.setModel(datasource)
    widget.setColumnWidth(0, Style.Layout.ColumnMinWidth)  # 0번 인덱스 고정 크기
    widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 나머지 확장
    return widget


def _datasource(datasource) -> PlainTableModel:
    datasource.size_hint = QSize(100, Style.Layout.CellLineHeight)
    font = QFont()
    font.setPixelSize(Style.Font.TextSize)
    datasource.font = font
    return datasource
