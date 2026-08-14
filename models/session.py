class Session:
    def __init__(
        self,
        session_id=None,
        user_id=None,
        start_time=None,
        end_time=None,
        remaining_time=0,
        status="inactive",
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.remaining_time = remaining_time
        self.status = status