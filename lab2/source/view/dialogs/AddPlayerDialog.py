from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QComboBox,
)
from PyQt6.QtCore import QDate
import datetime
from source.model.Player import Player


class AddPlayerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить футболиста")
        self.resize(300, 250)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.full_name_input = QLineEdit()

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())

        self.team_input = QLineEdit()
        self.home_city_input = QLineEdit()

        self.squad_input = QComboBox()
        self.squad_input.addItems(["Основной", "Запасной", "Резервный"])
        self.position_input = QComboBox()
        self.position_input.addItems(
            ["Вратарь", "Защитник", "Полузащитник", "Нападающий"]
        )

        self.form_layout.addRow("ФИО:", self.full_name_input)
        self.form_layout.addRow("Дата рождения:", self.birth_date_input)
        self.form_layout.addRow("Команда:", self.team_input)
        self.form_layout.addRow("Родной город:", self.home_city_input)
        self.form_layout.addRow("Состав:", self.squad_input)
        self.form_layout.addRow("Позиция:", self.position_input)

        self.layout.addLayout(self.form_layout)
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.accept)
        self.layout.addWidget(self.save_btn)

    def get_player_data(self):
        qdate = self.birth_date_input.date()
        py_date = datetime.date(qdate.year(), qdate.month(), qdate.day())

        return Player(
            full_name=self.full_name_input.text(),
            birth_date=py_date,
            team=self.team_input.text(),
            home_city=self.home_city_input.text(),
            squad=self.squad_input.currentText(),
            position=self.position_input.currentText(),
        )
