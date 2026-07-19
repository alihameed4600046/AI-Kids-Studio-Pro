class StatusBar:
    def __init__(self):
        self.status_label = "Ready"

    def set_status(self, text: str):
        self.status_label = text

    def get_status(self):
        return self.status_label