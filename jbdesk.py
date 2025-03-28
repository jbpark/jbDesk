import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QTextEdit,
                             QVBoxLayout, QWidget, QPushButton, QLabel,
                             QGroupBox, QComboBox, QHBoxLayout)
from PyQt5.QtWidgets import QMenu, QMessageBox, QSystemTrayIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from lib.util.log_util import convert_log_timezone_line
from lib.util.string_util import remove_line_spaces, to_camel_case_line, to_snake_case_line, to_pascal_case_line, \
    to_screaming_snake_case_line, to_train_case_line, to_dot_notation_line


class JbDesk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.init_widget()

        self.init_menu()

        self.init_tray()

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

        line_menu = menu_bar.addMenu("줄단위")
        line_action = QAction("줄 공백 제거", self)
        line_action.triggered.connect(lambda: self.set_function("줄 공백 제거"))
        line_menu.addAction(line_action)

        notation_menu = menu_bar.addMenu("표기법")
        notations = ["camelCase", "snake_case", "PascalCase", "SCREAMING_SNAKE_CASE", "Train-Case", "dot.notation"]
        for notation in notations:
            action = QAction(notation, self)
            action.triggered.connect(lambda checked, n=notation: self.set_function(n))
            notation_menu.addAction(action)

        timezone_menu = menu_bar.addMenu("TimeZone")
        timezone_action = QAction("로그 TimeZone 변환", self)
        timezone_action.triggered.connect(lambda: self.set_function("로그 TimeZone 변환"))
        timezone_menu.addAction(timezone_action)

    def set_function(self, function):
        self.selected_function = function
        self.tool_label.setText(f"선택된 기능: {function}")

        if function == "로그 TimeZone 변환":
            self.setup_timezone_conversion()
        else:
            self.setup_text_conversion()

        self.main_layout.insertWidget(0, self.tool_label)

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
