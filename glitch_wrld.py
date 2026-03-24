import pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glitch World - Hard Mode")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Colors
BG = (10, 10, 10)
GREEN = (0, 200, 0)
PLAYER_COLOR = (0, 255, 100)
SPIKE_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 255, 0)

# Player
player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 0.6
speed = 5
on_ground = False

spawn_point = [100, 300]

# Game state
lives = 3
level = 1
game_over = False
game_won = False

# Platforms
platforms = [
    pygame.Rect(0, 450, 800, 50),
    pygame.Rect(180, 360, 120, 20),
    pygame.Rect(350, 300, 100, 20),
    pygame.Rect(520, 240, 100, 20),
]

# Moving platform
moving_platform = pygame.Rect(650, 180, 100, 20)
move_dir = 1

# 🔺 Ground spikes (FULL ROW with safe start zone)
ground_spikes = []
for i in range(0, WIDTH, 35):
    if i < 120:  # safe spawn area
        continue
    ground_spikes.append(pygame.Rect(i, 430, 30, 20))

# 🔺 Platform spikes (alternate platforms)
platform_spikes = []

# Goal
goal_pos = (750, 140)
goal_radius = 15

running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                lives = 3
                player.x, player.y = 100, 300
                spawn_point = [100, 300]
                velocity_y = 0
                game_over = False
                game_won = False

    if not game_over and not game_won:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed

        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = -11
            on_ground = False

        velocity_y += gravity
        player.y += velocity_y

        # Moving platform
        moving_platform.x += move_dir * 3
        if moving_platform.x < 500 or moving_platform.x > 720:
            move_dir *= -1

        # 🔺 Update platform spikes dynamically
        platform_spikes = []
        all_platforms_for_spikes = platforms + [moving_platform]

        for i, p in enumerate(all_platforms_for_spikes):
            if i % 2 == 1:
                spike_x = p.x + p.width // 2 - 15
                spike_y = p.y - 20
                platform_spikes.append(pygame.Rect(spike_x, spike_y, 30, 20))

        # Collision
        on_ground = False
        all_platforms = platforms + [moving_platform]

        for p in all_platforms:
            if player.colliderect(p):
                if velocity_y > 0:
                    player.bottom = p.top
                    velocity_y = 0
                    on_ground = True

                    if p == moving_platform:
                        player.x += move_dir * 3

        # 💀 Death (fall)
        if player.y > HEIGHT:
            lives -= 1
            player.x, player.y = spawn_point
            velocity_y = 0

        # 💀 Death (ALL spikes)
        for spike in ground_spikes + platform_spikes:
            if player.colliderect(spike):
                lives -= 1
                player.x, player.y = spawn_point
                velocity_y = 0

        if lives <= 0:
            game_over = True

        # 🎯 Goal
        dx = player.centerx - goal_pos[0]
        dy = player.centery - goal_pos[1]
        if dx*dx + dy*dy < goal_radius*goal_radius:
            game_won = True

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)
    pygame.draw.rect(screen, GREEN, moving_platform)

    # 🔺 Draw ground spikes
    for spike in ground_spikes:
        pygame.draw.polygon(screen, SPIKE_COLOR, [
            (spike.x, spike.y + spike.height),
            (spike.x + spike.width // 2, spike.y),
            (spike.x + spike.width, spike.y + spike.height)
        ])

    # 🔺 Draw platform spikes
    for spike in platform_spikes:
        pygame.draw.polygon(screen, SPIKE_COLOR, [
            (spike.x, spike.y + spike.height),
            (spike.x + spike.width // 2, spike.y),
            (spike.x + spike.width, spike.y + spike.height)
        ])

    # Goal
    pygame.draw.circle(screen, GOAL_COLOR, goal_pos, goal_radius)

    # Player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # UI
    screen.blit(font.render(f"Level: {level}", True, (0,255,0)), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, (0,255,0)), (10, 40))

    if game_over:
        screen.blit(big_font.render("GAME OVER", True, (255,0,0)), (280, 200))
        screen.blit(font.render("Press R to Restart", True, (255,255,255)), (300, 260))

    if game_won:
        screen.blit(big_font.render("LEVEL COMPLETE!", True, (0,255,0)), (240, 200))
        screen.blit(font.render("Press R to Play Again", True, (255,255,255)), (270, 260))

    pygame.display.update()

pygame.quit()