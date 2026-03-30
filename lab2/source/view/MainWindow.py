from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QComboBox,
    QToolBar,
    QAbstractItemView,
    QHeaderView,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База футболистов")
        self.resize(900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.setup_menu_and_toolbar()

    def setup_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ФИО", "Дата рождения", "Команда", "Домашний город", "Состав", "Позиция"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.main_layout.addWidget(self.table)
        self.pagination_layout = QHBoxLayout()

        self.btn_first = QPushButton("<< Первая")
        self.btn_prev = QPushButton("< Назад")

        self.lbl_page_info = QLabel("Страница: 1 / 1")
        self.lbl_page_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_next = QPushButton("Вперед >")
        self.btn_last = QPushButton("Последняя >>")

        self.lbl_total_records = QLabel("Всего записей: 0")
        self.cmb_per_page = QComboBox()
        self.cmb_per_page.addItems(["10", "20", "50", "100"])

        self.pagination_layout.addWidget(self.btn_first)
        self.pagination_layout.addWidget(self.btn_prev)
        self.pagination_layout.addWidget(self.lbl_page_info)
        self.pagination_layout.addWidget(self.btn_next)
        self.pagination_layout.addWidget(self.btn_last)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(QLabel("Записей на стр:"))
        self.pagination_layout.addWidget(self.cmb_per_page)
        self.pagination_layout.addWidget(self.lbl_total_records)

        self.main_layout.addLayout(self.pagination_layout)

    def setup_menu_and_toolbar(self):
        self.action_load = QAction("Загрузить из XML", self)
        self.action_save = QAction("Сохранить в XML", self)
        self.action_add = QAction("Добавить игрока", self)
        self.action_search = QAction("Поиск", self)
        self.action_delete = QAction("Удалить", self)
        self.action_tree = QAction("Вид: Дерево", self)
        self.action_generate = QAction("Сгенерировать 50 записей", self)
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction(self.action_load)
        file_menu.addAction(self.action_save)
        edit_menu = menubar.addMenu("Записи")
        edit_menu.addAction(self.action_add)
        edit_menu.addAction(self.action_generate)
        edit_menu.addAction(self.action_search)
        edit_menu.addAction(self.action_delete)
        view_menu = menubar.addMenu("Вид")
        view_menu.addAction(self.action_tree)
        toolbar = QToolBar("Основная панель")
        self.addToolBar(toolbar)
        toolbar.addAction(self.action_load)
        toolbar.addAction(self.action_save)
        toolbar.addSeparator()
        toolbar.addAction(self.action_add)
        toolbar.addAction(self.action_generate)
        toolbar.addAction(self.action_search)
        toolbar.addAction(self.action_delete)
        toolbar.addSeparator()
        toolbar.addAction(self.action_tree)

    def update_table(self, players):
        self.table.setRowCount(0)
        for row, player in enumerate(players):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(player.full_name))
            self.table.setItem(
                row, 1, QTableWidgetItem(player.birth_date.strftime("%d.%m.%Y"))
            )
            self.table.setItem(row, 2, QTableWidgetItem(player.team))
            self.table.setItem(row, 3, QTableWidgetItem(player.home_city))
            self.table.setItem(row, 4, QTableWidgetItem(player.squad))
            self.table.setItem(row, 5, QTableWidgetItem(player.position))

    def update_pagination_labels(self, current_page, total_pages, total_records):
        self.lbl_page_info.setText(f"Страница: {current_page} / {total_pages}")
        self.lbl_total_records.setText(f"Всего записей: {total_records}")
