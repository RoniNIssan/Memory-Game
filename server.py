import socket
import threading

players = []
end_game = False


class Player:
    def __int__(self, id, sock, tid):
        self._id = id
        self._sock = sock
        self._turn = tid

    def get_id(self):
        return self._id

    def get_socket(self):
        return self._sock

    def get_turn(self):
        return self._turn

    def win(self):
        pass


def find_other_player_index(tid):
    if tid == 1:
        return 2
    else:
        return 1


def handle_client(player, tid):
    global players
    other_player_index = find_other_player_index(tid)
    while True:
        if len(players) < 2:
            player.get_socket().send("waiting for another player".encode())
            continue
        else:
            player.get_socket().send(players[other_player_index - 1]) # TODO: pickle sent object


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
    global players, end_game
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
        player = Player(addr, client_socket, len(threads) + 1)
        players.append(player)
        t = threading.Thread(target=handle_client, args=(players[len(threads)], len(threads) + 1))
        t.start()
        threads.append(t)

    while not end_game:
        receive_data()

    for t in threads:
        t.join()
    server_socket.close()


if __name__ == "__main__":
    main()
