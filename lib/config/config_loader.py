import configparser
import os
import tkinter as tk
from tkinter import simpledialog

from lib.util.encoding_util import encrypt_cipher_text

# 기본 conf 폴더
DIR_DEFAULT_CONF = "settings"


def get_config_section(env_type, db_type, vendor):
    parts = [env_type, db_type, vendor]
    filtered = [str(p).upper() for p in parts if p is not None]
    return ".".join(filtered)


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, message, isSecure=False):
        self.message = message
        self.isSecure = isSecure
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        # 창 크기 키우기
        self.geometry("500x150")

        # 메시지 레이블
        tk.Label(master, text=self.message, wraplength=480, justify='left').pack(pady=10)

        # 입력 필드
        self.entry = tk.Entry(master, show='*' if self.isSecure else '', width=60)
        self.entry.pack(pady=5)
        return self.entry

    def apply(self):
        self.result = self.entry.get()


def get_input_with_message(title, message, isSecure=False):
    root = tk.Tk()
    root.withdraw()

    dialog = CustomDialog(root, title, message, isSecure)
    return dialog.result


def ensure_config(config_path, section, key, title, message, isSecure=False):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        # Config 파일이 없으면 새로 생성
        with open(config_path, "w") as config_file:
            config.write(config_file)

    config.read(config_path)

    if not config.has_section(section):
        config.add_section(section)

    value = config.get(section, key, fallback=None)

    if not value:
        value_new = get_input_with_message(title, message, isSecure)
        if value_new:
            if isSecure:
                value_new = encrypt_cipher_text(value_new)

            config.set(section, key, value_new)

            with open(config_path, "w") as config_file:
                config.write(config_file)
            print("Credentials saved to config file.")
            value = value_new
        else:
            print("No input provided. Exiting.")
            return None

    return value

def set_config(config_path, section, key, value):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        # Config 파일이 없으면 새로 생성
        with open(config_path, "w") as config_file:
            config.write(config_file)

    config.read(config_path)

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, key, value)

    with open(config_path, "w") as config_file:
        config.write(config_file)

def get_config(config_path, section, key):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        return None

    config.read(config_path)

    if not config.has_section(section):
        return None

    return config.get(section, key, fallback=None)


class ConfigLoader:
    def __init__(self, root_path, config_file):
        self.root_path = root_path
        self.config_file = config_file
        config_path = os.path.join(root_path, DIR_DEFAULT_CONF, config_file)
        self.config_path = config_path

    def ensure_config(self, section, key, title, message, isSecure=False):
        return ensure_config(self.config_path, section, key, title, message, isSecure)

    def get_config(self, section, key):
        return get_config(self.config_path, section, key)

    def set_config(self, section, key, value):
        return set_config(self.config_path, section, key, value)
