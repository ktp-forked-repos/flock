import pygame
import math
import random

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RADIUS = 500


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


def main():
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Window size
    size = (RADIUS * 2, RADIUS * 2)
    screen = pygame.display.set_mode(size)

    # Window title
    pygame.display.set_caption('Flock')

    # Sim variables
    flock = []
    for i in range(200):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        flock.append(Bird(Vector(RADIUS, RADIUS), Vector(random.random() * 10 - 5, random.random() * 10 - 5), color))

    # Main sim loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Clear screen
        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, [0, 0, RADIUS * 2, RADIUS * 2])

        # Move and draw birds
        for bird in flock:
            # Move bird
            bird.move()

            # Draw bird
            x = int(bird.position.x)
            y = int(bird.position.y)
            pygame.draw.circle(screen, bird.color, [x, y], 5)

            circle_vector = get_vector_to_circle(bird.position, RADIUS)
            hx = int(circle_vector.x) + x
            hy = int(circle_vector.y) + y
            # pygame.draw.line(screen, RED, [x, y], [hx, hy], 2)

        # Update screen    
        pygame.display.flip()

        # Limit to 100 fps
        clock.tick(100)

    pygame.quit()


if __name__ == '__main__':
    main()
