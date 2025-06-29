"""FSM events (messages) for WiFi Manager."""


class Message:
    def __init__(self, id):
        self.id = id


class EventConnectRequest(Message):
    def __init__(self):
        super().__init__("ConnectRequest")


class EventService(Message):
    def __init__(self):
        super().__init__("Service")


class EventConfigReceived(Message):
    def __init__(self):
        super().__init__("ConfigReceived")
