import socket
import threading
import time

players = []
end_game = False
ready_to_start = False


class Player:
    def __init__(self, id, user_socket, pid):
        self.id = id
        self.user_socket = user_socket
        self.pid = pid


def find_other_player_index(tid):
    if tid == 1:
        return 2
    else:
        return 1


def protocol_build_msg(msg_code):
    if msg_code == 'WLCM':
        return 'WLCM' + '#' + 'you are connected!'
    elif msg_code == 'WAIT':
        return 'WAIT' + '#' + 'waiting for another player'
    elif msg_code == 'RDEY':
        return 'RDEY' + '#' + 'ready to play!'


def send_msg(sock, msg):
    data = msg + '$'
    sock.send(data.encode())


def handle_client(player, tid):
    global players, ready_to_start
    to_send = protocol_build_msg('WLCM')
    send_msg(player.user_socket, to_send)

    while not ready_to_start:
        time.sleep(0.8)
        to_send = protocol_build_msg('WAIT')
        send_msg(player.user_socket, to_send)

    to_send = protocol_build_msg('RDEY')
    send_msg(player.user_socket, to_send)


def receive_data():
    # called by main thread
    global players

    # each client sends new data received during last turn
    # TODO: check what msg contains when no receive due to timeout
    # TODO: lock global
    player1_msg = players[0].get_socket().recv(1024)
    players[0].set_matrix(player1_msg)
    player2_msg = players[1].get_socket().recv(1024)
    players[1].set_matrix(player2_msg)


def main():
    global players, end_game, ready_to_start
    IP = '0.0.0.0'
    PORT = 3339
    TIMEOUT = 0.02

    # initiallizing server
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(20)
    # server_socket.settimeout(0.2)

    threads = []

    while len(threads) < 2:
        client_socket, addr = server_socket.accept()
        players.append(Player(addr, client_socket, len(threads)))
        t = threading.Thread(target=handle_client, args=(players[len(threads)], len(threads) + 1))
        t.start()
        threads.append(t)

    ready_to_start = True

    while not end_game:
        receive_data()

    for t in threads:
        t.join()
    server_socket.close()


if __name__ == "__main__":
    main()
