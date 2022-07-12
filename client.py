import socket
import threading
import pygame
import moviepy.editor

username = ""
port = ""
ip = 0

# booleans
ready_to_connect = False
ready_to_start = False
connected = False


def handle_graphics():
    global ready_to_connect

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
        show_intro_screen(screen)
        ready_to_connect = True
        show_waiting_screen(screen)


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
                    print("lets begin")
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

    while not ready_to_start:
        waiting_screen_vid.preview()

def keyboard_input(event, user_text):
    if event.key == pygame.K_BACKSPACE:
        user_text = user_text[:-1]
    else:
        user_text += event.unicode
    return user_text


def handle_msg(code, msg):
    global connected, ready_to_start
    if code == 'WLCM':
        print(msg)
        connected = True
    elif code == 'WAIT':
        # print(msg)
        ready_to_start = False
    elif code == 'RDEY':
        print(msg)
        ready_to_start = True


def analyze_msg(msg):
    all_msg = msg.split('$')
    for msg in all_msg:
        code = msg[:4]
        msg = all_msg[5:]
        handle_msg(code, msg)


def main():
    global ready_to_connect, port, ip, connected, ready_to_start

    graphics = threading.Thread(target=handle_graphics)
    graphics.start()
    user_sock = socket.socket()

    while True:
        if ready_to_connect:
            user_sock.connect((ip, port))
            msg = user_sock.recv(1024)
            if msg == b'':
                print("something went wrong. please try again.")
                break
            msg = msg.decode('UTF-8')
            analyze_msg(msg)
            if connected:
                break
        else:
            continue

    while not ready_to_start:
        msg = user_sock.recv(1024)
        if msg == b'':
            print("something went wrong. please try again.")
            break
        msg = msg.decode('UTF-8')
        analyze_msg(msg)

    print("ready to play")


if __name__ == "__main__":
    main()
