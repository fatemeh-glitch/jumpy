import pygame
import asyncio
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumpy")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False

    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Check for platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:  # Falling
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Jumping
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

        # Keep player in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

async def main():
    # Create game objects
    player = Player(WIDTH // 2, HEIGHT // 2)
    platforms = [
        Platform(100, 400, 200, 20),
        Platform(400, 300, 200, 20),
        Platform(200, 200, 200, 20),
        Platform(0, HEIGHT - 20, WIDTH, 20)  # Ground
    ]

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        player.velocity_x = 0
        if keys[pygame.K_LEFT]:
            player.velocity_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.velocity_x = PLAYER_SPEED

        # Update
        player.update(platforms)

        # Draw
        screen.fill(WHITE)
        for platform in platforms:
            platform.draw(screen)
        player.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
        # Required for web
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main()) 