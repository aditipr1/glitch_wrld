import pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glitch World - Level 1")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Colors
BG = (10, 10, 10)
GREEN = (0, 200, 0)
PLAYER_COLOR = (0, 255, 100)
SPIKE_COLOR = (255, 0, 0)

# Player
player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 0.5
speed = 5
on_ground = False

spawn_point = [100, 300]

# Game state
lives = 3
level = 1
game_over = False

# Platforms
platforms = [
    pygame.Rect(0, 450, 800, 50),
    pygame.Rect(200, 350, 150, 20),
    pygame.Rect(400, 280, 150, 20),
]

# 🔺 SPIKE PATTERN (row of spikes)
spikes = []
for i in range(300, 500, 40):
    spikes.append(pygame.Rect(i, 430, 30, 20))

# Goal
goal = pygame.Rect(750, 180, 30, 50)

running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🔄 Restart game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                lives = 3
                player.x, player.y = 100, 300
                spawn_point = [100, 300]
                game_over = False

    if not game_over:

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

        # 💀 Death (fall)
        if player.y > HEIGHT:
            lives -= 1
            player.x, player.y = spawn_point
            velocity_y = 0

        # 💀 Death (spikes)
        for spike in spikes:
            if player.colliderect(spike):
                lives -= 1
                player.x, player.y = spawn_point
                velocity_y = 0

        # 💀 Game Over
        if lives <= 0:
            game_over = True

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)

    # 🔺 Draw spikes (triangle style)
    for spike in spikes:
        pygame.draw.polygon(screen, SPIKE_COLOR, [
            (spike.x, spike.y + spike.height),
            (spike.x + spike.width // 2, spike.y),
            (spike.x + spike.width, spike.y + spike.height)
        ])

    # Draw goal
    pygame.draw.rect(screen, (0,255,0), goal)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # UI
    level_text = font.render(f"Level: {level}", True, (0,255,0))
    lives_text = font.render(f"Lives: {lives}", True, (0,255,0))
    screen.blit(level_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    # Game Over screen
    if game_over:
        text = big_font.render("GAME OVER", True, (255,0,0))
        restart_text = font.render("Press R to Restart", True, (255,255,255))
        screen.blit(text, (280, 200))
        screen.blit(restart_text, (300, 260))

    pygame.display.update()

pygame.quit()