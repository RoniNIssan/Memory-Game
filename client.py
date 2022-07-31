import socket
import threading
import time

import pygame
import moviepy.editor
import pickle
import protocol_file
import elements

protocol = protocol_file.Protocol()
username = ""
port = ""
ip = 0

# booleans
end_game = False
switch_turns = False
click_on_card = False
got_update = False
ready_to_connect = False
ready_to_start = False
connected = False
my_turn = False
change_level = False
points = 0

board = elements.Board(1, "animals")
lock = threading.Lock()


def handle_graphics():
    global ready_to_connect
    global port
    global ip
    global username

    # define screen size
    WINDOW_SIZE = (854, 480)
    clock = pygame.time.Clock()
    clock.tick(25)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # caption and icon
    pygame.display.set_caption("Memory Game")
    # icon = pygame.image.load()
    # pygame.display.set_icon(icon)
    running = True

    while running:
        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # TODO: uncomment show_intro_screen + delete global ip, port, username
        # show_intro_screen(screen)
        port = 3339
        ip = "127.0.0.1"
        username = "bob"
        ready_to_connect = True

        show_waiting_screen(screen)
        print("showed intro")
        handle_gameplay_graphics(screen)


def show_intro_screen(screen):
    global username, port, ip
    intro_screen = pygame.image.load(r"data\screens\intro_screen.jpg")
    screen.blit(intro_screen, (0, 0))

    # intro screen rect
    username_rect = pygame.Rect(327, 153, 196, 34)
    port_rect = pygame.Rect(327, 252, 196, 34)
    ip_rect = pygame.Rect(327, 354, 196, 34)
    play_rect = pygame.Rect(339, 431, 176, 39)

    # user input
    writing_username = False
    writing_port = False
    writing_ip = False
    username = ""
    port = ""
    ip = ""

    # type - in user font
    base_font = pygame.font.Font(None, 25)

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    writing_username = True
                    writing_port = False
                    writing_ip = False
                if port_rect.collidepoint(event.pos):
                    writing_port = True
                    writing_ip = False
                    writing_username = False
                if ip_rect.collidepoint(event.pos):
                    writing_ip = True
                    writing_username = False
                    writing_port = False
                if play_rect.collidepoint(event.pos):
                    # all other variables were changed during loop
                    port = int(port)
                    return

            if event.type == pygame.KEYDOWN:
                if writing_username:
                    # TODO: everytime when writing - reset rect color to original and rewrite (sort of erasing)
                    username = keyboard_input(event, username)
                    username_text_surface = base_font.render(username, True, (255, 255, 255))
                    screen.blit(username_text_surface, (username_rect.x + 5, username_rect.y + 5))
                    print("username:" + username)
                elif writing_port:
                    port = keyboard_input(event, port)
                    port_text_surface = base_font.render(port, True, (255, 255, 255))
                    screen.blit(port_text_surface, (port_rect.x + 5, port_rect.y + 5))
                    print("port:" + port)
                elif writing_ip:
                    ip = keyboard_input(event, ip)
                    ip_text_surface = base_font.render(ip, True, (255, 255, 255))
                    screen.blit(ip_text_surface, (ip_rect.x + 5, ip_rect.y + 5))
                    print("ip:" + ip)

                pygame.display.flip()


def show_waiting_screen(screen):
    global ready_to_start
    waiting_screen_vid = moviepy.editor.VideoFileClip(r"data\screens\waiting_screen.mp4")

    print("start vid")
    while not ready_to_start:
        waiting_screen_vid.preview()

    print("ready to start")


def display_board(screen):
    global board, points
    print("current level " + str(board.level.level))
    base_screen = pygame.image.load(rf"data\screens\level_{board.level.level}.jpg")
    screen.blit(base_screen, (0, 0))
    pygame.display.update()

    font = pygame.font.Font(r"data\fonts\Heebo-Black.ttf", 32)
    text = font.render(f'points: {points}', True, (255, 255, 255))
    screen.blit(text, board.POINT_POS[board.level.level])

    i = 0
    for card in board.cards_in_rand_location:
        if card.is_face_up or card.burnt:
            card_image = pygame.image.load(
                        rf"data\screens\{board.category}\{card.title}.png")
            screen.blit(card_image, (board.level.LEVEL_LOCATIONS[i + 1].x, board.level.LEVEL_LOCATIONS[i + 1].y))
            pygame.display.update()
        i += 1


