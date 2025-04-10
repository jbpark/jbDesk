import json


class LogSearchResponse:
    def __init__(self):
        self.status = None
        self.message = None
        self.command_type = None
        self.step = None
        self.index = None
        self.total = None
        self.logs = []

    def __str__(self):
        return (
            f"LogSearchResponse(\n"
            f"  status={self.status},\n"
            f"  message={self.message},\n"
            f"  command_type={self.command_type},\n"
            f"  step={self.step},\n"
            f"  index={self.index},\n"
            f"  total={self.total},\n"
            f"  logs={self.logs}\n"
            f")"
        )


class LogSearchResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, LogSearchResponse):
            return {'status': obj.status,
                    'message': obj.message,
                    'command_type': obj.command_type,
                    'step': obj.step,
                    'index': obj.index,
                    'total': obj.total,
                    'logs': [item.__dict__ for item in obj.logs]}
        return super().default(obj)
