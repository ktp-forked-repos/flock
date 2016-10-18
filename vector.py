# Author: Kiran Tomlinson
# Version: 1.1

import math


# This class defines a mathematical vector
class Vector:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)

    def scale(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def normalize(self):
        return Vector(self.x / self.get_magnitude(), self.y / self.get_magnitude())
