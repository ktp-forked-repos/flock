import random

from Vector import Vector

RADIUS = 500


# This class defines a bird, which is a member of a flock
class Bird:
    circle_avoid_strength = 2
    position = Vector(0, 0)
    velocity = Vector(0, 0)
    color = ()
    speed_limit = 5

    def __init__(self, position, velocity, color):
        self.position = position
        self.velocity = velocity
        self.color = color

    def update_velocity(self):
        circle_vector = get_vector_to_circle(self.position, RADIUS)
        if circle_vector is not None:
            r = circle_vector.get_magnitude()
            circle_avoid = circle_vector.scale(-1 * self.circle_avoid_strength / (r * r))

            if point_in_circle(self.position, RADIUS):
                self.velocity = self.velocity.add(circle_avoid)
            else:
                self.velocity = self.velocity.subtract(circle_avoid)

        self.velocity = self.velocity.add(Vector(random.random() / 10 - 0.05, random.random() / 10 - 0.05))

        # Enforce speed limit
        speed = self.velocity.get_magnitude()
        if speed > self.speed_limit:
            self.velocity = self.velocity.scale(self.speed_limit / speed)

    def move(self):
        self.update_velocity()
        self.position = self.position.add(self.velocity)


# Returns true if the Vector point is in circle of radius, else false
def point_in_circle(point, radius):
    dx = abs(point.x - radius)
    dy = abs(point.y - radius)

    if dx + dy < radius:
        return True

    if dx > radius:
        return False

    if dy > radius:
        return False

    if dx * dx + dy * dy > radius * radius:
        return False
    else:
        return True


# Given a point in a circle, return a vector to the closest point on the circle
# to the given point.
def get_vector_to_circle(position, radius):
    center = Vector(radius, radius)
    diff = position.subtract(center)

    if diff.get_magnitude() == 0:
        return None

    return center.add(diff.scale(radius / diff.get_magnitude())).subtract(position)
