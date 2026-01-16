import math
import pygame as pg
import config

def render_cube(screen, camera_position, cube_width = 100):

    # screen
    width = config.SCREEN_LENGTH
    height = config.SCREEN_HEIGHT
    clock = pg.time.Clock()

    array_len = width * height
    
    # z buffer to keep track of closest pixel at each position
    zBuffer = [float('-inf')] * array_len

    # pixel buffer to store color of each pixel
    pixel_buffer = [(0, 0, 0)] * array_len

    distance_from_camera = 400
    fov = 45

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

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), # back face
        (4, 5), (5, 6), (6, 7), (7, 4), # front face
        (0, 4), (1, 5), (2, 6), (3, 7),  # connecting edges
        (0, 2), (3, 4), (5, 7), (1, 6), 
        (0, 5), (3, 6)
    ]

    while running:

        #  screen = pg.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
        # camera_position = [0, 0, -100]
    

        #  event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        if pg.key.get_pressed()[pg.K_SPACE]:
            camera_position[1] += 5

        if pg.key.get_pressed()[pg.K_w]:
            camera_position[2] += 5

        if pg.key.get_pressed()[pg.K_s]:
            camera_position[2] -= 5

        if pg.key.get_pressed()[pg.K_a]:
            camera_position[0] -= 5

        if pg.key.get_pressed()[pg.K_d]:
            camera_position[0] += 5


        screen.fill((0, 0, 0))
        # clear buffers 
        zBuffer = [float('-inf')] * array_len
        pixel_buffer = [(0, 0, 0)] * array_len
        
        # render the cube verticels

        projected_points = []

        for coord in range(len(cube)):
            
            # for any world point we have to translate it relative to camera position
            x = cube[coord][0] - camera_position[0]
            y = cube[coord][1] - camera_position[1]
            z = cube[coord][2] - camera_position[2]

            if z <= 0:
                z = 0.0001  # prevent division by zero or negative z values

            x_proj = x * (distance_from_camera / z) * (fov / 90)
            y_proj = y * (distance_from_camera / z) * (fov / 90)

            # since our screen origin is at top left corner we have to adjust the projected coordinates map them to the center
            x_proj = int(width / 2 + x_proj)
            y_proj = int(height / 2 - y_proj)

            projected_points.append((x_proj, y_proj, z))

        print(projected_points)
        # this idea is that we connected the projected points with lines
        for x, y in edges:
            # p1 would be point 0 and p2 would be point 1
            p1 = projected_points[x]
            p2 = projected_points[y]

            screen_x1, screen_y1, z1 = p1
            screen_x2, screen_y2, z2 = p2

            pg.draw.line(screen, (255, 255, 255), (screen_x1, screen_y1), (screen_x2, screen_y2))


        # if within the screen bounds update z buffer and pixel buffer
        index = y_proj * width + x_proj
        if 0 <= x_proj < width and 0 <= y_proj < height:
            if z > zBuffer[index]:
                zBuffer[index] = z
                pixel_buffer[index] = (255, 255, 255)  # white color for cube vertices

        fps = clock.get_fps()
        text_surface = pg.font.SysFont("Arial", 18).render(f"FPS: {int(fps)}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pg.display.flip()
        clock.tick(config.FPS)

    pg.quit()


        

        


