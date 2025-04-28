import logging

from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit, QComboBox, QCheckBox, QWidget,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt

from lib.manager.log.log_search_manager import LogSearchManager
from lib.manager.log.log_search_scheduler import LogSearchScheduler
from lib.manager.test.service_test_manager import ServiceTestManager
from lib.models.constants.config_key import ConfigKey
from lib.models.constants.env_type import ENV_LIVE, ENV_STAGE, ENV_DEV
from lib.models.constants.service_name_type import ServiceType
from lib.models.log.log_level import LogLevel
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_MARIADB = "MARIADB"

MENU_TEST_SERVICE = "Test Service"

g_table = None


def init_menu_test_service(self, menu_bar):
    test_menu = menu_bar.addMenu("Test")
    test_service_action = QAction(MENU_TEST_SERVICE, self)
    test_service_action.triggered.connect(lambda: self.set_function(MENU_TEST_SERVICE))
    test_menu.addAction(test_service_action)

def save_env(yaml_loader, config_loader, table, tid_line, env_combo):
    section = MENU_TEST_SERVICE
    key = ConfigKey.KEY_ENV.key
    value = env_combo.currentText()
    config_loader.set_config(section, key, value)
    init_test_service(yaml_loader, config_loader, table, tid_line, env_combo)

def setup_test_service(yaml_loader, config_loader, main_layout):
    clear_layout(main_layout)

    # 첫째 라인
    first_line_layout = QHBoxLayout()

    # Env 그룹박스
    env_group = QGroupBox("Env")
    env_layout = QHBoxLayout()
    env_combo = QComboBox()
    env_combo.addItems([ENV_LIVE, ENV_STAGE, ENV_DEV])
    env_save = config_loader.get_config_with_default(MENU_TEST_SERVICE, ConfigKey.KEY_ENV.key, ENV_DEV)
    env_combo.setCurrentText(env_save)
    # env_combo.setCurrentText(ENV_DEV)
    env_layout.addWidget(env_combo)
    env_group.setLayout(env_layout)
    first_line_layout.addWidget(env_group)

    # Orader 그룹박스
    tid_group = QGroupBox("Service Name")
    tid_layout = QHBoxLayout()
    tid_line = QLineEdit()
    tid_layout.addWidget(tid_line)
    tid_group.setLayout(tid_layout)
    first_line_layout.addWidget(tid_group)

    env_combo.currentIndexChanged.connect(
        lambda: save_env(yaml_loader, config_loader, table, tid_line, env_combo))

    # Search 버튼
    search_btn = QPushButton("Test")
    search_btn.clicked.connect(lambda: test_service(yaml_loader, config_loader, table, tid_line, env_combo))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["Select", "Service Name", "Host Name", "Project", "Group"])

    header = table.horizontalHeader()

    # 첫 번째 컬럼: 고정 너비
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    table.setColumnWidth(0, 50)

    # 두 번째 컬럼: 고정 너비
    header.setSectionResizeMode(1, QHeaderView.Fixed)
    table.setColumnWidth(1, 100)

    # 두 번째 컬럼: 콘텐츠에 맞게 자동
    header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

    # 세 번째 컬럼: 나머지 공간 채우기
    header.setSectionResizeMode(4, QHeaderView.Stretch)

    # 마우스로 컬럼 너비 조절 가능하도록 설정하기
    header.setSectionResizeMode(0, QHeaderView.Interactive)
    header.setSectionResizeMode(1, QHeaderView.Interactive)
    header.setSectionResizeMode(2, QHeaderView.Interactive)
    header.setSectionResizeMode(3, QHeaderView.Interactive)
    header.setSectionResizeMode(4, QHeaderView.Interactive)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)

    init_test_service(yaml_loader, config_loader, table, tid_line, env_combo)

def init_test_service(yaml_loader, config_loader, table, tid_line, env_combo):
    env = env_combo.currentText()
    # keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    # keyword = "T2405110733507a666506"
    keyword = tid_line.text()

    manager = ServiceTestManager(env)
    manager.load_info(yaml_loader)

    table.setRowCount(0)

    infos = manager.service_test_infos
    for item in infos:
        row_position = table.rowCount()  # 현재 행 개수 확인
        table.insertRow(row_position)  # 새 행 추가

        checkbox = QCheckBox()
        checkbox_widget = QWidget()
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(checkbox, Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        table.setCellWidget(row_position, 0, checkbox_widget)

        # 새 행에 데이터 추가
        table.setItem(row_position, 1, QTableWidgetItem(item.service_name))
        table.setItem(row_position, 2, QTableWidgetItem(item.host_name))
        table.setItem(row_position, 3, QTableWidgetItem(item.project))
        table.setItem(row_position, 4, QTableWidgetItem(item.group))

    table.resizeColumnsToContents()


def test_service(yaml_loader, config_loader, table, tid_line, env_combo):
    env = env_combo.currentText()
    # keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    # keyword = "T2405110733507a666506"
    keyword = tid_line.text()

    manager = ServiceTestManager(env)
    manager.load_info(yaml_loader)

    infos = manager.service_test_infos
    for item in infos:
        row_position = table.rowCount()  # 현재 행 개수 확인
        table.insertRow(row_position)  # 새 행 추가

        checkbox = QCheckBox()
        checkbox_widget = QWidget()
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(checkbox, Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        table.setCellWidget(row_position, 0, checkbox_widget)

        # 새 행에 데이터 추가
        table.setItem(row_position, 1, QTableWidgetItem(item.service_name))
        table.setItem(row_position, 2, QTableWidgetItem(item.host_name))
        table.setItem(row_position, 3, QTableWidgetItem(item.project))
        table.setItem(row_position, 4, QTableWidgetItem(item.group))

    table.resizeColumnsToContents()

    # service_name = ServiceType.GATEWAY.value.service_name
    # manager = LogSearchManager(env, keyword, service_name, LogLevel.DEBUG.value)
    # scheduler = LogSearchScheduler(manager, yaml_loader, config_loader)
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
