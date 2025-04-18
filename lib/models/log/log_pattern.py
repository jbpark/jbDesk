class LogPattern:
    def __init__(self, pattern, setter):
        self.pattern = pattern
        self.setter = setter

        if not setter:
            self.name = None
            return

        self.name = setter.__name__
        self.setter = setter
        self.pattern = pattern % self.name
