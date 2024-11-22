import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0 ,0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Bricks")

clock = pygame.time.Clock()

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20

BRICK_WIDTH = 50
BRICK_HEIGHT = 30

FPS = 60

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()