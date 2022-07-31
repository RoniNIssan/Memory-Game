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
        self.win = False
        self.loose = False
        self.points = 0
        self.disconnected = False

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
count_burnt = 0

lock = threading.Lock()
update = False
end_game = False
two_clicks = False
pair_correct = False
ready_to_start = False
is_board_randomized = False
protocol = protocol_file.Protocol()


def handle_client(player, tid=0):
    global protocol, players, ready_to_start, level, board, is_board_randomized, turn, update, two_clicks, pair_correct, count_burnt
    
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
    count_burnt = 0

    while not end_game:

        print("start round")
        lock.acquire()
        pair_correct = False
        two_clicks = False
        lock.release()

        to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
        protocol.send_message(to_send, players[tid].user_socket)
        print(f"sent player {players[tid].pid} {str(to_send[:4])}")

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

            lock.acquire()
            two_clicks = True
            lock.release()
            handle_game()

            if pair_correct:
                to_send = protocol.build_message(protocol.get_correct_command(), b'correct! add 2 points.')
                protocol.send_message(to_send, players[turn].user_socket)
            else:
                to_send = protocol.build_message(protocol.get_wrong_command(), b'wrong! no points will be added.')
                protocol.send_message(to_send, players[turn].user_socket)
                print(f"sent player {players[turn].pid} {str(to_send[:4])}")

        else:
            to_send = protocol.build_message(protocol.get_other_turn_command(), b'its other players turn.')
            protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
            print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")

            count_updates = 0
            while True:
                if update:
                    count_updates += 1
                    to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
                    protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
                    print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")
                    lock.acquire()
                    update = False
                    lock.release()

                if count_updates >= 2:
                    to_send = protocol.build_message(protocol.get_wrong_command(), b'switching turns.')
                    protocol.send_message(to_send, players[(turn + 1) % 2].user_socket)
                    print(f"sent player {players[(turn + 1) % 2].pid} {str(to_send[:4])}")
                    break
        turns_counter += 1
        while not is_board_randomized:
            if end_game:
                print("endgame")
                break
            continue

    to_send = protocol.build_message(protocol.get_end_command(), b'Almost closing')
    protocol.send_message(to_send, players[tid].user_socket)
    print(f"sent player {players[tid].pid} {str(to_send[:4])}")

    if players[tid].win and not players[tid].loose:
        to_send = protocol.build_message(protocol.get_win_command(), b'Well done!')
        protocol.send_message(to_send, players[tid].user_socket)
        print(f"sent player {players[tid].pid} {str(to_send[:4])}")

    elif players[tid].loose and not players[tid].win:
        to_send = protocol.build_message(protocol.get_win_command(), b'Do better next time!')
        protocol.send_message(to_send, players[tid].user_socket)
        print(f"sent player {players[tid].pid} {str(to_send[:4])}")

    else:
        to_send = protocol.build_message(protocol.get_tie_command(), b'great effort!')
        protocol.send_message(to_send, players[tid].user_socket)
        print(f"sent player {players[tid].pid} {str(to_send[:4])}")

    players[tid].user_socket.close()
    players[tid].disconnected = True


def check_victory():
    global players

    if players[0].points > players[1].points:
        players[0].win = True
    elif players[0].points < players[1].points:
        players[1].win = True
    else:
        players[0].win = True
        players[0].loose = True
        players[1].win = True
        players[1].loose = True



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
    global turn, players, board, two_clicks, pair_correct, is_board_randomized, count_burnt, end_game
    count_up = 0
    list_up = []
    for card in board.cards_in_rand_location:
        lock.acquire()
        is_board_randomized = False
        lock.release()
        if card.is_face_up and not card.burnt:
            count_up += 1
            list_up.append(card)

        if count_up == 2:
            print("two clicks: " + str(two_clicks))
            if list_up[0].title == list_up[1].title:
                lock.acquire()
                pair_correct = True
                print("pair correct")
                players[turn].points += 1
                count_burnt += 2
                list_up[1].burnt = True
                list_up[0].burnt = True
                lock.release()

            else:
                lock.acquire()
                list_up[0].is_face_up = False
                list_up[1].is_face_up = False
                lock.release()

            if count_burnt == board.level.pile_size:

                # if board.level.level != 2:  # if current level is not equal to final level
                #     lock.acquire()
                #     end_level = True
                #     lock.release()
                # else:
                #     lock.acquire()
                #     end_game = True
                #     lock.release()
                lock.acquire()
                end_game = True
                # is_board_randomized = True
                lock.release()
            else:
                lock.acquire()
                is_board_randomized = True
                print("no enough burnt:" + str(count_burnt))
                lock.release()
            break


def handle_msg(command: bytes, msg: bytes):
    """function handles messages from client """
    global ready_to_start, board, protocol, update, lock

    if command == protocol.get_board_command():
        lock.acquire()
        update = True
        lock.release()
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
    global players, end_game, ready_to_start, board, level, update
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

    check_victory()

    while not players[0].disconnected and not players[1].disconnected:
        continue

    for t in threads:
        t.join()
    server_socket.close()


if __name__ == "__main__":
    main()
