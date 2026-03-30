from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QComboBox,
    QLabel,
    QStackedWidget,
    QSizePolicy,
)


class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удаление записей")
        self.resize(300, 200)

        self.layout = QVBoxLayout(self)

        self.criteria_combo = QComboBox()
        self.criteria_combo.addItems(
            [
                "1. По ФИО и дате рождения",
                "2. По позиции или составу",
                "3. По команде или родному городу",
                "4. Удалить ВСЕ записи",
            ]
        )
        self.criteria_combo.currentIndexChanged.connect(self.update_inputs)

        self.layout.addWidget(QLabel("Условие удаления:"))
        self.layout.addWidget(self.criteria_combo)

        self.form_layout = QFormLayout()

        self.input_1 = QLineEdit()
        self.input_2 = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)

        self.position_combo = QComboBox()
        self.position_combo.addItems(
            ["", "Вратарь", "Защитник", "Полузащитник", "Нападающий"]
        )

        self.squad_combo = QComboBox()
        self.squad_combo.addItems(["", "Основной", "Запасной", "Резервный"])

        self.stack1 = QStackedWidget()
        self.stack1.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.stack1.addWidget(self.input_1)
        self.stack1.addWidget(self.position_combo)

        self.stack2 = QStackedWidget()
        self.stack2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.stack2.addWidget(self.date_input)
        self.stack2.addWidget(self.squad_combo)
        self.stack2.addWidget(self.input_2)

        self.lbl_1 = QLabel("ФИО:")
        self.lbl_2 = QLabel("Дата рождения:")

        self.form_layout.addRow(self.lbl_1, self.stack1)
        self.form_layout.addRow(self.lbl_2, self.stack2)

        self.layout.addLayout(self.form_layout)

        self.delete_btn = QPushButton("Удалить записи")
        self.layout.addWidget(self.delete_btn)

    def update_inputs(self, index):
        self.lbl_1.show()
        self.lbl_2.show()
        self.stack1.show()
        self.stack2.show()

        if index == 0:
            self.lbl_1.setText("ФИО:")
            self.lbl_2.setText("Дата рождения:")
            self.stack1.setCurrentIndex(0)
            self.stack2.setCurrentIndex(0)
        elif index == 1:
            self.lbl_1.setText("Позиция:")
            self.lbl_2.setText("Состав:")
            self.stack1.setCurrentIndex(1)
            self.stack2.setCurrentIndex(1)
        elif index == 2:
            self.lbl_1.setText("Команда:")
            self.lbl_2.setText("Город:")
            self.stack1.setCurrentIndex(0)
            self.stack2.setCurrentIndex(2)
        elif index == 3:
            self.lbl_1.setText("ВНИМАНИЕ: База будет полностью очищена!")
            self.lbl_2.hide()
            self.stack1.hide()
            self.stack2.hide()
