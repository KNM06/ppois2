import sys
from PyQt6.QtWidgets import QApplication
from source.controller.Controller import Controller


def main() -> None:
    app = QApplication(sys.argv)
    controller = Controller()
    controller.run()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
