import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0 ,0, 255)
GREEN = (0, 255, 0)

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

brick_hit_sound = pygame.mixer.Sound("crash.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

score = 0
lives = 3

class Brick:
    def __init__(self, x, y, speed, brick_type="regular"):
        self.x = x
        self.y = y
        self.speed = speed
        self.type = brick_type 
        self.color = RED
        if(brick_type=="heavy"):
            self.color = BLUE
        elif(brick_type=="bonus"):
            self.color = GREEN
    
    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT))

bricks = []
brick_spawn_timer = 0 # Timer to control brick spawn rate
BRICK_SPAWN_RATE = 120 # Spawn a new brick every 30 frames

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
        brick_type = random.choices(
            ["regular", "heavy", "bonus"], weights = [70, 20, 10], k=1
        )[0]
        bricks.append(Brick(brick_x, 0, brick_speed, brick_type))

    # Update and draw bricks
    for brick in bricks[:]:
        brick.move()
        brick.draw(screen)

        # Check collision with paddle
        if (brick.y + BRICK_HEIGHT >= paddle_y and
            paddle_x <= brick.x <= paddle_x + PADDLE_WIDTH):
            pygame.mixer.Sound.play(brick_hit_sound)
            if brick.type == "regular":
                score += 10
            elif brick.type == "heavy":
                score += 20
            elif brick.type == "bonus":
                score += 50
                lives += 1 
            bricks.remove(brick)
            continue

        # Remove brick if it falls past the screen
        if brick.y > SCREEN_HEIGHT:
            pygame.mixer.Sound.play(miss_sound)
            bricks.remove(brick)
            lives -= 1 # Deduct a life

    # Draw the score and lives
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    # Check for game over
    if lives <= 0:
        running = False

    pygame.display.flip()
    clock.tick(FPS)

# Game Over Screen
screen.fill(BLACK)
game_over_text = font.render("Game Over", True, RED)
pygame.mixer.Sound.play(game_over_sound)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))
pygame.display.flip()
pygame.time.wait(2000)