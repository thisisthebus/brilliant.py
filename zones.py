class Zone(object):

    def __init__(self, name, range=None):
        self.name = name
        self.range = range
        self.current_color = (0, 0, 0, 0)

