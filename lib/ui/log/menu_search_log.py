import logging

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit, QComboBox,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)

from lib.manager.process.manger_holder import get_shared_list
from lib.models.log.log_level import LogLevel
from lib.ui.menu_layout import clear_layout
from multiprocessing import Process

logging.basicConfig(level=logging.DEBUG)

VENDOR_MARIADB = "MARIADB"

MENU_SINGLE_API_LOG = "Single API Log"

g_table = None

def init_menu_search_log(self, menu_bar):
    log_menu = menu_bar.addMenu("Log")
    single_log_action = QAction(MENU_SINGLE_API_LOG, self)
    single_log_action.triggered.connect(lambda: self.set_function(MENU_SINGLE_API_LOG))
    log_menu.addAction(single_log_action)

def setup_single_api_log(yaml_loader, config_loader, main_layout):
    clear_layout(main_layout)

    # 첫째 라인
    first_line_layout = QHBoxLayout()

    # Env 그룹박스
    env_group = QGroupBox("Env")
    env_layout = QHBoxLayout()
    env_combo = QComboBox()
    env_combo.addItems(["Live", "Stage", "Dev"])
    env_combo.setCurrentText("Dev")
    env_layout.addWidget(env_combo)
    env_group.setLayout(env_layout)
    first_line_layout.addWidget(env_group)

    # Orader 그룹박스
    tid_group = QGroupBox("Tid")
    tid_layout = QHBoxLayout()
    tid_line = QLineEdit()
    tid_layout.addWidget(tid_line)
    tid_group.setLayout(tid_layout)
    first_line_layout.addWidget(tid_group)

    # Search 버튼
    search_btn = QPushButton("Search")
    search_btn.clicked.connect(lambda: search_single_api_log(yaml_loader, config_loader, table, tid_line, env_combo))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Host", "Log Path", "Message"])

    header = table.horizontalHeader()

    # 첫 번째 컬럼: 고정 너비
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    table.setColumnWidth(0, 100)

    # 두 번째 컬럼: 콘텐츠에 맞게 자동
    header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    # 세 번째 컬럼: 나머지 공간 채우기
    header.setSectionResizeMode(2, QHeaderView.Stretch)

    # 마우스로 컬럼 너비 조절 가능하도록 설정하기
    header.setSectionResizeMode(0, QHeaderView.Interactive)
    header.setSectionResizeMode(1, QHeaderView.Interactive)
    header.setSectionResizeMode(2, QHeaderView.Interactive)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)


def search_single_api_log(yaml_loader, config_loader, table, tid_line, env_combo):
    env = env_combo.currentText()
    keyword = "T250408204905517648d0"
    # keyword = "T2405110733507a666506"
    # keyword = tid_line.text()
