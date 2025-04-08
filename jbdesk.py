import logging
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QTextEdit,
                             QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit,
                             QGroupBox, QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtWidgets import QMenu, QMessageBox, QSystemTrayIcon

from lib.config.config_loader import ConfigLoader
from lib.config.yaml_loader import YamlLoader
from lib.db.mariadb.mariadb_tenant_manager import MariadbTenantManager
from lib.db.oracle.oracle_tenant_manager import OracleTenantManager
from lib.db.sqlite.sqlite_tenant_manager import SqliteTenantManager
from lib.util.log_util import convert_log_timezone_line
from lib.util.string_util import remove_line_spaces, to_camel_case_line, to_snake_case_line, to_pascal_case_line, \
    to_screaming_snake_case_line, to_train_case_line, to_dot_notation_line

logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE = "jbdesk.conf"
YAML_FILE = "config.yaml"
VENDOR_ORACLE = "ORACLE"
VENDOR_MARIADB = "MARIADB"
VENDOR_SQLITE = "SQLITE"

class JbDesk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initVariable()

    def initUI(self):
        self.init_widget()

        self.init_menu()

        self.init_tray()

    def initVariable(self):
        self.config_loader = ConfigLoader(os.path.join(os.getcwd(), CONFIG_FILE))
        self.yaml_loader = YamlLoader(os.getcwd(), YAML_FILE)

    def init_widget(self):
        self.setWindowTitle("JbDesk")
        self.setGeometry(300, 300, 1200, 900)
        self.selected_function = ""
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.tool_label = QLabel("선택된 기능: ", self)
        self.main_layout.addWidget(self.tool_label)
        self.input_group = QGroupBox("입력")
        self.input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_layout.addWidget(self.input_text)
        self.input_group.setLayout(self.input_layout)
        self.main_layout.addWidget(self.input_group)
        self.convert_button = QPushButton("변환")
        self.convert_button.setFixedWidth(self.convert_button.fontMetrics().width("변환") + 20)
        self.convert_button.clicked.connect(self.perform_conversion)
        self.main_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)
        self.output_group = QGroupBox("출력")
        self.output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_layout.addWidget(self.output_text)
        self.output_group.setLayout(self.output_layout)
        self.main_layout.addWidget(self.output_group)
        self.centralWidget.setLayout(self.main_layout)

    def init_tray(self):
        # 시스템 트레이 아이콘 생성
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = "tray_icon.png"  # 아이콘 경로 확인 (아이콘 파일이 있어야 합니다)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("PyQt5 Tray App")
        self.tray_icon.show()  # 트레이 아이콘 표시
        # 트레이 메뉴 설정
        tray_menu = QMenu()
        restore_action = QAction("열기", self)
        restore_action.triggered.connect(self.show_window)
        quit_action = QAction("종료", self)
        quit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_clicked)

    def closeEvent(self, event):
        """창 닫기 버튼(X) 클릭 시 앱 종료 여부 확인"""
        reply = QMessageBox.question(self, "종료 확인", "앱을 종료하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.exit_app()
        else:
            event.ignore()  # 창을 최소화하여 숨깁니다
            self.hide()  # 창 숨기기
            self.tray_icon.showMessage(
                "앱이 실행 중", "트레이에서 실행 중입니다.", QSystemTrayIcon.Information, 2000
            )

    def show_window(self):
        """트레이 메뉴에서 '열기' 선택 시 창 복원"""
        self.showNormal()
        self.activateWindow()

    def tray_icon_clicked(self, reason):
        """트레이 아이콘 클릭 시 창을 다시 보이게 함"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()

    def exit_app(self):
        """트레이 메뉴에서 '종료' 선택 시 앱 완전히 종료"""
        self.tray_icon.hide()  # 트레이 아이콘 숨기기
        QApplication.quit()  # PyQt5 이벤트 루프 종료
        sys.exit(0)  # 강제 종료

    def init_menu(self):
        menu_bar = self.menuBar()

        self.init_menu_line(menu_bar)

        self.init_menu_notation(menu_bar)

        self.init_menu_timezone(menu_bar)

        self.init_menu_db(menu_bar)

    def init_menu_db(self, menu_bar):
        db_menu = menu_bar.addMenu("Database")
        member_info_action = QAction("Member Info", self)
        member_info_action.triggered.connect(lambda: self.set_function("Member Info"))
        db_menu.addAction(member_info_action)

        order_info_action = QAction("Order Info", self)
        order_info_action.triggered.connect(lambda: self.set_function("Order Info"))
        db_menu.addAction(order_info_action)

        host_info_action = QAction("Host Info", self)
        host_info_action.triggered.connect(lambda: self.set_function("Host Info"))
        db_menu.addAction(host_info_action)

    def init_menu_timezone(self, menu_bar):
        timezone_menu = menu_bar.addMenu("TimeZone")
        timezone_action = QAction("로그 TimeZone 변환", self)
        timezone_action.triggered.connect(lambda: self.set_function("로그 TimeZone 변환"))
        timezone_menu.addAction(timezone_action)

    def init_menu_notation(self, menu_bar):
        notation_menu = menu_bar.addMenu("표기법")
        notations = ["camelCase", "snake_case", "PascalCase", "SCREAMING_SNAKE_CASE", "Train-Case", "dot.notation"]
        for notation in notations:
            action = QAction(notation, self)
            action.triggered.connect(lambda checked, n=notation: self.set_function(n))
            notation_menu.addAction(action)

    def init_menu_line(self, menu_bar):
        line_menu = menu_bar.addMenu("줄단위")
        line_action = QAction("줄 공백 제거", self)
        line_action.triggered.connect(lambda: self.set_function("줄 공백 제거"))
        line_menu.addAction(line_action)

    def set_function(self, function):
        self.selected_function = function
        self.tool_label.setText(f"선택된 기능: {function}")

        if function == "로그 TimeZone 변환":
            self.setup_timezone_conversion()
        elif function == "Member Info":
            self.setup_db_member()
        elif function == "Order Info":
            self.setup_db_order()
        elif function == "Host Info":
            self.setup_db_host()
        else:
            self.setup_text_conversion()

        self.main_layout.insertWidget(0, self.tool_label)

    def setup_db_member(self):
        self.clear_layout()

        # 첫째 라인
        first_line_layout = QHBoxLayout()

        # # Env 그룹박스
        # self.env_group = QGroupBox("Env")
        # env_layout = QHBoxLayout()
        # self.env_combo = QComboBox()
        # self.env_combo.addItems(["Live", "Stage", "Dev"])
        # self.env_combo.setCurrentText("Dev")
        # env_layout.addWidget(self.env_combo)
        # self.db_combo = QComboBox()
        # self.db_combo.addItems(["TRM", "OEM"])
        # self.db_combo.setCurrentText("TRM")
        # env_layout.addWidget(self.db_combo)
        # self.env_group.setLayout(env_layout)
        # first_line_layout.addWidget(self.env_group)
        #
        # # Member 그룹박스
        # self.member_group = QGroupBox("Member Uid")
        # member_layout = QHBoxLayout()
        # self.member_line = QLineEdit()
        # member_layout.addWidget(self.member_line)
        # self.member_group.setLayout(member_layout)
        # first_line_layout.addWidget(self.member_group)

        # Dataset Name 그룹박스
        self.dataset_group = QGroupBox("Member Name")
        dataset_layout = QHBoxLayout()
        self.dataset_line = QLineEdit()
        dataset_layout.addWidget(self.dataset_line)
        self.dataset_group.setLayout(dataset_layout)
        first_line_layout.addWidget(self.dataset_group)

        # Search 버튼
        self.search_btn = QPushButton("Search")
        #self.search_btn.clicked.connect(self.search_oracle_member)
        self.search_btn.clicked.connect(self.search_test_oracle_member)
        first_line_layout.addWidget(self.search_btn)

        # 둘째 라인 - Grid
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.main_layout.insertLayout(1, first_line_layout)
        self.main_layout.insertWidget(2, self.table)

    def search_test_oracle_member(self):

        manager = OracleTenantManager(self.yaml_loader, None, None, VENDOR_ORACLE)
        manager.ensure_connect_info(self.config_loader)
        #member_resp = manager.select_test_member_info(self.member_line.text(), self.dataset_line.text())
        member_resp = manager.select_test_member_info(self.dataset_line.text())

        if member_resp is None:
            logging.debug("cannot found member")
            return

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        # 새 행에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem("Name"))
        self.table.setItem(row_position, 1, QTableWidgetItem(member_resp.name))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        self.table.setItem(row_position, 0, QTableWidgetItem("Age"))
        self.table.setItem(row_position, 1, QTableWidgetItem(member_resp.age))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        logging.debug("search_oracle_member")

    def search_oracle_member(self):

        env_type = self.env_combo.currentText()
        db_type = self.db_combo.currentText()

        manager = OracleTenantManager(self.yaml_loader, env_type, db_type, VENDOR_ORACLE)

        manager.ensure_connect_info(self.config_loader)
        member_resp = manager.select_test_member_info(self.member_line.text(), self.dataset_line.text())

        if member_resp is None:
            logging.debug("cannot found member")
            return

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        # 새 행에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem("UserName"))
        self.table.setItem(row_position, 1, QTableWidgetItem(member_resp.USERNAME))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        self.table.setItem(row_position, 0, QTableWidgetItem("Timezone"))
        self.table.setItem(row_position, 1, QTableWidgetItem(member_resp.TIMEZONE))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        logging.debug("search_oracle_member")

    def setup_db_order(self):
        self.clear_layout()

        # 첫째 라인
        first_line_layout = QHBoxLayout()

        # Env 그룹박스
        self.env_group = QGroupBox("Env")
        env_layout = QHBoxLayout()
        self.env_combo = QComboBox()
        self.env_combo.addItems(["Live", "Stage", "Dev"])
        self.env_combo.setCurrentText("Dev")
        env_layout.addWidget(self.env_combo)
        self.db_combo = QComboBox()
        self.db_combo.addItems(["FIRST", "SECOND"])
        self.db_combo.setCurrentText("FIRST")
        env_layout.addWidget(self.db_combo)
        self.env_group.setLayout(env_layout)
        first_line_layout.addWidget(self.env_group)

        # Orader 그룹박스
        self.name_group = QGroupBox("Name")
        name_layout = QHBoxLayout()
        self.name_line = QLineEdit()
        name_layout.addWidget(self.name_line)
        self.name_group.setLayout(name_layout)
        first_line_layout.addWidget(self.name_group)

        # Search 버튼
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_mariadb_order)
        first_line_layout.addWidget(self.search_btn)

        # 둘째 라인 - Grid
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.main_layout.insertLayout(1, first_line_layout)
        self.main_layout.insertWidget(2, self.table)

    def search_mariadb_order(self):

        env_type = self.env_combo.currentText()
        db_type = self.db_combo.currentText()

        manager = MariadbTenantManager(self.yaml_loader, env_type, db_type, VENDOR_MARIADB)
        manager.ensure_connect_info(self.config_loader)
        order_resp = manager.select_order_info(self.name_line.text())

        if order_resp is None:
            logging.debug("cannot found order")
            return

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        # 새 행에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem("Customer Name"))
        self.table.setItem(row_position, 1, QTableWidgetItem(order_resp.CUSTOMER_NAME))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        self.table.setItem(row_position, 0, QTableWidgetItem("Product"))
        self.table.setItem(row_position, 1, QTableWidgetItem(order_resp.PRODUCT))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        logging.debug("search_mariadb_order")

    def setup_db_host(self):
        self.clear_layout()

        # 첫째 라인
        first_line_layout = QHBoxLayout()

        # Orader 그룹박스
        self.name_group = QGroupBox("Name")
        name_layout = QHBoxLayout()
        self.name_line = QLineEdit()
        name_layout.addWidget(self.name_line)
        self.name_group.setLayout(name_layout)
        first_line_layout.addWidget(self.name_group)

        # Search 버튼
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_sqlite_host)
        first_line_layout.addWidget(self.search_btn)

        # 둘째 라인 - Grid
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.main_layout.insertLayout(1, first_line_layout)
        self.main_layout.insertWidget(2, self.table)

    def search_sqlite_host(self):

        manager = SqliteTenantManager(self.yaml_loader, None, None, VENDOR_SQLITE)
        manager.ensure_connect_info(self.config_loader)
        host_resp = manager.select_host_info(self.name_line.text())

        if host_resp is None:
            logging.debug("cannot found host")
            return

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        # 새 행에 데이터 추가
        self.table.setItem(row_position, 0, QTableWidgetItem("Host Name"))
        self.table.setItem(row_position, 1, QTableWidgetItem(host_resp.HOST_NAME))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        row_position = self.table.rowCount()  # 현재 행 개수 확인
        self.table.insertRow(row_position)  # 새 행 추가

        self.table.setItem(row_position, 0, QTableWidgetItem("Ip"))
        self.table.setItem(row_position, 1, QTableWidgetItem(host_resp.IP))
        self.table.setItem(row_position, 2, QTableWidgetItem(""))

        logging.debug("search_mariadb_order")

    def setup_text_conversion(self):
        self.clear_layout()
        self.main_layout.insertWidget(1, self.input_group)
        self.main_layout.insertWidget(2, self.convert_button, alignment=Qt.AlignCenter)
        self.main_layout.insertWidget(3, self.output_group)

    def setup_timezone_conversion(self):
        self.clear_layout()

        self.timezone_layout = QHBoxLayout()
        self.from_group = QGroupBox("원본 TimeZone")
        self.from_layout = QVBoxLayout()
        self.from_timezone = QComboBox()
        self.from_layout.addWidget(self.from_timezone)
        self.from_group.setLayout(self.from_layout)
        self.from_timezone.addItems(["US/Pacific", "Asia/Seoul"])

        self.to_group = QGroupBox("목표 TimeZone")
        self.to_layout = QVBoxLayout()
        self.to_timezone = QComboBox()
        self.to_layout.addWidget(self.to_timezone)
        self.to_group.setLayout(self.to_layout)
        self.to_timezone.addItems(["US/Pacific", "Asia/Seoul"])
        self.to_timezone.setCurrentText("Asia/Seoul")

        self.timezone_layout.addWidget(self.from_group)
        self.timezone_layout.addWidget(self.to_group)
        self.timezone_layout.addWidget(self.convert_button)

        self.main_layout.insertWidget(1, self.input_group)
        self.main_layout.insertLayout(2, self.timezone_layout)
        self.main_layout.insertWidget(3, self.output_group)

    def clear_layout(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().setParent(None)

    def perform_conversion(self):
        text = self.input_text.toPlainText()

        if self.selected_function == "줄 공백 제거":
            result = remove_line_spaces(text)
        elif self.selected_function == "camelCase":
            result = to_camel_case_line(text)
        elif self.selected_function == "snake_case":
            result = to_snake_case_line(text)
        elif self.selected_function == "PascalCase":
            result = to_pascal_case_line(text)
        elif self.selected_function == "SCREAMING_SNAKE_CASE":
            result = to_screaming_snake_case_line(text)
        elif self.selected_function == "Train-Case":
            result = to_train_case_line(text)
        elif self.selected_function == "dot.notation":
            result = to_dot_notation_line(text)
        elif self.selected_function == "로그 TimeZone 변환":
            result = convert_log_timezone_line(text, self.from_timezone.currentText(), self.to_timezone.currentText())
        else:
            result = "선택된 기능이 없습니다."

        self.output_text.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 모든 창이 닫혀도 앱이 종료되지 않도록 설정
    app.setQuitOnLastWindowClosed(False)

    # 아이콘 설정
    app.setWindowIcon(QIcon("tray_icon.png"))

    window = JbDesk()
    window.show()
    sys.exit(app.exec_())
