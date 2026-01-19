import pygame as pg
from camera import Camera
import config
from config import SCREEN_LENGTH, SCREEN_HEIGHT, FPS
from cube import Cube
from render import Scene


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    scene = Scene()
    # start with a small grid by default — increase when stable
    def create_cube_grid(rows, cols, cube_half_size=6, gap=2, y=0):
        spacing = cube_half_size * 2 + gap
        offset_x = (cols - 1) * spacing / 2.0
        offset_z = (rows - 1) * spacing / 2.0
        for rz in range(rows):
            for cx in range(cols):
                x = cx * spacing - offset_x
                z = rz * spacing - offset_z
                c = Cube(size=cube_half_size, position=(x, y, z))
                scene.add(c)

    # moderate default: 20x20 grid = 400 cubes
    create_cube_grid(20, 20, cube_half_size=6, gap=2, y=0)

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

        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if pg.mouse.get_focused():
            camera.rotate('yaw', -mouse_dx * 0.1)
            camera.rotate('pitch', -mouse_dy * 0.1)

        screen.fill((0, 0, 0))
        scene.render(screen, camera, SCREEN_LENGTH, SCREEN_HEIGHT, show_wireframe, max_distance=250)

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
