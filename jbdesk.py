import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QTextEdit,
                             QVBoxLayout, QWidget, QPushButton, QLabel,
                             QGroupBox, QComboBox, QHBoxLayout)
from PyQt5.QtCore import Qt
import pytz
from datetime import datetime

def remove_line_spaces(text):
    return '\n'.join([line for line in text.splitlines() if line.strip()])


def to_snake_case(text):
    text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)  # camelCase -> snake_case
    text = re.sub(r'[-\s]', '_', text)  # kebab-case, space -> snake_case
    return text.lower()


def to_camel_case(text):
    words = to_snake_case(text).split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(text):
    words = to_snake_case(text).split('_')
    return ''.join(word.capitalize() for word in words)


def to_kebab_case(text):
    return to_snake_case(text).replace('_', '-')


def to_screaming_snake_case(text):
    return to_snake_case(text).upper()


def to_train_case(text):
    return '-'.join(word.capitalize() for word in to_snake_case(text).split('_'))


def to_dot_notation(text):
    words = re.split(r'[\s_\-]+', text)
    return ".".join(word.lower() for word in words)

def to_camel_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_camel_case(line) for line in lines])

def to_snake_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_snake_case(line) for line in lines])

def to_pascal_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_pascal_case(line) for line in lines])

def to_screaming_snake_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_screaming_snake_case(line) for line in lines])

def to_kebab_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_kebab_case(line) for line in lines])

def to_train_case_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_train_case(line) for line in lines])

def to_dot_notation_line(text):
    lines = text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([to_dot_notation(line) for line in lines])

DATE_PATTERNS = [
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3}', '%Y-%m-%d %H:%M:%S %Z'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '%Y-%m-%d %H:%M:%S'),
    (r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', '%Y-%m-%d %H:%M'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M:%S %p'),
    (r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{1,2} [APap][Mm]', '%m/%d/%Y %I:%M %p'),
    (r'\d{4}-\d{1,2}-\d{1,2} [APap][Mm] \d{1,2}:\d{1,2}:\d{1,2}', '%Y-%m-%d %p %I:%M:%S'),
    (r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2} [APap][Mm]', '%Y-%m-%d %I:%M:%S %p'),
    (r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [-+]\d{4}', '%d/%b/%Y:%H:%M:%S %z')
]

def convert_log_timezone(log_text: str, source_timezone: str, dest_timezone: str) -> str:
    for pattern, date_format in DATE_PATTERNS:
        match = re.search(pattern, log_text)
        if match:
            datetime_str = match.group()
            try:
                dt = datetime.strptime(datetime_str, date_format)
                if '%z' not in date_format and '%Z' not in date_format:
                    source_tz = pytz.timezone(source_timezone)
                    dt = source_tz.localize(dt)
                dt = dt.astimezone(pytz.timezone(dest_timezone))
                new_datetime_str = dt.strftime(date_format)
                log_text = log_text.replace(datetime_str, new_datetime_str)
            except ValueError:
                continue
    return log_text

def convert_log_timezone_line(log_text: str, source_timezone: str, dest_timezone: str):
    lines = log_text.strip().split("\n")  # 줄 단위로 분리
    return "\n".join([convert_log_timezone(line, source_timezone, dest_timezone) for line in lines])

class JbDesk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

        self.create_menu()

    def create_menu(self):
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
    ex = JbDesk()
    ex.show()
    sys.exit(app.exec_())
