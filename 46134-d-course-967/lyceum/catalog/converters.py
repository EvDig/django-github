__all__ = []


class IntConverter:
    regex = "[0-9]*[1-9]+[0-9]*"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
