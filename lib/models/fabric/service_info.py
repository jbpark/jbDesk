class ServiceInfo:
    def __init__(self, service_name, user_name, log_path_access, log_path_level, urls, parser_name):
        self.service_name = service_name
        self.user_name = user_name
        self.log_path_access = log_path_access
        self.log_path_level = log_path_level
        self.urls = urls
        self.parser_name = parser_name
