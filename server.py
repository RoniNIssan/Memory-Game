import socket
import threading
import time
import elements
import protocol_file


class Player:
    def __init__(self, addr, user_socket, pid):
        self.id = addr
        self.user_socket = user_socket
        self.pid = pid
        self.turn = False
        self.points = 0

    def is_turn(self):
        global turn
        if turn == self.pid:
            self.turn = True
        else:
            self.turn = False


board = elements.Board(level=1, category="animals")
level = 1
players = []
turn = 1

lock = threading.Lock()
update = False
end_game = False
two_clicks = False
pair_correct = False
ready_to_start = False
is_board_randomized = False
protocol = protocol_file.Protocol()


def handle_client(player, tid=0):
    global protocol, players, ready_to_start, level, board, is_board_randomized, turn, update, two_clicks, pair_correct
    
    to_send = protocol.build_message(protocol.get_welcome_command(), b'successful')
    protocol.send_message(to_send, player.user_socket)
    print(f"sent player {player.pid} {str(to_send[:4])}")

    while not ready_to_start:
        # time.sleep(0.8)
        to_send = protocol.build_message(protocol.get_wait_command(), b'waiting for another player')
        protocol.send_message(to_send, player.user_socket)
        print(f"sent player {player.pid} {str(to_send[:4])}")

    to_send = protocol.build_message(protocol.get_ready_command(), b'successful')
    protocol.send_message(to_send, player.user_socket)
    print(f"sent player {player.pid} {str(to_send[:4])}")


    while not is_board_randomized:
        continue

    turns_counter = 0

    while not end_game:
        print("start round")
        lock.acquire()
        pair_correct = False
        two_clicks = False
        lock.release()

        to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
        protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
        print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")

        turn = turns_counter % 2

        player.is_turn()

        if player.turn:
            to_send = protocol.build_message(protocol.get_my_turn_command(), b'its your turn.')
            protocol.send_message(to_send, players[turn].user_socket)
            print(f"sent player {players[turn].pid} {str(to_send[:4])}")

            count_clicks = 0
            while count_clicks < 2:
                try:
                    print("waiting for board")
                    handle_communication(player.user_socket)  # get data from user - update board
                    print("got new board")
                    count_clicks += 1
                except:
                    pass

                if count_clicks < 2:
                    to_send = protocol.build_message(protocol.get_wait_command(), b'got board. Waiting for updates.')
                    protocol.send_message(to_send, players[turn].user_socket)
                    print(f"sent player {players[turn].pid} {str(to_send[:4])}")

            handle_game()

            if pair_correct:
                to_send = protocol.build_message(protocol.get_correct_command(), b'correct! add 2 points.')
                protocol.send_message(to_send, players[turn].user_socket)
            else:
                to_send = protocol.build_message(protocol.get_worng_command(), b'wrong! no points will be added.')
                protocol.send_message(to_send, players[turn].user_socket)
                print(f"sent player {players[turn].pid} {str(to_send[:4])}")

        else:
            to_send = protocol.build_message(protocol.get_other_turn_command(), b'its other players turn.')
            protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
            print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")

            while True:
                if update:
                    to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
                    protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
                    print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")
                    update = False
                if two_clicks:
                    to_send = protocol.build_message(protocol.get_worng_command(), b'switching turns.')
                    protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
                    print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")
                    break

        turns_counter += 1
        # time.sleep(1.2)


def randomize_game(category):
    global board, is_board_randomized, level
    board = elements.Board(level, category)
    is_board_randomized = True


def receive_data():
    global turn, players

    while True:
        handle_communication(players[turn].user_socket)
        print("get turn msg")

        to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
        protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
        print("sent other not turn msg")


def handle_game():
    global turn, players, board, two_clicks, pair_correct
    count_up = 0
    list_up = []
    for card in board.cards_in_rand_location:
        if card.is_face_up:
            count_up += 1
            list_up.append(card)

        if count_up == 2:
            print("two clicks: " + str(two_clicks))
            if list_up[0].title == list_up[1].title:
                pair_correct = True
                players[turn].points += 1
                list_up[1].burnt = True
                list_up[0].burnt = True

            else:
                list_up[0].is_face_up = False
                list_up[1].is_face_up = False
            two_clicks = True
            break

def handle_msg(command: bytes, msg: bytes):
    """function handles messages from client """
    global ready_to_start, board, protocol, update, lock

    if command == protocol.get_board_command():
        update = True
        try:
            board = protocol_file.unpack(protocol.analyze_message(msg))
        except:
            pass


def received_messages(data_bytes: bytes):
    global protocol
    if data_bytes != b'':
        data_bytes = protocol.separate_messages(data_bytes)

        for message in data_bytes:
            handle_msg(message[:4], message)


def handle_communication(sock: socket.socket):
    msg = sock.recv(1024)
    received_messages(msg)


def main():
    global players, end_game, ready_to_start, board, level
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
        t = threading.Thread(target=handle_client, args=(players[len(threads)], len(threads)))
        t.start()
        threads.append(t)

    ready_to_start = True
    randomize_game("animals")

    # handle_game()
    while not end_game:
        continue
    for t in threads:
        t.join()
    server_socket.close()


if __name__ == "__main__":
    main()
