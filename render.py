import math
import pygame as pg
import config
import numpy as np

def render_cube(screen, camera_position, cube_width = 100):

    # screen
    width = config.SCREEN_LENGTH
    height = config.SCREEN_HEIGHT
    clock = pg.time.Clock()

    array_len = width * height
    distance_from_camera = 400
    fov = 45
    near_clip = 10  # Near clipping plane

    camera_angle = np.array([0.0, 0.0, 0.0])  # x, y, z 
    running = True
    
    
    cube = np.array([
        [-cube_width/2, -cube_width/2, -cube_width/2],  # 0
        [ cube_width/2, -cube_width/2, -cube_width/2],  # 1
        [ cube_width/2,  cube_width/2, -cube_width/2],  # 2
        [-cube_width/2,  cube_width/2, -cube_width/2],  # 3
        [-cube_width/2, -cube_width/2,  cube_width/2],  # 4
        [ cube_width/2, -cube_width/2,  cube_width/2],  # 5
        [ cube_width/2,  cube_width/2,  cube_width/2],  # 6
        [-cube_width/2,  cube_width/2,  cube_width/2],  # 7
    ])

    triangles = np.array([
        (0, 1, 2), (0, 2, 3),  # back face
        (4, 5, 6), (4, 6, 7),  # front face
        (0, 1, 5), (0, 5, 4),  # bottom face
        (2, 3, 7), (2, 7, 6),  # top face
        (1, 2, 6), (1, 6, 5),  # right face
        (0, 3, 7), (0, 7, 4)   # left face
    ])

    show_wireframe: bool = True
    
    while running:
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

        if pg.key.get_pressed()[pg.K_ESCAPE]:
            running = False
        
        if pg.key.get_pressed()[pg.K_TAB]:
            show_wireframe = not show_wireframe
            pg.time.delay(200) 

        if pg.key.get_pressed()[pg.K_LEFT]:
            camera_angle[1] -= 2

        if pg.key.get_pressed()[pg.K_RIGHT]:
            camera_angle[1] += 2

        if pg.key.get_pressed()[pg.K_UP]:
            camera_angle[0] -= 2
        
        if pg.key.get_pressed()[pg.K_DOWN]:
            camera_angle[0] += 2

        screen.fill((0, 0, 0))
        
       
        # Transform vertices to camera space
        camera_space_points = []

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, math.cos(math.radians(camera_angle[0])), -math.sin(math.radians(camera_angle[0]))],
            [0, math.sin(math.radians(camera_angle[0])), math.cos(math.radians(camera_angle[0]))]
        ])

        rotation_y = np.matrix([
            [math.cos(math.radians(camera_angle[1])), 0, math.sin(math.radians(camera_angle[1]))],
            [0, 1, 0],
            [-math.sin(math.radians(camera_angle[1])), 0, math.cos(math.radians(camera_angle[1]))]
        ])

        rotation_z = np.matrix([
            [math.cos(math.radians(camera_angle[2])), -math.sin(math.radians(camera_angle[2])), 0],
            [math.sin(math.radians(camera_angle[2])), math.cos(math.radians(camera_angle[2])), 0],
            [0, 0, 1]
        ])

        rotation_matrix = rotation_x * rotation_y * rotation_z

        for coord in range(len(cube)):

            # right-handed coordinate system
            x = cube[coord][0] - camera_position[0] 
            y = cube[coord][1] - camera_position[1]
            z = cube[coord][2] - camera_position[2] 

            point = np.matrix([[x, y, z]])
            final_point = point * rotation_matrix
            camera_space_points.append(final_point)
        
        # Process each triangle
        for v1, v2, v3 in triangles:
            p1 = camera_space_points[v1]
            p2 = camera_space_points[v2]
            p3 = camera_space_points[v3]
            
            if p1[0, 2] <= near_clip or p2[0, 2] <= near_clip or p3[0, 2] <= near_clip:
                continue  
            
            projected = []
            for point in [p1, p2, p3]:
                x, y, z = point[0, 0], point[0, 1], point[0, 2]
                x_proj = x * (distance_from_camera / z) * (fov / 90)
                y_proj = y * (distance_from_camera / z) * (fov / 90)

                # Convert to screen coordinates
                x_proj = int(width / 2 + x_proj)
                y_proj = int(height / 2 - y_proj)
                projected.append((x_proj, y_proj, z))

            
            # Extract projected points
            proj_p1, proj_p2, proj_p3 = projected
            x1, y1, z1 = proj_p1
            x2, y2, z2 = proj_p2
            x3, y3, z3 = proj_p3

            # Draw lines
            if show_wireframe:
                pg.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))
                pg.draw.line(screen, (255, 255, 255), (x2, y2), (x3, y3))
                pg.draw.line(screen, (255, 255, 255), (x3, y3), (x1, y1))
            
            # Fill triangle based on depth
            else: 
                fill_triangle(screen, proj_p1, proj_p2, proj_p3, width, height)

        fps = clock.get_fps()
        text_surface = pg.font.SysFont("Arial", 18).render(f"FPS: {int(fps)}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pg.display.flip()
        clock.tick(config.FPS)

    pg.quit()


# barycentric triangle fill algorithm
def fill_triangle(screen, p1, p2, p3, width, height):
    x1, y1, z1 = p1 # point 1 in triangle
    x2, y2, z2 = p2 # point 2 in triangle
    x3, y3, z3 = p3 # point 3 in triangle

    if min(y1, y2, y3) > height - 1 or max(y1, y2, y3) < 0:
        return  # Triangle is completely outside vertical bounds

    if min(x1, x2, x3) > width - 1 or max(x1, x2, x3) < 0:
        return  # Triangle is completely outside horizontal bounds
    
    pg.draw.polygon(screen, (100, 100, 255), [(x1, y1), (x2, y2), (x3, y3)], 0)
