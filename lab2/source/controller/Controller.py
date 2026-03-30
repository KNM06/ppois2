import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
    QFileDialog,
    QDialog,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidgetItem,
)

from source.model.database.PlayerDatabase import PlayerDatabase
from source.view.MainWindow import MainWindow
from source.view.dialogs.AddPlayerDialog import AddPlayerDialog
from source.view.dialogs.SearchDialog import SearchDialog
from source.view.dialogs.DeleteDialog import DeleteDialog
import source.model.xml_handler.XmlUtils as XmlUtils
import random
from faker import Faker
from source.model.Player import Player


class Controller:
    def __init__(self) -> None:
        self.db = PlayerDatabase("players.db")
        self.view = MainWindow()

        self.current_page = 1
        self.per_page = 10

        self.connect_signals()
        self.load_page()

    def connect_signals(self) -> None:
        self.view.action_add.triggered.connect(self.show_add_dialog)
        self.view.action_search.triggered.connect(self.show_search_dialog)
        self.view.action_delete.triggered.connect(self.show_delete_dialog)
        self.view.action_save.triggered.connect(self.save_to_xml)
        self.view.action_load.triggered.connect(self.load_from_xml)
        self.view.action_tree.triggered.connect(self.show_tree_view)
        self.view.action_generate.triggered.connect(self.generate_test_data)
        self.view.btn_next.clicked.connect(self.next_page)
        self.view.btn_prev.clicked.connect(self.prev_page)
        self.view.btn_first.clicked.connect(self.first_page)
        self.view.btn_last.clicked.connect(self.last_page)
        self.view.cmb_per_page.currentTextChanged.connect(self.change_per_page)

    def load_page(self) -> None:
        players, total_records, total_pages = self.db.get_players_page(
            self.current_page, self.per_page
        )

        if self.current_page > total_pages and total_pages > 0:
            self.current_page = total_pages
            players, total_records, total_pages = self.db.get_players_page(
                self.current_page, self.per_page
            )

        self.view.update_table(players)
        self.view.update_pagination_labels(
            self.current_page, total_pages, total_records
        )
        self.total_pages = total_pages

    def next_page(self) -> None:
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_page()

    def prev_page(self) -> None:
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page()

    def first_page(self) -> None:
        if self.current_page != 1:
            self.current_page = 1
            self.load_page()

    def last_page(self) -> None:
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.load_page()

    def change_per_page(self, text: str) -> None:
        self.per_page = int(text)
        self.current_page = 1
        self.load_page()

    def show_add_dialog(self) -> None:
        dialog = AddPlayerDialog(self.view)
        if dialog.exec():
            new_player = dialog.get_player_data()
            self.db.add_player(new_player)
            self.load_page()

    def show_search_dialog(self) -> None:
        dialog = SearchDialog(self.view)

        def perform_search() -> None:
            idx = dialog.criteria_combo.currentIndex()
            if idx == 0:
                val1 = dialog.input_1.text()
                val2 = dialog.date_input.date().toString("yyyy-MM-dd")
            elif idx == 1:
                val1 = dialog.position_combo.currentText()
                val2 = dialog.squad_combo.currentText()
            else:
                val1 = dialog.input_1.text()
                val2 = dialog.input_2.text()

            results = self.db.search_players(idx, val1, val2)

            dialog.result_table.setRowCount(0)
            for row, player in enumerate(results):
                dialog.result_table.insertRow(row)
                dialog.result_table.setItem(row, 0, QTableWidgetItem(player.full_name))
                dialog.result_table.setItem(
                    row, 1, QTableWidgetItem(player.birth_date.strftime("%d.%m.%Y"))
                )
                dialog.result_table.setItem(row, 2, QTableWidgetItem(player.team))
                dialog.result_table.setItem(row, 3, QTableWidgetItem(player.home_city))
                dialog.result_table.setItem(row, 4, QTableWidgetItem(player.squad))
                dialog.result_table.setItem(row, 5, QTableWidgetItem(player.position))

        dialog.search_btn.clicked.connect(perform_search)
        dialog.exec()

    def show_delete_dialog(self) -> None:
        dialog = DeleteDialog(self.view)

        def perform_delete() -> None:
            idx = dialog.criteria_combo.currentIndex()

            warning_msg = (
                "Вы уверены, что хотите удалить ВСЕ записи?"
                if idx == 3
                else "Вы уверены, что хотите удалить записи по этому критерию?"
            )
            reply = QMessageBox.question(
                dialog,
                "Подтверждение удаления",
                warning_msg + "\nЭто действие нельзя отменить.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.No:
                return

            val1, val2 = "", ""
            if idx == 0:
                val1 = dialog.input_1.text()
                val2 = dialog.date_input.date().toString("yyyy-MM-dd")
            elif idx == 1:
                val1 = dialog.position_combo.currentText()
                val2 = dialog.squad_combo.currentText()
            elif idx == 2:
                val1 = dialog.input_1.text()
                val2 = dialog.input_2.text()

            deleted_count = self.db.delete_players(idx, val1, val2)

            if deleted_count > 0:
                QMessageBox.information(
                    dialog, "Успех", f"Успешно удалено записей: {deleted_count}"
                )
                self.load_page()
                dialog.accept()
            else:
                QMessageBox.warning(
                    dialog, "Результат", "Записи по заданным критериям не найдены."
                )

        dialog.delete_btn.clicked.connect(perform_delete)
        dialog.exec()

    def save_to_xml(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self.view, "Сохранить в XML", "", "XML Files (*.xml)"
        )
        if path:
            all_players, _, _ = self.db.get_players_page(1, 999999)
            XmlUtils.save_to_xml(path, all_players)
            QMessageBox.information(
                self.view, "Успех", "Данные успешно сохранены в XML (DOM)."
            )

    def load_from_xml(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self.view, "Загрузить из XML", "", "XML Files (*.xml)"
        )
        if path:
            try:
                players = XmlUtils.load_from_xml(path)
                self.db.clear_database()
                for p in players:
                    self.db.add_player(p)
                self.current_page = 1
                self.load_page()
                QMessageBox.information(
                    self.view, "Успех", f"Загружено записей: {len(players)} (SAX)."
                )
            except Exception as e:
                QMessageBox.critical(
                    self.view, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}"
                )

    def show_tree_view(self) -> None:
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Древовидное отображение")
        dialog.resize(500, 400)
        layout = QVBoxLayout(dialog)

        tree = QTreeWidget()
        tree.setHeaderLabel("Футболисты")
        layout.addWidget(tree)

        all_players, _, _ = self.db.get_players_page(1, 999999)
        for player in all_players:
            parent_item = QTreeWidgetItem(tree, [player.full_name])

            QTreeWidgetItem(
                parent_item,
                [f"Дата рождения: {player.birth_date.strftime('%d.%m.%Y')}"],
            )
            QTreeWidgetItem(parent_item, [f"Команда: {player.team}"])
            QTreeWidgetItem(parent_item, [f"Город: {player.home_city}"])
            QTreeWidgetItem(parent_item, [f"Состав: {player.squad}"])
            QTreeWidgetItem(parent_item, [f"Позиция: {player.position}"])

        dialog.exec()

    def run(self) -> None:
        self.view.show()

    def generate_test_data(self) -> None:
        fake = Faker("ru_RU")

        squads = ["Основной", "Запасной", "Резервный"]
        positions = ["Вратарь", "Защитник", "Полузащитник", "Нападающий"]
        teams = [
            "Спартак",
            "Зенит",
            "Динамо",
            "ЦСКА",
            "Локомотив",
            "Ростов",
            "Краснодар",
            "Рубин",
            "БАТЭ",
            "Шахтер",
        ]

        for _ in range(50):
            full_name = fake.name_male()
            birth_date = fake.date_of_birth(minimum_age=16, maximum_age=40)
            team = random.choice(teams)
            home_city = fake.city()
            squad = random.choice(squads)
            position = random.choice(positions)

            player = Player(full_name, birth_date, team, home_city, squad, position)
            self.db.add_player(player)

        self.load_page()
        QMessageBox.information(
            self.view, "Успех", "Успешно сгенерировано 50 тестовых записей футболистов!"
        )
