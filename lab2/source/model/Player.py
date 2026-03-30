import datetime


class Player:
    def __init__(
        self,
        full_name: str,
        birth_date: datetime.date,
        team: str,
        home_city: str,
        squad: str,
        position: str,
    ) -> None:
        self.full_name = full_name
        self.birth_date = birth_date
        self.team = team
        self.home_city = home_city
        self.squad = squad
        self.position = position

    def to_dict(self) -> dict:
        return {
            "full_name": self.full_name,
            "birth_date": self.birth_date.strftime("%Y-%m-%d"),
            "team": self.team,
            "home_city": self.home_city,
            "squad": self.squad,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        b_date = datetime.datetime.strptime(data["birth_date"], "%Y-%m-%d").date()
        return cls(
            full_name=data["full_name"],
            birth_date=b_date,
            team=data["team"],
            home_city=data["home_city"],
            squad=data["squad"],
            position=data["position"],
        )
