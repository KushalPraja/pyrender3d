import numpy as np
import pygame as pg
import math
import config

class Cube:
    def __init__(self, size=50):
        s = size
        self.vertices = np.array([
            [-s, -s, -s],
            [ s, -s, -s],
            [ s,  s, -s],
            [-s,  s, -s],
            [-s, -s,  s],
            [ s, -s,  s],
            [ s,  s,  s],
            [-s,  s,  s],
        ], dtype=float)

        self.triangles = [
            (0, 1, 2), (0, 2, 3),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (1, 2, 6), (1, 6, 5),
            (0, 3, 7), (0, 7, 4)
        ]

    # converts world space points to camera space points
    def camera_space_points(self, camera_position, camera_angle):
        # Build rotation matrices
        rx = np.array([
            [1, 0, 0],
            [0, math.cos(math.radians(camera_angle[0])), -math.sin(math.radians(camera_angle[0]))],
            [0, math.sin(math.radians(camera_angle[0])), math.cos(math.radians(camera_angle[0]))]
        ])

        ry = np.array([
            [math.cos(math.radians(camera_angle[1])), 0, math.sin(math.radians(camera_angle[1]))],
            [0, 1, 0],
            [-math.sin(math.radians(camera_angle[1])), 0, math.cos(math.radians(camera_angle[1]))]
        ])

        rz = np.array([
            [math.cos(math.radians(camera_angle[2])), -math.sin(math.radians(camera_angle[2])), 0],
            [math.sin(math.radians(camera_angle[2])), math.cos(math.radians(camera_angle[2])), 0],
            [0, 0, 1]
        ])

        rotation = rx.dot(ry).dot(rz)

        cam_points = []
        for v in self.vertices:
            x = v[0] - camera_position[0]
            y = v[1] - camera_position[1]
            z = v[2] - camera_position[2]
            p = np.array([x, y, z], dtype=float)
            rotated = rotation.dot(p)
            cam_points.append(rotated)

        return cam_points

# takes camera_space points and projects it to 2D screen coordinates
def _project_point(point, width, height, distance_from_camera, fov):
    x, y, z = point[0], point[1], point[2]
    if z == 0:
        z = 0.0001
    x_proj = x * (distance_from_camera / z) * (fov / 90)
    y_proj = y * (distance_from_camera / z) * (fov / 90)
    screen_x = int(width / 2 + x_proj)
    screen_y = int(height / 2 - y_proj)
    return (screen_x, screen_y, z)

# fills triangles between projected points
def render_frame(screen, cube_obj, camera, width, height, show_wireframe=True,
                 distance_from_camera=400, fov=45, near_clip=10):
    
    cam_pos = camera.position
    cam_angle = camera.angle
    cam_points = cube_obj.camera_space_points(cam_pos, cam_angle)

    for v1, v2, v3 in cube_obj.triangles:
        p1 = cam_points[v1]
        p2 = cam_points[v2]
        p3 = cam_points[v3]

        if p1[2] <= near_clip or p2[2] <= near_clip or p3[2] <= near_clip:
            continue

        proj1 = _project_point(p1, width, height, distance_from_camera, fov)
        proj2 = _project_point(p2, width, height, distance_from_camera, fov)
        proj3 = _project_point(p3, width, height, distance_from_camera, fov)

        x1, y1, z1 = proj1
        x2, y2, z2 = proj2
        x3, y3, z3 = proj3

        if show_wireframe:
            pg.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))
            pg.draw.line(screen, (255, 255, 255), (x2, y2), (x3, y3))
            pg.draw.line(screen, (255, 255, 255), (x3, y3), (x1, y1))
        else:
            fill_triangle(screen, proj1, proj2, proj3, width, height)


def fill_triangle(screen, p1, p2, p3, width, height):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    if min(y1, y2, y3) > height - 1 or max(y1, y2, y3) < 0:
        return
    if min(x1, x2, x3) > width - 1 or max(x1, x2, x3) < 0:
        return

    pg.draw.polygon(screen, (100, 100, 255), [(x1, y1), (x2, y2), (x3, y3)], 0)

