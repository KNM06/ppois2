import sqlite3
import math
import datetime
from source.model.Player import Player


class PlayerDatabase:
    def __init__(self, db_name: str = "players.db") -> None:
        self.db_name = db_name
        self.init_db()

    def init_db(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT,
                    birth_date TEXT,
                    team TEXT,
                    home_city TEXT,
                    squad TEXT,
                    position TEXT
                )
            """)
            conn.commit()

    def add_player(self, player: Player) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO players (full_name, birth_date, team, home_city, squad, position)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    player.full_name,
                    player.birth_date.strftime("%Y-%m-%d"),
                    player.team,
                    player.home_city,
                    player.squad,
                    player.position,
                ),
            )
            conn.commit()

    def clear_database(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players")
            conn.commit()

    def get_players_page(
        self, page: int, per_page: int
    ) -> tuple[list[Player], int, int]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM players")
            total_records = cursor.fetchone()[0]
            total_pages = (
                math.ceil(total_records / per_page) if total_records > 0 else 1
            )

            if page > total_pages:
                page = total_pages
            if page < 1:
                page = 1

            offset = (page - 1) * per_page
            cursor.execute(
                """
                SELECT full_name, birth_date, team, home_city, squad, position 
                FROM players LIMIT ? OFFSET ?
            """,
                (per_page, offset),
            )

            rows = cursor.fetchall()

            players = []
            for row in rows:
                players.append(
                    Player(
                        full_name=row[0],
                        birth_date=datetime.datetime.strptime(
                            row[1], "%Y-%m-%d"
                        ).date(),
                        team=row[2],
                        home_city=row[3],
                        squad=row[4],
                        position=row[5],
                    )
                )

            return players, total_records, total_pages

    def execute_query(self, query: str, params: tuple = ()) -> list[Player]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            players = []
            for row in rows:
                players.append(
                    Player(
                        full_name=row[1],
                        birth_date=datetime.datetime.strptime(
                            row[2], "%Y-%m-%d"
                        ).date(),
                        team=row[3],
                        home_city=row[4],
                        squad=row[5],
                        position=row[6],
                    )
                )
            return players

    def search_players(self, criteria_index: int, val1: str, val2: str) -> list[Player]:
        if criteria_index == 0:
            query = "SELECT * FROM players WHERE full_name LIKE ? AND birth_date = ?"
            return self.execute_query(query, (f"%{val1}%", val2))
        elif criteria_index == 1:
            query = "SELECT * FROM players WHERE position = ? OR squad = ?"
            return self.execute_query(query, (val1, val2))
        elif criteria_index == 2:
            query = "SELECT * FROM players WHERE team = ? OR home_city = ?"
            return self.execute_query(query, (val1, val2))

    def delete_players(
        self, criteria_index: int, val1: str = None, val2: str = None
    ) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if criteria_index == 0:
                query = "DELETE FROM players WHERE full_name LIKE ? AND birth_date = ?"
                cursor.execute(query, (f"%{val1}%", val2))
            elif criteria_index == 1:
                query = "DELETE FROM players WHERE position = ? OR squad = ?"
                cursor.execute(query, (val1, val2))
            elif criteria_index == 2:
                query = "DELETE FROM players WHERE team = ? OR home_city = ?"
                cursor.execute(query, (val1, val2))
            elif criteria_index == 3:
                query = "DELETE FROM players"
                cursor.execute(query)

            conn.commit()
            return cursor.rowcount
