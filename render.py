import math
import pygame as pg
import config

def render_cube(screen, camera_position, cube_width = 100):


    # screen
    width = config.SCREEN_LENGTH
    height = config.SCREEN_HEIGHT
    clock = pg.time.Clock()

    #

    array_len = width * height

    # z buffer to keep track of closest pixel at each position
    zBuffer = [float('-inf')] * array_len

    # pixel buffer to store color of each pixel
    pixel_buffer = [(0, 0, 0)] * array_len

    distance_from_camera = 300 
    fov = 90

    running = True
    
    cube = [
        [-cube_width, -cube_width, -cube_width],
        [ cube_width, -cube_width, -cube_width],
        [ cube_width,  cube_width, -cube_width],
        [-cube_width,  cube_width, -cube_width],
        [-cube_width, -cube_width,  cube_width],
        [ cube_width, -cube_width,  cube_width],
        [ cube_width,  cube_width,  cube_width],
        [-cube_width,  cube_width,  cube_width],
    ]

    while running:

        #  event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        if pg.key.get_pressed()[pg.K_SPACE]:
            print("space pressed")
            running = False

        if pg.key.get_pressed()[pg.K_w]:
            camera_position[2] += 10
        if pg.key.get_pressed()[pg.K_s]:
            camera_position[2] -= 10
        if pg.key.get_pressed()[pg.K_a]:
            camera_position[0] -= 10
        if pg.key.get_pressed()[pg.K_d]:
            camera_position[0] += 10

        # clear buffers 
        zBuffer = [float('-inf')] * array_len
        pixel_buffer = [(0, 0, 0)] * array_len
        screen.fill((0, 0, 0))


        pg.display.flip()
        clock.tick(config.FPS)

    pg.quit()

        

        


