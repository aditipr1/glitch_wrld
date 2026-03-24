import pygame
import random
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glitch World")

clock = pygame.time.Clock()

player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 0.5
speed = 5
on_ground = False

platforms = [
    pygame.Rect(0, 400, 800, 50),
    pygame.Rect(200, 300, 150, 20),
    pygame.Rect(450, 220, 150, 20)
]

running = True
while running:
    clock.tick(60)
    
    # Random background glitch color
    bg_color = (
        random.randint(0,50),
        random.randint(0,50),
        random.randint(0,50)
    )
    screen.fill(bg_color)

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

    # 🔥 RANDOM GLITCHES

    # 1. Random gravity change
    if random.random() < 0.01:
        gravity = random.uniform(-0.8, 0.8)

    # 2. Random teleport
    if random.random() < 0.005:
        player.x = random.randint(0, WIDTH-40)
        player.y = random.randint(0, HEIGHT-40)

    # 3. Platforms randomly disappear
    visible_platforms = []
    for p in platforms:
        if random.random() > 0.2:  # 80% chance visible
            visible_platforms.append(p)

    # Apply gravity
    velocity_y += gravity
    player.y += velocity_y

    # Collision
    on_ground = False
    for p in visible_platforms:
        if player.colliderect(p):
            if velocity_y > 0:
                player.bottom = p.top
                velocity_y = 0
                on_ground = True

    # Draw platforms
    for p in visible_platforms:
        pygame.draw.rect(screen, (0, 255, 0), p)

    # Player glitch color
    player_color = (
        random.randint(100,255),
        random.randint(0,255),
        random.randint(0,255)
    )
    pygame.draw.rect(screen, player_color, player)

    pygame.display.update()

pygame.quit()