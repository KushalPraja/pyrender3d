from object3d import Object3d


class Cube(Object3d):
    def __init__(self, size=50, position=(0, 0, 0), rotation=(0, 0, 0), scale=1.0):
        s = size
        vertices = [
            [-s, -s, -s],
            [s, -s, -s],
            [s, s, -s],
            [-s, s, -s],
            [-s, -s, s],
            [s, -s, s],
            [s, s, s],
            [-s, s, s],
        ]

        triangles = [
            (0, 1, 2),
            (0, 2, 3),
            (4, 5, 6),
            (4, 6, 7),
            (0, 1, 5),
            (0, 5, 4),
            (2, 3, 7),
            (2, 7, 6),
            (1, 2, 6),
            (1, 6, 5),
            (0, 3, 7),
            (0, 7, 4),
        ]

        super().__init__(
            vertices, triangles, position=position, rotation=rotation, scale=scale
        )
