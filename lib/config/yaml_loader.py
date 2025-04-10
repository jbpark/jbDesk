import glob
import os
from pathlib import Path

import yaml
from ruamel.yaml import YAML

# 기본 yaml 폴더
DIR_DEFAULT_YAML = "settings"

# 사용자 yaml 폴더 (우선 순위 높음)
DIR_USER_YAML = "_settings"


def save_config_value(config_path: Path, key_path_str: str, value):
    """
    config_path에 'a.b.c' 같은 key_path 문자열을 사용하여 값을 설정.
    예: save_config_value(path, 'database.host', '127.0.0.1')
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # 파일 읽기
    data = {}
    if config_path.exists():
        with config_path.open("r") as f:
            data = yaml.load(f) or {}

    # 키 경로를 '.' 기준으로 나눔
    key_path = key_path_str.split('.')

    # 중첩 딕셔너리 생성
    ref = data
    for key in key_path[:-1]:
        if key not in ref or not isinstance(ref[key], dict):
            ref[key] = {}
        ref = ref[key]
    ref[key_path[-1]] = value

    # 저장
    with config_path.open("w") as f:
        yaml.dump(data, f)


def get_value_from_dic(data, key_path, delimiter='.'):
    keys = key_path.split(delimiter)
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None  # key path doesn't exist
    return current


def is_exist_key(config_path, key_path):
    override_data = {}

    if Path(config_path).exists():
        with Path(config_path).open("r") as f:
            override_data = yaml.safe_load(f) or {}

    if get_value_from_dic(override_data, key_path) is not None:
        return True

    return False


class YamlLoader:
    def __init__(self, root_path):
        self.root_path = root_path
        self.override__dir = os.path.join(self.root_path, DIR_USER_YAML)
        self.default_dir = os.path.join(self.root_path, DIR_DEFAULT_YAML)

    def load_config(self):

        merged_settings = {}

        # 먼저 fallback 디렉토리의 내용을 로딩 (우선순위 낮음)
        if self.default_dir and os.path.isdir(self.default_dir):
            for file_path in sorted(glob.glob(os.path.join(self.default_dir, "*.yaml"))):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    merged_settings.update(data)

        # 이후 우선순위가 높은 settings_dir의 내용을 덮어씀
        if os.path.isdir(self.override__dir):
            for file_path in sorted(glob.glob(os.path.join(self.override__dir, "*.yaml"))):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    merged_settings.update(data)

        return merged_settings

    def get_config_path(self, key_path):

        if self.override__dir and os.path.isdir(self.override__dir):
            for file_path in sorted(glob.glob(os.path.join(self.override__dir, "*.yaml"))):
                if is_exist_key(file_path, key_path):
                    return file_path

        if self.default_dir and os.path.isdir(self.default_dir):
            for file_path in sorted(glob.glob(os.path.join(self.default_dir, "*.yaml"))):
                if is_exist_key(file_path, key_path):
                    return file_path

        return None

    def save_config_value(self, key_path: list, value):
        config_path = self.get_config_path(key_path)

        if config_path is None:
            if not config_path.exists():
                print(f"{config_path} 파일이 존재하지 않아 새로 생성합니다.")
                config_path.parent.mkdir(parents=True, exist_ok=True)  # 디렉터리 없으면 생성
                with config_path.open("w") as f:
                    yaml.dump({}, f)
                    config_path = self.default_config_path

        save_config_value(config_path, key_path, value)
