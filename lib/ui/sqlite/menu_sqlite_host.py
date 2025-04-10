import logging

from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit, QComboBox,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)

from lib.manager.mariadb.mariadb_tenant_manager import MariadbTenantManager
from lib.manager.sqlite.sqlite_tenant_manager import SqliteTenantManager
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_SQLITE = "SQLITE"

MENU_HOST_INFO = "Host Info"


def init_menu_sqlite_host(self, db_menu):
    order_info_action = QAction(MENU_HOST_INFO, self)
    order_info_action.triggered.connect(lambda: self.set_function(MENU_HOST_INFO))
    db_menu.addAction(order_info_action)


def setup_sqlite_host(yaml_loader, config_loader, main_layout):
    clear_layout(main_layout)

    # 첫째 라인
    first_line_layout = QHBoxLayout()

    # Orader 그룹박스
    name_group = QGroupBox("Name")
    name_layout = QHBoxLayout()
    name_line = QLineEdit()
    name_layout.addWidget(name_line)
    name_group.setLayout(name_layout)
    first_line_layout.addWidget(name_group)

    # Search 버튼
    search_btn = QPushButton("Search")
    search_btn.clicked.connect(lambda: search_sqlite_host(yaml_loader, config_loader, table, name_line))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)


def search_sqlite_host(yaml_loader, config_loader, table, name_line):
    manager = SqliteTenantManager(yaml_loader, None, None, VENDOR_SQLITE)
    manager.ensure_connect_info(config_loader)
    host_resp = manager.select_host_info(name_line.text())

    if host_resp is None:
        logging.debug("cannot found host")
        return

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    # 새 행에 데이터 추가
    table.setItem(row_position, 0, QTableWidgetItem("Host Name"))
    table.setItem(row_position, 1, QTableWidgetItem(host_resp.HOST_NAME))
    table.setItem(row_position, 2, QTableWidgetItem(""))

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    table.setItem(row_position, 0, QTableWidgetItem("Ip"))
    table.setItem(row_position, 1, QTableWidgetItem(host_resp.IP))
    table.setItem(row_position, 2, QTableWidgetItem(""))
