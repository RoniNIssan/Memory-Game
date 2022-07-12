import pygame
from pyvidplayer import Video
import moviepy.editor

def main():
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(25)
    WINDOW_SIZE = (854, 480)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    VIDEO_SIZE = (854, 480)
    waiting_screen_vid = moviepy.editor.VideoFileClip(r"data\screens\waiting_screen.mp4")
    while True:
        waiting_screen_vid.preview()
if __name__ == '__main__':
    main()