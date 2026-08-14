class Station:
    def __init__(
        self,
        station_id=None,
        station_name=None,
        agent_key=None,
        status="offline",
    ):
        self.station_id = station_id
        self.station_name = station_name
        self.agent_key = agent_key
        self.status = status