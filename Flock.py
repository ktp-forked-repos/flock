import pygame
import random

from Bird import Bird
from Vector import Vector

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RADIUS = 500


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
    for i in range(100):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        flock.append(Bird(Vector(RADIUS, RADIUS), color))

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
            bird.move(flock)

            # Draw bird
            x = int(bird.position.x)
            y = int(bird.position.y)
            pygame.draw.circle(screen, bird.color, [x, y], 5)

        # Update screen    
        pygame.display.flip()

        # Limit to 100 fps
        clock.tick(100)

    pygame.quit()


if __name__ == '__main__':
    main()
