# nuitka-project-if: {OS} == "Windows":
#   nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/assets/appicon.ico
#   nuitka-project: --windows-console-mode=disable
#   nuitka-project: --standalone
# nuitka-project-if: {OS} == "Darwin":
#   nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/assets/appicon.icns
#   nuitka-project: --macos-app-name="Pure"
#   nuitka-project: --macos-signed-app-name="kiro.shin.Pure"
#   nuitka-project: --macos-app-version="0.1.0"
#   nuitka-project: --macos-create-app-bundle
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/assets/=assets
# nuitka-project: --output-filename=pure
#
#  == PURE ==
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.
#

import os
import sys
import logging
import asyncio
from multiprocessing import freeze_support
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
from asset import Asset
from vessel import Vessel
from screen import MainWindow


# APP INFO
APP_NAME = "Pure"
APP_VERSION = "0.1.0"
APP_IDENTIFIER = "com.example.pure"
APP_DB_FILENAME = "database.db"
APP_SCHEMA_FILENAME = "schema.sql"
APP_REPORT_FILENAME = "report.log"


# PROC FOR MSWIN
if sys.platform == "win32":
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_IDENTIFIER)


# DATA CACHE
def _app_path_support(app_data_path: str, app_cache_path: str):
    if not os.path.isdir(app_data_path):
        os.makedirs(app_data_path)
    if not os.path.isdir(app_cache_path):
        os.makedirs(app_cache_path)


# LOGGING
def _app_logging_support(app_report_path: str):
    logging.basicConfig(filename=app_report_path,
                        format="[%(asctime)s|%(levelname)s|%(module)s:%(lineno)s] > %(message)s",
                        datefmt="%y%m%d:%H%M%S")


# MAIN
if __name__ == "__main__":
    # MULTIPROCESSING ON WINDOWS
    freeze_support()

    # APP LOAD
    app = QApplication(sys.argv)
    app.setOrganizationDomain(APP_IDENTIFIER)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setWindowIcon(QIcon(Asset.Icon.app))

    # APP SUPPORT
    APP_DATA_PATH = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
    APP_CACHE_PATH = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.CacheLocation)
    _app_path_support(APP_DATA_PATH, APP_CACHE_PATH)
    _app_logging_support(os.path.join(APP_CACHE_PATH, APP_REPORT_FILENAME))

    # RUNLOOP - qasync
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    # VESSEL & WINDOW
    vessel = Vessel(
        data_path=APP_DATA_PATH,
        cache_path=APP_CACHE_PATH,
        db_filename=APP_DB_FILENAME
    )
    window = MainWindow(
        title=APP_NAME,
        service=vessel,
        app_data_path=APP_DATA_PATH,
        app_cache_path=APP_CACHE_PATH
    )
    vessel.set_message_handler(window.receive_message)

    # LAUNCH - qasync
    with event_loop:
        asyncio.gather(vessel.__bootup__(), window.__bootup__())
        event_loop.run_until_complete(app_close_event.wait())
        shutdown = asyncio.ensure_future(vessel.__shutdown__())
        while not shutdown.done():
            QApplication.instance().processEvents()
