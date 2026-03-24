import pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glitch World - Stable Build")

clock = pygame.time.Clock()

# Colors (black + green theme)
BG = (10, 10, 10)
PLATFORM_COLOR = (0, 200, 0)
PLAYER_COLOR = (0, 255, 100)
SPAWN_COLOR = (0, 150, 0)

# Player
player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 0.5
speed = 5
on_ground = False

# Spawn point
spawn_point = (100, 300)

# Platforms
platforms = [
    pygame.Rect(0, 450, 800, 50),     # ground
    pygame.Rect(200, 350, 150, 20),
    pygame.Rect(400, 280, 150, 20),
    pygame.Rect(650, 220, 120, 20)
]

running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed

    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = -10
        on_ground = False

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    # Collision
    on_ground = False
    for p in platforms:
        if player.colliderect(p):
            if velocity_y > 0:
                player.bottom = p.top
                velocity_y = 0
                on_ground = True

    # 💀 Death condition (fall off screen)
    if player.y > HEIGHT:
        player.x, player.y = spawn_point
        velocity_y = 0

    # 🟢 Draw spawn area
    spawn_rect = pygame.Rect(spawn_point[0], spawn_point[1], 40, 40)
    pygame.draw.rect(screen, SPAWN_COLOR, spawn_rect, 2)

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, p)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    pygame.display.update()

pygame.quit()