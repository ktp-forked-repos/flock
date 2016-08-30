import pygame
import math
import random

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RADIUS = 500


def point_in_circle(x, y, radius):
    dx = abs(x - radius)
    dy = abs(y - radius)

    if dx + dy < radius:
        return True

    if dx > radius:
        return False

    if dy > radius:
        return False

    if dx*dx + dy*dy > radius * radius:
        return False
    else:
        return True


class Bird:
    x = 0
    y = 0
    speed = 0
    heading = 0
    color = ()

    def __init__(self, x, y, speed, heading, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.heading = heading
        self.color = color

    def update_heading(self):

        if random.randint(0, 3) == 3:
            delta = random.randint(-10, 10) / 30
            self.heading += delta

        proj_x = self.x + 30 * math.sin(self.heading)
        proj_y = self.y - 30 * math.cos(self.heading)

        while not point_in_circle(proj_x, proj_y, RADIUS):
            self.heading -= 0.15
            proj_x = self.x + 30 * math.sin(self.heading)
            proj_y = self.y - 30 * math.cos(self.heading)

    def move(self):
        self.update_heading()

        self.x += self.speed * math.sin(self.heading)
        self.y -= self.speed * math.cos(self.heading)


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
    tweety = Bird(RADIUS, RADIUS, 3, 0, RED)

    flock = [tweety]
    for i in range(200):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        flock.append(Bird(RADIUS, RADIUS, 1 + (2 * random.random()), 2 * random.random() * math.pi, color))

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
            x = int(bird.x)
            y = int(bird.y)
            # hx = int(x + 30*math.sin(bird.heading))
            # hy = int(y - 30*math.cos(bird.heading))
            pygame.draw.circle(screen, bird.color, [x, y], 5)
            # pygame.draw.line(screen, RED, [x, y], [hx, hy], 2)

        # Update screen    
        pygame.display.flip()

        # Limit to 60 fps
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
