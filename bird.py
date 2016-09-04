import random

from vector import Vector

RADIUS = 500


# This class defines a bird, which is a member of a flock
class Bird:
    position = Vector(0, 0)
    velocity = Vector(random.random() - 0.5, random.random() - 0.5)
    color = ()

    # Movement parameters
    speed_limit = 10
    detection_radius = 100
    circle_avoid_strength = 130
    separation_strength = 5
    cohesion_strength = 0.01
    alignment_strength = 0.1
    mouse_avoid_strength = 1000

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # The separation rule:
    # Move away from all birds closer than the detection radius
    def get_separation_vector(self, flock):
        bird_avoid = Vector(0, 0);

        for bird in flock:
            r = self.get_distance_to(bird)
            if r == 0:
                continue
            bird_avoid = bird_avoid.subtract(bird.position.subtract(self.position).scale(1 / (r * r)))

        return bird_avoid.scale(self.separation_strength)

    # The cohesion rule:
    # Move towards the center of mass of the flock
    def get_cohesion_vector(self, flock):
        center_of_mass = Vector(0, 0)

        for bird in flock:
            center_of_mass = center_of_mass.add(bird.position)

        center_of_mass = center_of_mass.scale(1.0 / len(flock))

        return center_of_mass.subtract(self.position).scale(self.cohesion_strength)

    # The alignment rule:
    # Move towards the average heading of the flock
    def get_alignment_vector(self, flock):
        average_velocity = Vector(0, 0)

        for bird in flock:
            average_velocity = average_velocity.add(bird.velocity)

        return average_velocity.scale(self.alignment_strength / len(flock))

    # The circle avoidance rule:
    # Move away from the circle
    def get_circle_avoid_vector(self):
        circle_vector = get_vector_to_circle(self.position, RADIUS)
        if circle_vector is not None:
            r = circle_vector.get_magnitude()
            if r > self.detection_radius:
                return Vector(0, 0)

            circle_avoid = circle_vector.scale(-1 * self.circle_avoid_strength / (r * r))

            if not point_in_circle(self.position, RADIUS):
                circle_avoid = circle_avoid.scale(-1)

            return circle_avoid

        return Vector(0, 0)

    # The mouse avoidance rule:
    # Move away from the mouse
    def get_mouse_avoid(self, mouse):
        if not point_in_circle(mouse, RADIUS):
            return Vector(0, 0)

        vector_to_mouse = mouse.subtract(self.position)
        r = vector_to_mouse.get_magnitude()

        return vector_to_mouse.scale(-1 * self.mouse_avoid_strength / (r * r))

    # Update this bird's velocity
    def update_velocity(self, flock, mouse):

        apparent_flock = [bird for bird in flock if
                          self.get_distance_to(bird) < self.detection_radius and bird is not self]

        # Calculate all influences
        separation = Vector(0, 0)
        cohesion = Vector(0, 0)
        alignment = Vector(0, 0)
        if len(apparent_flock) != 0:
            separation = self.get_separation_vector(apparent_flock)
            cohesion = self.get_cohesion_vector(apparent_flock)
            alignment = self.get_alignment_vector(apparent_flock)

        circle_avoid = self.get_circle_avoid_vector()
        mouse_avoid = self.get_mouse_avoid(mouse)

        # Apply influences
        self.velocity = self.velocity.add(separation).add(cohesion).add(alignment).add(circle_avoid).add(mouse_avoid)

        # Enforce speed limit
        speed = self.velocity.get_magnitude()
        if speed > self.speed_limit:
            self.velocity = self.velocity.scale(self.speed_limit / speed)

    # Update this bird's position
    def move(self, flock, mouse):
        self.update_velocity(flock, mouse)
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
