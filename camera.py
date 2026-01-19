import math


class Camera:
    def __init__(self):
        self.position = [0, 0, -200]
        self.angle = [0, 0, 0]
        self.forward_vector = [0, 0, 1]

    # movement controller (world space)
    def move(self, direction, amount):
        directions = self.get_forward_vector()
        directions_left_right = self.get_right_vector()
        if direction == "up":
            self.position[1] += amount
        elif direction == "down":
            self.position[1] -= amount
        elif direction == "forward":
            self.position[2] += directions[2] * amount
            self.position[0] -= directions[0] * amount
        elif direction == "backward":
            self.position[2] -= directions[2] * amount
            self.position[0] += directions[0] * amount
        elif direction == "left":
            self.position[0] -= directions_left_right[0] * amount
            self.position[2] += directions_left_right[2] * amount
        elif direction == "right":
            self.position[0] += directions_left_right[0] * amount
            self.position[2] -= directions_left_right[2] * amount

    def rotate(self, axis, amount):
        if axis == "pitch":
            if self.angle[0] + amount > 90:
                self.angle[0] = 90
            elif self.angle[0] + amount < -90:
                self.angle[0] = -90
            else:
                self.angle[0] += amount
        elif axis == "yaw":
            if self.angle[1] + amount > 360:
                self.angle[1] = 0
            elif self.angle[1] + amount < 0:
                self.angle[1] = 360
            else:
                self.angle[1] += amount
        elif axis == "roll":
            if self.angle[2] + amount > 360:
                self.angle[2] = 0
            elif self.angle[2] + amount < 0:
                self.angle[2] = 360
            else:
                self.angle[2] += amount

    def get_forward_vector(self):
        pitch_rad = math.radians(self.angle[0])
        yaw_rad = math.radians(self.angle[1])

        x = math.cos(pitch_rad) * math.sin(yaw_rad)
        y = math.sin(pitch_rad)
        z = math.cos(pitch_rad) * math.cos(yaw_rad)

        length = math.sqrt(x**2 + y**2 + z**2)
        if length == 0:
            return [0, 0, 0]
        return [x / length, y / length, z / length]

    def get_right_vector(self):
        pitch = math.radians(self.angle[0])
        yaw = math.radians(self.angle[1] + 90)

        x = math.cos(pitch) * math.sin(yaw)
        y = 0
        z = math.cos(pitch) * math.cos(yaw)
        length = math.sqrt(x**2 + y**2 + z**2)
        if length == 0:
            return [0, 0, 0]
        return [x / length, y / length, z / length]
