# Author: Kiran Tomlinson
# Version: 1.1

import pygame
import random

from bird import Bird
from vector import Vector

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 1000
HEIGHT = 1000


def disperse(flock):
    for bird in flock:
        bird.disperse = True


def resume(flock):
    for bird in flock:
        bird.disperse = False


def main():
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Window size
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)

    # Window title
    pygame.display.set_caption('Flock')

    # Sim variables
    flock = []
    for i in range(100):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        flock.append(Bird(Vector(random.randint(0, WIDTH), random.randint(0, WIDTH)), color))

    # Main sim loop
    done = False
    while not done:
        mouse = Vector(-1, -1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    disperse(flock)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    resume(flock)

        # Clear screen
        screen.fill(BLACK)

        # Get mouse position
        mouse.x, mouse.y = pygame.mouse.get_pos()

        # Move and draw birds
        for bird in flock:
            # Move bird
            bird.move(flock)

            # Draw bird
            x = int(bird.position.x)
            y = int(bird.position.y)
            pygame.draw.circle(screen, bird.color, [x, y], 8)
            pygame.draw.line(screen, bird.color, [x, y], [x + bird.velocity.x * 3, y + bird.velocity.y * 3], 3)

        # Update screen    
        pygame.display.flip()

        # Limit to 100 fps
        clock.tick(100)

    pygame.quit()


if __name__ == '__main__':
    main()
