import xml.dom.minidom as minidom
import xml.sax
from source.model.Player import Player
from source.model.xml_handler.PlayerHandler import PlayerHandler


def save_to_xml(filepath: str, players: list[Player]) -> None:
    doc = minidom.Document()

    root = doc.createElement("players")
    doc.appendChild(root)

    for player in players:
        player_elem = doc.createElement("player")
        root.appendChild(player_elem)

        def add_child(
            parent: minidom.Element, tag_name: str, text_content: str
        ) -> None:
            elem = doc.createElement(tag_name)
            text_node = doc.createTextNode(str(text_content))
            elem.appendChild(text_node)
            parent.appendChild(elem)

        add_child(player_elem, "full_name", player.full_name)
        add_child(player_elem, "birth_date", player.birth_date.strftime("%Y-%m-%d"))
        add_child(player_elem, "team", player.team)
        add_child(player_elem, "home_city", player.home_city)
        add_child(player_elem, "squad", player.squad)
        add_child(player_elem, "position", player.position)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="    "))


def load_from_xml(filepath: str) -> list[Player]:
    handler = PlayerHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(filepath)
    return handler.players
