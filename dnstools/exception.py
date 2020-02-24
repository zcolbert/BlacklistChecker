class HostError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class EmptyHostError(HostError):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

