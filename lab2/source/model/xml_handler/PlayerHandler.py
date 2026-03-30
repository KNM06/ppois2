import xml.sax
import datetime
from typing import Any
from source.model.Player import Player


class PlayerHandler(xml.sax.ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.players = []
        self.current_data = ""

        self.full_name = ""
        self.birth_date = ""
        self.team = ""
        self.home_city = ""
        self.squad = ""
        self.position = ""

    def startElement(self, tag: str, attributes: Any) -> None:
        self.current_data = tag

    def characters(self, content: str) -> None:
        if self.current_data:
            text = content.strip()
            if not text:
                return

            if self.current_data == "full_name":
                self.full_name += text
            elif self.current_data == "birth_date":
                self.birth_date += text
            elif self.current_data == "team":
                self.team += text
            elif self.current_data == "home_city":
                self.home_city += text
            elif self.current_data == "squad":
                self.squad += text
            elif self.current_data == "position":
                self.position += text

    def endElement(self, tag: str) -> None:
        if tag == "player":
            b_date = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()
            player = Player(
                self.full_name,
                b_date,
                self.team,
                self.home_city,
                self.squad,
                self.position,
            )
            self.players.append(player)

            self.full_name = ""
            self.birth_date = ""
            self.team = ""
            self.home_city = ""
            self.squad = ""
            self.position = ""

        self.current_data = ""
