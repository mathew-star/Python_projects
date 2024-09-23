class Session:
    def __init__(self, user):
        self.user = user
        self.is_active = True

    def end(self):
        self.is_active = False