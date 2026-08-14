class Command:
    def __init__(
        self,
        command_id=None,
        command=None,
        payload=None,
        status="pending",
    ):
        self.command_id = command_id
        self.command = command
        self.payload = payload
        self.status = status