import logging

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit, QComboBox,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)

from lib.manager.fabric.log.fab_log_manager import FabLogManager
from lib.manager.fabric.log.fab_log_scheduler import FabLogScheduler
from lib.models.constants.service_name_type import ServiceType
from lib.models.log.log_level import LogLevel
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_MARIADB = "MARIADB"

MENU_ECHO_API_LOG = "Echo API Log"

g_table = None

class ThreadLogWorker(QThread):
    result_ready = pyqtSignal(object)  # row_index, result

    def __init__(self, yaml_loader, config_loader, env, keyword):
        super().__init__()
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.env = env
        self.keyword = keyword

    def run(self):
        try:
            service_name = ServiceType.GATEWAY.value.service_name
            manager = FabLogManager(self.env, self.keyword, service_name, LogLevel.DEBUG.value)
            scheduler = FabLogScheduler(manager, self.yaml_loader, self.config_loader)
            data = manager.get_log_info(scheduler)
        except Exception as e:
            logging.warn(f"Error: {e}")
            data = None

        logging.info("result_ready.emit")
        self.result_ready.emit(data)


class LogTableWindow:
    def __init__(self, parent_self, yaml_loader, config_loader, table, tid_line, env_combo):
        self.parent_self = parent_self
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.table = table
        self.tid_line = tid_line
        self.env_combo = env_combo

    def run_thread(self):
        env = self.env_combo.currentText()
        keyword = self.tid_line.text()
        thread = ThreadLogWorker(self.yaml_loader, self.config_loader, env, keyword)
        thread.result_ready.connect(self.parent_self.update_log_table)
        thread.start()
        self.parent_self.threads.append(thread)

def init_menu_search_log(self, menu_bar):
    log_menu = menu_bar.addMenu("Log")
    echo_log_action = QAction(MENU_ECHO_API_LOG, self)
    echo_log_action.triggered.connect(lambda: self.set_function(MENU_ECHO_API_LOG))
    log_menu.addAction(echo_log_action)

def update_log_table(table, data):
    table.setRowCount(0)

    if data is None or data.logs is None:
        logging.debug("cannot found log")
        return

    for log in data.logs:
        row_position = table.rowCount()  # 현재 행 개수 확인
        table.insertRow(row_position)  # 새 행 추가

        # 새 행에 데이터 추가
        table.setItem(row_position, 0, QTableWidgetItem(log.host))
        table.setItem(row_position, 1, QTableWidgetItem(log.path))
        table.setItem(row_position, 2, QTableWidgetItem(log.message))

    table.resizeColumnsToContents()

def setup_echo_api_log(self, yaml_loader, config_loader, main_layout):
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

    keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    tid_line.setText(keyword)

    # Search 버튼
    search_btn = QPushButton("Search")
    search_btn.clicked.connect(lambda: search_echo_api_log(self, yaml_loader, config_loader, table, tid_line, env_combo))
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

    self.result_table = table


def search_echo_api_log(self, yaml_loader, config_loader, table, tid_line, env_combo):
    keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    # keyword = "T2405110733507a666506"
    tid_line.setText(keyword)

    table_window = LogTableWindow(self, yaml_loader, config_loader, table, tid_line, env_combo)
    table_window.run_thread()
    #
    #
    #
    # env = env_combo.currentText()
    # keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    # # keyword = "T2405110733507a666506"
    # tid_line.setText(keyword)
    # tid_line.update()
    # keyword = tid_line.text()
    #
    # service_name = ServiceType.GATEWAY.value.service_name
    # manager = FabLogManager(env, keyword, service_name, LogLevel.DEBUG.value)
    # scheduler = FabLogScheduler(manager, yaml_loader, config_loader)
    # log_resp = manager.get_log_info(scheduler)
    #
    # if log_resp is None or log_resp.logs is None:
    #     logging.debug("cannot found log")
    #     return
    #
    # for log in log_resp.logs:
    #     row_position = table.rowCount()  # 현재 행 개수 확인
    #     table.insertRow(row_position)  # 새 행 추가
    #
    #     # 새 행에 데이터 추가
    #     table.setItem(row_position, 0, QTableWidgetItem(log.host))
    #     table.setItem(row_position, 1, QTableWidgetItem(log.path))
    #     table.setItem(row_position, 2, QTableWidgetItem(log.message))
    #
    # table.resizeColumnsToContents()
