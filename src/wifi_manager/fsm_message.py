"""FSM events (messages) for WiFi Manager."""


class Message:
    def __init__(self, id):
        self.id = id


class EventConnectRequest(Message):
    def __init__(self):
        super().__init__("ConnectRequest")


class EventConnected(Message):
    def __init__(self):
        super().__init__("Connected")


class EventConnectFailed(Message):
    def __init__(self):
        super().__init__("ConnectFailed")


class EventConfigReceived(Message):
    def __init__(self):
        super().__init__("ConfigReceived")
