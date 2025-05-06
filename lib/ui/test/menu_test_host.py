import logging

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QLineEdit, QComboBox, QCheckBox, QGroupBox, QHBoxLayout, QHeaderView)
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton

from lib.manager.fabric.test.fab_test_manager import FabTestManager
from lib.manager.fabric.test.fab_test_scheduler import FabTestScheduler
from lib.models.constants.config_key import ConfigKey
from lib.models.constants.env_type import ENV_LIVE, ENV_STAGE, ENV_DEV
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_MARIADB = "MARIADB"

MENU_TEST_SERVICE = "Test Service"

class ThreadTestWorker(QThread):
    result_ready = pyqtSignal(object)  # row_index, result

    def __init__(self, yaml_loader, config_loader, env):
        super().__init__()
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.env = env

    def run(self):
        try:
            manager = FabTestManager(self.env, None, None, None)
            scheduler = FabTestScheduler(manager, self.yaml_loader, self.config_loader)
            data = manager.get_test_data(scheduler)
        except Exception as e:
            logging.warn(f"Error: {e}")
            data = None

        logging.info("result_ready.emit")
        self.result_ready.emit(data)


class TestTableWindow:
    def __init__(self, parent_self, yaml_loader, config_loader, table, tid_line, env_combo):
        self.parent_self = parent_self
        self.yaml_loader = yaml_loader
        self.config_loader = config_loader
        self.table = table
        self.tid_line = tid_line
        self.env_combo = env_combo

    def run_thread(self):
        env = self.env_combo.currentText()
        thread = ThreadTestWorker(self.yaml_loader, self.config_loader, env)
        thread.result_ready.connect(self.parent_self.update_test_table)
        thread.start()
        self.parent_self.threads.append(thread)


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


def setup_test_service(self, yaml_loader, config_loader, main_layout):
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
    search_btn.clicked.connect(lambda: test_service(self, yaml_loader, config_loader, table, tid_line, env_combo))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["Select", "Service Name", "Host Name", "Project", "Group", "OS"])

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

    header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    # 세 번째 컬럼: 나머지 공간 채우기
    header.setSectionResizeMode(5, QHeaderView.Stretch)

    # 마우스로 컬럼 너비 조절 가능하도록 설정하기
    header.setSectionResizeMode(0, QHeaderView.Interactive)
    header.setSectionResizeMode(1, QHeaderView.Interactive)
    header.setSectionResizeMode(2, QHeaderView.Interactive)
    header.setSectionResizeMode(3, QHeaderView.Interactive)
    header.setSectionResizeMode(4, QHeaderView.Interactive)
    header.setSectionResizeMode(5, QHeaderView.Interactive)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)

    self.result_table = table

    init_test_service(yaml_loader, config_loader, table, tid_line, env_combo)


def update_test_table(table, data):
    table.setRowCount(0)

    for item in data.logs:
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
        table.setItem(row_position, 1, QTableWidgetItem(item.connect_info.service.service_name))
        table.setItem(row_position, 2, QTableWidgetItem(item.connect_info.host.host_name))
        table.setItem(row_position, 3, QTableWidgetItem(item.connect_info.project))
        table.setItem(row_position, 4, QTableWidgetItem(item.connect_info.group))
        table.setItem(row_position, 5, QTableWidgetItem(item.os_info))

    table.resizeColumnsToContents()


def init_test_service(yaml_loader, config_loader, table, tid_line, env_combo):
    env = env_combo.currentText()
    keyword = "db34a6fa-af3d-4aad-a783-6fbbb4b2bf65"
    # keyword = "T2405110733507a666506"
    # tid_line.setText(keyword)
    # tid_line.update()
    keyword = tid_line.text()

    manager = FabTestManager(env, None, None, None)
    scheduler = FabTestScheduler(manager, yaml_loader, config_loader)
    data = manager.get_data(scheduler)

    update_test_table(table, data)


def test_service(self, yaml_loader, config_loader, table, tid_line, env_combo):
    table_window = TestTableWindow(self, yaml_loader, config_loader, table, tid_line, env_combo)
    table_window.run_thread()
