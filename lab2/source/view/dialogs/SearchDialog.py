from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QLabel,
    QStackedWidget,
    QSizePolicy,
)


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск записей")
        self.resize(600, 500)

        self.layout = QVBoxLayout(self)

        self.criteria_combo = QComboBox()
        self.criteria_combo.addItems(
            [
                "1. По ФИО и дате рождения",
                "2. По позиции или составу",
                "3. По команде или родному городу",
            ]
        )
        self.criteria_combo.currentIndexChanged.connect(self.update_inputs)

        self.layout.addWidget(QLabel("Выберите критерий поиска:"))
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

        self.lbl_1 = QLabel("ФИО (можно частично):")
        self.lbl_2 = QLabel("Дата рождения:")

        self.form_layout.addRow(self.lbl_1, self.stack1)
        self.form_layout.addRow(self.lbl_2, self.stack2)

        self.layout.addLayout(self.form_layout)

        self.search_btn = QPushButton("Найти")
        self.layout.addWidget(self.search_btn)

        self.result_table = QTableWidget(0, 6)
        self.result_table.setHorizontalHeaderLabels(
            ["ФИО", "Дата рожд.", "Команда", "Город", "Состав", "Позиция"]
        )
        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.layout.addWidget(self.result_table)

    def update_inputs(self, index):
        if index == 0:
            self.lbl_1.setText("ФИО (можно частично):")
            self.lbl_2.setText("Дата рождения:")
            self.stack1.setCurrentIndex(0)
            self.stack2.setCurrentIndex(0)
        elif index == 1:
            self.lbl_1.setText("Позиция:")
            self.lbl_2.setText("Состав:")
            self.stack1.setCurrentIndex(1)
            self.stack2.setCurrentIndex(1)
        elif index == 2:
            self.lbl_1.setText("Футбольная команда:")
            self.lbl_2.setText("Домашний город:")
            self.stack1.setCurrentIndex(0)
            self.stack2.setCurrentIndex(2)
