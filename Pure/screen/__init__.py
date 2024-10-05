#  == SCREEN ==
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import os
import asyncio
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox
)
from serving import Serving
from util.asyncio_helper import async_slot
from screen.content_view import ContentView


class MainWindow(QMainWindow):
    def __init__(self, title: str, service: Serving, app_data_path, app_cache_path):
        super().__init__()
        self.service = service
        self.app_data_path = app_data_path
        self.app_cache_path = app_cache_path
        self.setWindowTitle(title)
        self.setMinimumSize(650, 400)
        self.resize(700, 450)
        self.setup_menu_bar()
        self.msg_task = None

    async def __bootup__(self):
        self.setCentralWidget(ContentView(self.service, self))
        self.show()

    def setup_menu_bar(self):
        menu = self.menuBar()
        # FILE SECTION
        file_menu = menu.addMenu("&File")
        file_refresh_action = QAction("Refresh Data", self)
        file_refresh_action.triggered.connect(self.click_file_refresh_data)
        file_menu.addAction(file_refresh_action)
        file_clear_action = QAction("Clear Cache", self)
        file_clear_action.triggered.connect(self.click_file_clear_cache)
        file_menu.addAction(file_clear_action)
        file_menu.addSeparator()
        file_exit_action = QAction("Exit", self)
        file_exit_action.triggered.connect(self.close)
        file_menu.addAction(file_exit_action)
        #
        # EDIT SECTION
        #
        # VIEW SECTION
        view_menu = menu.addMenu("&View")
        view_data_folder_action = QAction("Show Data Folder", self)
        view_data_folder_action.triggered.connect(self.click_view_data_folder)
        view_menu.addAction(view_data_folder_action)
        view_cache_folder_action = QAction("Show Cache Folder", self)
        view_cache_folder_action.triggered.connect(self.click_view_cache_folder)
        view_menu.addAction(view_cache_folder_action)
        #
        # WINDOW SECTION
        #
        # HELP SECTION
        help_menu = menu.addMenu("&Help")
        help_about_action = QAction("About Pure", self)
        help_about_action.triggered.connect(self.click_help_about)
        help_menu.addAction(help_about_action)
        #

    def click_help_about(self):
        # 앱을 블로킹 하며 띄운다.
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("About")
        msgbox.setText("Pure 는 예시 프로그램")
        msgbox.exec()

    @async_slot
    async def click_file_refresh_data(self):
        await self.service.build_app_data_action(False)

    @async_slot
    async def click_file_clear_cache(self):
        await self.service.clear_app_cache_action()

    def click_view_data_folder(self):
        # 리눅스는 고려하지 않음
        if os.name == "nt":
            os.startfile(self.app_data_path)
        else:
            os.system(f"""open -R '{self.app_data_path}'""")

    def click_view_cache_folder(self):
        # 리눅스는 고려하지 않음
        if os.name == "nt":
            os.startfile(self.app_cache_path)
        else:
            os.system(f"""open -R '{self.app_cache_path}'""")

    # 메시지 핸들러: 베쓸이 쏴주는 메시지를 잠깐 보여주고 없앤다.
    async def receive_message(self, msg):
        self.statusBar().showMessage(msg)
        self.statusBar().show()
        if self.msg_task and not self.msg_task.done():
            self.msg_task.cancel()
        async def _disappear_after(sec):
            await asyncio.sleep(sec)
            self.statusBar().hide()
            self.statusBar().clearMessage()
        self.msg_task = asyncio.create_task(_disappear_after(sec=2))
        return self.msg_task

    # OVERRIDE
    # def closeEvent(self, event):
    #     super().closeEvent(event)


#
# SCREEN 은 UI 를 구성하는 기본 판을 제공합니다. 상태를 가지며 이를 통해 SHOW 를 컨트롤합니다.
# SHOW 서브클래싱하여 앱에 완전히 종속적인 컴포넌트로 구성할 수 있습니다.
# 내부에 VIEWMODEL 을 옵션으로 가질 수 있습니다.
# VIEWMODEL 은 종속적입니다. 따라서 내부에서 초기화합니다.
#
