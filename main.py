import pygame as pg
from camera import Camera
import config
from config import SCREEN_LENGTH, SCREEN_HEIGHT, FPS
from cube import Cube, render_frame


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    cube = Cube()
    camera = Camera()

    show_wireframe = True
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            camera.move('up', 5)

        if keys[pg.K_LSHIFT]:
            camera.move('down', 5)

        if keys[pg.K_w]:
            camera.move('forward', 5)

        if keys[pg.K_s]:
            camera.move('backward', 5)

        if keys[pg.K_a]:
            camera.move('left', 5)

        if keys[pg.K_d]:
            camera.move('right', 5)

        if keys[pg.K_ESCAPE]:
            running = False

        if keys[pg.K_TAB]:
            show_wireframe = not show_wireframe
            pg.time.delay(200)

        if keys[pg.K_LEFT]:
            camera.rotate('yaw', 2)

        if keys[pg.K_RIGHT]:
            camera.rotate('yaw', -2)

        if keys[pg.K_UP]:
            camera.rotate('pitch', 2)

        if keys[pg.K_DOWN]:
            camera.rotate('pitch', -2)

        screen.fill((0, 0, 0))
        render_frame(screen, cube, camera, SCREEN_LENGTH, SCREEN_HEIGHT, show_wireframe)

        fps = int(clock.get_fps())
        text_surface = pg.font.SysFont("Arial", 18).render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        text_surface = pg.font.SysFont("Arial", 18).render(f"Camera Pos: {camera.position}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 30))
        text_surface = pg.font.SysFont("Arial", 18).render(f"Camera Angle: {camera.angle}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 50))
        # get forward vector
        text_surface = pg.font.SysFont("Arial", 18).render(f"Forward Vector: {camera.get_forward_vector()}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 70))

        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
