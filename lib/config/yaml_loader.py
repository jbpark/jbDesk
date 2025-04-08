import os
import yaml

class YamlLoader:
    def __init__(self, root_path, yaml_file):
        self.root_path = root_path
        self.yaml_file = yaml_file

    def load_config(self):
        primary_path = os.path.join(self.root_path, '_settings', self.yaml_file)
        fallback_path = os.path.join(self.root_path, self.yaml_file)

        config_path = primary_path if os.path.exists(primary_path) else fallback_path

        if not os.path.exists(config_path):
            raise FileNotFoundError("yaml 파일이 _settings 또는 실행 폴더에 존재하지 않습니다.")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        print(f"🔧 설정 파일 로드됨: {config_path}")
        return config
