import math

import numpy as np


# we are trying to make the code more module with this class so that we can support
class Object3d:
    def __init__(
        self, vertices, triangles, position=(0, 0, 0), rotation=(0, 0, 0), scale=1.0
    ) -> None:
        self.base_vertices = np.array(vertices, dtype=float)
        self.triangles = list(triangles)
        self.position = np.array(position, dtype=float)
        self.rotation = tuple(rotation)
        self.scale = float(scale)

    def transformed_vertices(self):
        s = self.scale
        rx, ry, rz = map(math.radians, self.rotation)

        # rotated points
        sx = math.sin(rx)
        cx = math.cos(rx)
        sy = math.sin(ry)
        cy = math.cos(ry)
        sz = math.sin(rz)
        cz = math.cos(rz)

        rx_m = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        ry_m = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        rz_m = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

        # final rotation matrices
        rot = rx_m.dot(ry_m).dot(rz_m)

        verts = []

        for v in self.base_vertices * s:
            w = rot.dot(v) + self.position
            verts.append(w)

        return np.array(verts)

    def camera_space_points(self, camera_position, camera_angle):
        cam_pos = np.array(camera_position, dtype=float)

        verts = self.transformed_vertices()

        rx = math.radians(camera_angle[0])
        ry = math.radians(camera_angle[1])
        rz = math.radians(camera_angle[2])

        rx_m = np.array(
            [
                [1, 0, 0],
                [0, math.cos(rx), -math.sin(rx)],
                [0, math.sin(rx), math.cos(rx)],
            ]
        )
        ry_m = np.array(
            [
                [math.cos(ry), 0, math.sin(ry)],
                [0, 1, 0],
                [-math.sin(ry), 0, math.cos(ry)],
            ]
        )
        rz_m = np.array(
            [
                [math.cos(rz), -math.sin(rz), 0],
                [math.sin(rz), math.cos(rz), 0],
                [0, 0, 1],
            ]
        )

        cam_rot = rx_m.dot(ry_m).dot(rz_m)

        cam_points = []

        for v in verts:
            p = v - cam_pos
            # dot the rotation matrix with the points
            cam_points.append(cam_rot.dot(p))

        return cam_points

    # added: axis-aligned bounding box for simple collisions
    def get_aabb(self):
        verts = self.transformed_vertices()
        mn = verts.min(axis=0)
        mx = verts.max(axis=0)
        return tuple(mn), tuple(mx)
