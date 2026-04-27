import socket
import threading

HOST = "127.0.0.1"  # локальный ip
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server.listen(2)  # сервер ждет только двух игроков
print("Сервер запущен. Ожидание игроков...")

clients = []


# обрабатывает подключение одного клиента
def handle_client(conn, player_id):
    conn.send(str.encode(player_id))  # выдаем цвет: 'w' первому, 'b' второму
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                break
            # получили ход от одного игрока - отправляем другому
            for c in clients:
                if c != conn:
                    c.send(data)
        except:
            break

    print(f"Игрок {player_id} отключился")
    clients.remove(conn)
    conn.close()


# главный цикл сервера, принимает новые подключения
while True:
    conn, addr = server.accept()
    clients.append(conn)
    # назначаем цвет в зависимости от порядка подключения
    player_id = "w" if len(clients) == 1 else "b"
    print(f"Подключился {addr}, выдаем цвет: {player_id}")
    # запускаем отдельный поток для каждого клиента
    threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
