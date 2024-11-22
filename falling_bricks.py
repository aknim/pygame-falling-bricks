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

paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = (SCREEN_HEIGHT - PADDLE_HEIGHT - 10)
paddle_speed = 10

class Brick:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT))

bricks = []
brick_spawn_timer = 0 # Timer to control brick spawn rate
BRICK_SPAWN_RATE = 30 # Spawn a new brick every 30 frames

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Move paddle
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed

    # Restrict paddle movement within screen bounds
    paddle_x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, paddle_x))

    screen.fill(BLACK)

    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Spawn bricks at intervals
    brick_spawn_timer += 1
    if brick_spawn_timer >= BRICK_SPAWN_RATE:
        brick_spawn_timer = 0
        brick_x = random.randint(0, SCREEN_WIDTH - BRICK_WIDTH)
        brick_speed = random.randint(3, 7)
        bricks.append(Brick(brick_x, 0, brick_speed))

    # Update and draw bricks
    for brick in bricks[:]:
        brick.move()
        brick.draw(screen)

        # Remove brick if it falls past the screen
        if brick.y > SCREEN_HEIGHT:
            bricks.remove(brick)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()