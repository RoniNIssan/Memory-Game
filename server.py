import socket
import threading
import time
import elements
import pickle
import protocol_file

board = elements.Board(level=1, category="animals")
level = 1
players = []
end_game = False
ready_to_start = False
is_board_randomized = False
protocol = protocol_file.Protocol()


class Player:
    def __init__(self, id, user_socket, pid):
        self.id = id
        self.user_socket = user_socket
        self.pid = pid


def pack(obj: elements.Board) -> bytes:
    return pickle.dumps(obj)


def unpack(obj):
    return pickle.loads(obj)


def handle_client(player, tid):
    global protocol, players, ready_to_start, level, board, is_board_randomized
    
    to_send = protocol.build_message(protocol.get_welcome_command(), b'successful')
    protocol.send_message(to_send, player.user_socket)

    while not ready_to_start:
        time.sleep(0.8)
        to_send = protocol.build_message(protocol.get_wait_command(), b'waiting for another player')
        protocol.send_message(to_send, player.user_socket)

    to_send = protocol.build_message(protocol.get_ready_command(), b'successful')
    protocol.send_message(to_send, player.user_socket)

    if is_board_randomized:
        to_send = protocol.build_message(protocol.get_board_command(), pack(board))
        protocol.send_message(to_send, player.user_socket)


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


def randomize_game(level, categroy):
    global board
    board = elements.Board(level, categroy)


def main():
    global players, end_game, ready_to_start, board, level, is_board_randomized
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
    #     TODO: after connection - client sends msg so to see it is still connected
    ready_to_start = True

    while not end_game:
        # LEVEL 1
        # level = 1
        # randomize_game(level, "animals")
        # is_board_randomized = True

        # receive_data()
        pass

    for t in threads:
        t.join()
    server_socket.close()


if __name__ == "__main__":
    main()
