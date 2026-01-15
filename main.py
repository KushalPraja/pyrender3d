import pygame as pg
from config import SCREEN_LENGTH, SCREEN_HEIGHT, FPS
import pygame.gfxdraw as gfxdraw
from render import render_cube


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))

    # 100 units back on z-axis
    camera_position = [0, 0, -100]
    render_cube(screen, camera_position)

if __name__ == "__main__":
    main()
