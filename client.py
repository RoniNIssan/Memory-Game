import socket
import threading
import pygame

username = ""
port = ""
ip = 0

# booleans
ready_to_start = False


def handle_graphics():
    global ready_to_start


    # define screen size
    WINDOW_SIZE = (854, 480)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # caption and icon
    pygame.display.set_caption("Memory Game")
    # icon = pygame.image.load()
    # pygame.display.set_icon(icon)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        show_intro_screen(screen)
        ready_to_start = True
        print("ready to play")
        pygame.display.update()


def show_intro_screen(screen):
    global username, port, ip
    print("here")
    intro_screen = pygame.image.load(r"data\screens\intro_screen.jpg")
    screen.blit(intro_screen, (0, 0))

    # intro screen rect
    username_rect = pygame.Rect(327, 153, 196, 34)
    port_rect = pygame.Rect(327, 252, 196, 34)
    ip_rect = pygame.Rect(327, 354, 196, 34)
    play_rect = pygame.Rect(339, 431, 176, 39)

    # type - in user font
    base_font = pygame.font.Font(None, 16)
    user_text = ""
    color = pygame.Color("White")

    # user input
    writing_username = False
    writing_port = False
    writing_ip = False
    username = ""
    port = ""
    ip = ""

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("pressed")
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
                print("key")
                if writing_username:
                    username += keyboard_input(event)
                    print("username:" + username)
                elif writing_port:
                    port += keyboard_input(event)
                    print("port:" + port)
                elif writing_ip:
                    ip += keyboard_input(event)
                    print("ip:" + ip)


def keyboard_input(event):
    user_text = ""
    if event.key == pygame.K_BACKSPACE:

        # get text input from 0 to -1 i.e. end.
        user_text = user_text[:-1]

    # Unicode standard is used for string
    # formation
    else:
        user_text += event.unicode
    return user_text


def main():
    global ready_to_start, port, ip

    graphics = threading.Thread(target=handle_graphics)
    graphics.start()

    while True:
        if ready_to_start:
            user_sock = socket.socket()
            user_sock.connect((ip, port))
            print("connected")
        else:
            continue



if __name__ == "__main__":
    main()
