import pygame
import random

from bird import Bird
from vector import Vector

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RADIUS = 500


def disperse(flock):
    for bird in flock:
        bird.cohesion_strength = 0
        bird.alignment_strength = 0


def resume(flock):
    for bird in flock:
        bird.cohesion_strength = 0.01
        bird.alignment_strength = 0.1


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
        pygame.draw.ellipse(screen, WHITE, [0, 0, RADIUS * 2, RADIUS * 2])

        # Get mouse position
        mouse.x, mouse.y = pygame.mouse.get_pos()

        # Move and draw birds
        for bird in flock:
            # Move bird
            bird.move(flock, mouse)

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
