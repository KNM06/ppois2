import socket
import threading


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"  # ip сервера
        self.port = 5555
        self.addr = (self.server, self.port)
        self.color = None
        self.connected = False
        self.callback = None

    # устанавливает функцию для обработки ходов соперника
    def set_callback(self, callback):
        self.callback = callback

    # подключается к серверу
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.color = self.client.recv(2048).decode()
            self.connected = True
            # запускаем поток для прослушивания ходов соперника
            threading.Thread(target=self.receive_moves, daemon=True).start()
            return self.color
        except Exception as e:
            print("Не удалось подключиться к серверу:", e)
            return None

    # отправляет ход на сервер
    def send_move(self, start_pos, end_pos):
        if self.connected:
            # формируем строку вида "r1,c1:r2,c2"
            msg = f"{start_pos[0]},{start_pos[1]}:{end_pos[0]},{end_pos[1]}"
            try:
                self.client.send(str.encode(msg))
            except:
                self.connected = False

    # получает ходы от сервера в фоновом потоке
    def receive_moves(self):
        while self.connected:
            try:
                data = self.client.recv(2048).decode()
                if data and self.callback:
                    # расшифровываем строку в координаты
                    parts = data.split(":")
                    start_pos = tuple(map(int, parts[0].split(",")))
                    end_pos = tuple(map(int, parts[1].split(",")))
                    self.callback(start_pos, end_pos)  # передаем ход в контроллер
            except:
                # если соединение разорвано, выходим из цикла
                self.connected = False
                break
