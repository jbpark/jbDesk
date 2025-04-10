import logging

from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit, QComboBox,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)

from lib.manager.mariadb.mariadb_tenant_manager import MariadbTenantManager
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_MARIADB = "MARIADB"

MENU_ORDER_INFO = "Order Info"


def init_menu_mariadb_order(self, db_menu):
    order_info_action = QAction(MENU_ORDER_INFO, self)
    order_info_action.triggered.connect(lambda: self.set_function(MENU_ORDER_INFO))
    db_menu.addAction(order_info_action)


def setup_mariadb_order(yaml_loader, config_loader, main_layout):
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
    db_combo = QComboBox()
    db_combo.addItems(["FIRST", "SECOND"])
    db_combo.setCurrentText("FIRST")
    env_layout.addWidget(db_combo)
    env_group.setLayout(env_layout)
    first_line_layout.addWidget(env_group)

    # Orader 그룹박스
    name_group = QGroupBox("Name")
    name_layout = QHBoxLayout()
    name_line = QLineEdit()
    name_layout.addWidget(name_line)
    name_group.setLayout(name_layout)
    first_line_layout.addWidget(name_group)

    # Search 버튼
    search_btn = QPushButton("Search")
    search_btn.clicked.connect(lambda: search_mariadb_order(yaml_loader, config_loader, table, name_line,
                                                            env_combo, db_combo))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)


def search_mariadb_order(yaml_loader, config_loader, table, name_line, env_combo, db_combo):
    env_type = env_combo.currentText()
    db_type = db_combo.currentText()

    manager = MariadbTenantManager(yaml_loader, env_type, db_type, VENDOR_MARIADB)
    manager.ensure_connect_info(config_loader)
    order_resp = manager.select_order_info(name_line.text())

    if order_resp is None:
        logging.debug("cannot found order")
        return

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    # 새 행에 데이터 추가
    table.setItem(row_position, 0, QTableWidgetItem("Customer Name"))
    table.setItem(row_position, 1, QTableWidgetItem(order_resp.CUSTOMER_NAME))
    table.setItem(row_position, 2, QTableWidgetItem(""))

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    table.setItem(row_position, 0, QTableWidgetItem("Product"))
    table.setItem(row_position, 1, QTableWidgetItem(order_resp.PRODUCT))
    table.setItem(row_position, 2, QTableWidgetItem(""))
