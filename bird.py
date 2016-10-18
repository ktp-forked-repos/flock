import random

from vector import Vector

HEIGHT = 1000
WIDTH = 1000


# This class defines a bird, which is a member of a flock
class Bird:
    position = Vector(0, 0)
    velocity = Vector(0, 0)
    color = ()
    disperse = False

    # Movement parameters
    speed_limit = 8
    detection_radius = 50
    separation_strength = 30
    cohesion_strength = 0.1
    alignment_strength = 0.5

    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.velocity = Vector(random.random() * 10 - 5, random.random() * 10 - 5)

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

    # Update this bird's velocity
    def update_velocity(self, flock):

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

        if self.disperse:
            cohesion = cohesion.scale(-1)
            alignment = Vector(0, 0)

        # Apply influences
        self.velocity = self.velocity.add(separation).add(cohesion).add(alignment)

        # Enforce speed limit
        speed = self.velocity.get_magnitude()
        if speed > self.speed_limit:
            self.velocity = self.velocity.scale(self.speed_limit / speed)

    # Update this bird's position
    def move(self, flock):
        self.update_velocity(flock)
        self.position = self.position.add(self.velocity)

        self.position.x = self.position.x % WIDTH
        self.position.y = self.position.y % HEIGHT

    # FInd the distance from this bird to another one
    def get_distance_to(self, bird):
        return self.position.subtract(bird.position).get_magnitude()
