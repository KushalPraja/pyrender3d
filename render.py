import numpy as np
import pygame as pg


def aabb_intersect(a_min, a_max, b_min, b_max):
    for i in range(3):
        if a_max[i] < b_min[i] or a_min[i] > b_max[i]:
            return False
    return True


def _project_point(point, width, height, distance_from_camera, fov):
    x, y, z = point[0], point[1], point[2]
    if z <= 0.1:  # avoid divide by zero
        z = 0.1
    scale = (distance_from_camera / z) * (fov / 90)
    screen_x = int(width / 2 + x * scale)
    screen_y = int(height / 2 - y * scale)
    return (screen_x, screen_y, z)


def fill_triangle(screen, p1, p2, p3, color=(100, 100, 255)):
    x1, y1, _ = p1
    x2, y2, _ = p2
    x3, y3, _ = p3
    pg.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3)], 0)


class Scene:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def check_collisions(self):
        hits = []
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                a_min, a_max = self.objects[i].get_aabb()
                b_min, b_max = self.objects[j].get_aabb()
                if aabb_intersect(a_min, a_max, b_min, b_max):
                    hits.append((self.objects[i], self.objects[j]))
        return hits

    def render(
        self,
        screen,
        camera,
        width,
        height,
        show_wireframe=True,
        distance_from_camera=400,
        fov=45,
        near_clip=5,
        max_distance=200,
    ):
        draw_list = []
        cam_pos = np.array(camera.position, dtype=float)

        for obj in self.objects:
            # Distance cull - skip far objects EARLY
            obj_pos = obj.position
            dist_sq = (
                (obj_pos[0] - cam_pos[0]) ** 2
                + (obj_pos[1] - cam_pos[1]) ** 2
                + (obj_pos[2] - cam_pos[2]) ** 2
            )
            if dist_sq > max_distance * max_distance:
                continue

            cam_points = obj.camera_space_points(camera.position, camera.angle)

            for tri in obj.triangles:
                p1 = cam_points[tri[0]]
                p2 = cam_points[tri[1]]
                p3 = cam_points[tri[2]]

                # Near plane cull - skip if any vertex too close
                if p1[2] <= near_clip or p2[2] <= near_clip or p3[2] <= near_clip:
                    continue

                # Back-face culling using cross product
                # Edge vectors
                v1_x = p2[0] - p1[0]
                v1_y = p2[1] - p1[1]
                v1_z = p2[2] - p1[2]

                v2_x = p3[0] - p1[0]
                v2_y = p3[1] - p1[1]
                v2_z = p3[2] - p1[2]

                # Normal (cross product)
                nx = v1_y * v2_z - v1_z * v2_y
                ny = v1_z * v2_x - v1_x * v2_z
                nz = v1_x * v2_y - v1_y * v2_x

                # View direction (to camera at origin in camera space)
                # Use first point as reference
                if nx * p1[0] + ny * p1[1] + nz * p1[2] >= 0:
                    # Triangle facing away
                    continue

                proj1 = _project_point(p1, width, height, distance_from_camera, fov)
                proj2 = _project_point(p2, width, height, distance_from_camera, fov)
                proj3 = _project_point(p3, width, height, distance_from_camera, fov)

                depth = (proj1[2] + proj2[2] + proj3[2]) / 3.0
                draw_list.append((depth, proj1, proj2, proj3, show_wireframe))

        # Painter's algorithm: draw far -> near
        draw_list.sort(key=lambda x: -x[0])

        for _, p1, p2, p3, wire in draw_list:
            if wire:
                pg.draw.line(screen, (255, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]), 1)
                pg.draw.line(screen, (255, 255, 255), (p2[0], p2[1]), (p3[0], p3[1]), 1)
                pg.draw.line(screen, (255, 255, 255), (p3[0], p3[1]), (p1[0], p1[1]), 1)
            else:
                fill_triangle(screen, p1, p2, p3)