def handle_gameplay_graphics(screen):
    global board, click_on_card, got_update, switch_turns, end_game, change_level, ready_to_start
    print("handle graph")
    display_board(screen)

    while not end_game:
        if my_turn:
            turn_image = pygame.image.load(
                rf"data\screens\my_turn.png")
            screen.blit(turn_image, (board.TITLE_POS[board.level.level].x, board.TITLE_POS[board.level.level].y))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for i in range(len(board.level.LEVEL_LOCATIONS)):
                        if board.level.LEVEL_LOCATIONS[i + 1].collidepoint(event.pos) and\
                                not board.cards_in_rand_location[i].burnt and\
                                not board.cards_in_rand_location[i].is_face_up:
                            lock.acquire()
                            click_on_card = True
                            lock.release()
                            board.cards_in_rand_location[i].is_face_up = True
                            display_board(screen)
                            break

        else:
            turn_image = pygame.image.load(
                rf"data\screens\others_turn.png")
            screen.blit(turn_image, (board.TITLE_POS[board.level.level].x, board.TITLE_POS[board.level.level].y))
            pygame.display.update()

            pygame.event.get()

            lock.acquire()
            if got_update:
                display_board(screen)
                got_update = False
            lock.release()

        if switch_turns:
            print("switched turns")
            display_board(screen)

        if change_level:
            print("change level")
            # TODO: show announcement of new level
            while not ready_to_start:
                continue
            # display_board(screen)
            change_level = False


def keyboard_input(event, user_text):
    if event.key == pygame.K_BACKSPACE:
        user_text = user_text[:-1]
    else:
        user_text += event.unicode
    return user_text


def handle_msg(command: bytes, msg: bytes):
    global username, connected, ready_to_start, board, protocol, my_turn, got_update, lock, switch_turns, points, change_level

    if command == protocol.get_welcome_command():
        if protocol.analyze_message(msg) == 'successful':
            connected = True

    elif command == protocol.get_wait_command():
        protocol.analyze_message(msg)
        # print(protocol.analyze_message(msg))
        # ready_to_start = False

    elif command == protocol.get_ready_command():
        protocol.analyze_message(msg)
        # print(protocol.analyze_message(msg))
        ready_to_start = True

    elif command == protocol.get_board_command():
        board = protocol_file.unpack(protocol.analyze_message(msg))
        print(f"client {username} got board from server.")
        lock.acquire()
        got_update = True
        lock.release()

        if change_level:
            ready_to_start = True

    elif command == protocol.get_my_turn_command():
        lock.acquire()
        print(protocol.analyze_message(msg))
        my_turn = True
        lock.release()

    elif command == protocol.get_other_turn_command():
        lock.acquire()
        print(protocol.analyze_message(msg))
        my_turn = False
        lock.release()

    elif command == protocol.get_correct_command():
        print(protocol.analyze_message(msg))
        lock.acquire()
        switch_turns = True
        lock.release()
        points += 2

    elif command == protocol.get_correct_command():
        print(protocol.analyze_message(msg))
        lock.acquire()
        switch_turns = True
        lock.release()

    elif command == protocol.get_next_level_command():
        print(protocol.analyze_message(msg))
        lock.acquire()
        change_level = True
        lock.release()


def received_messages(data_bytes: bytes, sock: socket.socket):
    global protocol
    if data_bytes != b'':
        data_bytes = protocol.separate_messages(data_bytes)

        for message in data_bytes:
            try:
                handle_msg(message[:4], message)
            except:
                return


def handle_communication(sock: socket.socket):
    try:
        msg = sock.recv(4096)
        received_messages(msg, sock)
    except:
        print("skip receiving")
        return


def handle_game(sock: socket.socket):
    global my_turn, board, switch_turns, change_level

    # TODO: handle next level
    while True:
        print("reset")

        while my_turn and not switch_turns:
            check_for_board_updates(sock)

        while not my_turn and not switch_turns:
            print("is my turns: " + str(my_turn))
            handle_communication(sock)

        if switch_turns:
            switch_turns = False
            handle_communication(sock)  # turn command

        if change_level:
            print("out of handle game")
            break


def check_for_board_updates(sock: socket.socket):
    global click_on_card, board

    if click_on_card:
        to_send = protocol.build_message(protocol.get_board_command(), protocol_file.pack(board))
        protocol.send_message(to_send, sock)
        print("sent board")
        click_on_card = False
        time.sleep(0.4)
        handle_communication(sock)
    else:
        # print("no click")
        pass


def main():
    global ready_to_connect, port, ip, connected, ready_to_start, change_level

    graphics = threading.Thread(target=handle_graphics)
    graphics.start()
    user_sock = socket.socket()

    while True:
        if ready_to_connect:
            user_sock.connect((ip, port))
            handle_communication(user_sock) # welcome message

            if connected:
                break
        else:
            continue

    while not ready_to_start:
        handle_communication(user_sock) # wait or ready message

    while not end_game:
        handle_communication(user_sock)  # board command

        to_send = protocol.build_message(protocol.get_wait_command(), b'got board. waiting for turn command')
        protocol.send_message(to_send, user_sock)

        handle_communication(user_sock)  # turn command
        handle_game(user_sock)
        ready_to_start = False


if __name__ == "__main__":
    main()
