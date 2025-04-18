import logging

from PyQt5.QtWidgets import (QAction, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView)

from lib.manager.oracle.dao.dao_emp import select_emp_info
from lib.manager.oracle.oracle_tenant_manager import OracleTenantManager
from lib.ui.menu_layout import clear_layout

logging.basicConfig(level=logging.DEBUG)

VENDOR_ORACLE = "ORACLE"

MENU_EMP_INFO = "Emp Info"


def init_menu_oracle_emp(self, db_menu):
    member_info_action = QAction(MENU_EMP_INFO, self)
    member_info_action.triggered.connect(lambda: self.set_function(MENU_EMP_INFO))
    db_menu.addAction(member_info_action)


def setup_oracle_emp(yaml_loader, config_loader, main_layout):
    clear_layout(main_layout)

    # 첫째 라인
    first_line_layout = QHBoxLayout()

    name_group = QGroupBox("Name")
    dataset_layout = QHBoxLayout()
    name_line = QLineEdit()
    dataset_layout.addWidget(name_line)
    name_group.setLayout(dataset_layout)
    first_line_layout.addWidget(name_group)

    # Search 버튼
    search_btn = QPushButton("Search")
    search_btn.clicked.connect(lambda: search_oracle_emp(yaml_loader, config_loader, table, name_line.text()))
    first_line_layout.addWidget(search_btn)

    # 둘째 라인 - Grid
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Column", "Value", "Comment"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    main_layout.insertLayout(1, first_line_layout)
    main_layout.insertWidget(2, table)


def search_oracle_emp(yaml_loader, config_loader, table, name):
    manager = OracleTenantManager(yaml_loader, None, None, VENDOR_ORACLE)
    manager.ensure_connect_info(config_loader)
    db_resp = select_emp_info(manager.get_db_session(), name)

    if db_resp is None:
        return

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    # 새 행에 데이터 추가
    table.setItem(row_position, 0, QTableWidgetItem("Name"))
    table.setItem(row_position, 1, QTableWidgetItem(db_resp.NAME))
    table.setItem(row_position, 2, QTableWidgetItem(""))

    row_position = table.rowCount()  # 현재 행 개수 확인
    table.insertRow(row_position)  # 새 행 추가

    table.setItem(row_position, 0, QTableWidgetItem("Job"))
    table.setItem(row_position, 1, QTableWidgetItem(db_resp.JOB))
    table.setItem(row_position, 2, QTableWidgetItem(""))
