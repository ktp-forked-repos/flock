import random

from Vector import Vector

RADIUS = 500


# This class defines a bird, which is a member of a flock
class Bird:
    position = Vector(0, 0)
    velocity = Vector(random.random() - 0.5, random.random() - 0.5)
    color = ()

    speed_limit = 5
    detection_radius = 100
    circle_avoid_strength = 20
    bird_avoid_strength = 10

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Update this bird's velocity
    def update_velocity(self, flock):

        # Random movement
        # self.velocity = self.velocity.add(Vector(random.random() / 10 - 0.05, random.random() / 10 - 0.05))

        # Circle avoidance
        circle_vector = get_vector_to_circle(self.position, RADIUS)
        if circle_vector is not None:
            r = circle_vector.get_magnitude()
            circle_avoid = circle_vector.scale(-1 * self.circle_avoid_strength / (r * r))

            if point_in_circle(self.position, RADIUS):
                self.velocity = self.velocity.add(circle_avoid)
            else:
                self.velocity = self.velocity.subtract(circle_avoid)


        # Crowding avoidance
        for bird in (bird for bird in flock if 0 < self.get_distance_to(bird) < self.detection_radius):
            vector_to_bird = bird.position.subtract(self.position)
            r = vector_to_bird.get_magnitude()
            bird_avoid = vector_to_bird.scale(-1 * self.bird_avoid_strength / (r * r))

            self.velocity = self.velocity.add(bird_avoid)

        # Enforce speed limit
        speed = self.velocity.get_magnitude()
        if speed > self.speed_limit:
            self.velocity = self.velocity.scale(self.speed_limit / speed)

    # Update this bird's position
    def move(self, flock):
        self.update_velocity(flock)
        self.position = self.position.add(self.velocity)

    # FInd the distance from this bird to another one
    def get_distance_to(self, bird):
        return self.position.subtract(bird.position).get_magnitude()





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
