import pygame as pg


class Camera:
    def __init__(self):
        self.position = [0, 0, -200]
        self.angle = [0, 0, 0]
        self.direction_vector = [0, 0, 1]

    def move(self, direction, amount):
        if direction == 'up':
            self.position[1] += amount
        elif direction == 'down':
            self.position[1] -= amount
        elif direction == 'forward':
            self.position[2] += amount
        elif direction == 'backward':
            self.position[2] -= amount
        elif direction == 'left':
            self.position[0] -= amount
        elif direction == 'right':
            self.position[0] += amount

    def rotate(self, axis, amount):
        if axis == 'pitch':
            self.angle[0] += amount
        elif axis == 'yaw':
            self.angle[1] += amount
        elif axis == 'roll':
            self.angle[2] += amount

    
    def get_position(self):
        return self.position
    
    def get_angle(self):
        return self.angle
