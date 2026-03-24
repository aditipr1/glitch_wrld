import pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glitch World - Full Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Colors
BG = (10, 10, 10)
GREEN = (0, 200, 0)
PLAYER_COLOR = (0, 255, 100)
SPIKE_COLOR = (255, 50, 50)
GOAL_COLOR = (0, 255, 0)
CHECKPOINT_COLOR = (0, 150, 0)

# Player
player = pygame.Rect(100, 300, 40, 40)
velocity_y = 0
gravity = 0.5
speed = 5
on_ground = False

spawn_point = [100, 300]

# Timer
start_time = pygame.time.get_ticks()
game_won = False

# Platforms
platforms = [
    pygame.Rect(0, 450, 800, 50),
    pygame.Rect(200, 350, 150, 20),
    pygame.Rect(400, 280, 150, 20),
]

# Moving platform
moving_platform = pygame.Rect(600, 220, 120, 20)
move_dir = 1

# Spikes
spikes = [
    pygame.Rect(300, 430, 40, 20),
    pygame.Rect(500, 260, 40, 20)
]

# Checkpoints
checkpoints = [
    pygame.Rect(420, 240, 20, 40)
]

# Goal
goal = pygame.Rect(750, 180, 30, 50)

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

    # Moving platform logic
    moving_platform.x += move_dir * 2
    if moving_platform.x < 500 or moving_platform.x > 700:
        move_dir *= -1

    # Collision
    on_ground = False
    all_platforms = platforms + [moving_platform]

    for p in all_platforms:
        if player.colliderect(p):
            if velocity_y > 0:
                player.bottom = p.top
                velocity_y = 0
                on_ground = True

    # 💀 Death (fall)
    if player.y > HEIGHT:
        player.x, player.y = spawn_point
        velocity_y = 0

    # 💀 Death (spikes)
    for spike in spikes:
        if player.colliderect(spike):
            player.x, player.y = spawn_point
            velocity_y = 0

    # 📦 Checkpoints
    for cp in checkpoints:
        if player.colliderect(cp):
            spawn_point = [cp.x, cp.y]

    # 🎯 Goal
    if player.colliderect(goal):
        game_won = True

    # Draw platforms
    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)

    pygame.draw.rect(screen, GREEN, moving_platform)

    # Draw spikes
    for spike in spikes:
        pygame.draw.rect(screen, SPIKE_COLOR, spike)

    # Draw checkpoints
    for cp in checkpoints:
        pygame.draw.rect(screen, CHECKPOINT_COLOR, cp)

    # Draw goal
    pygame.draw.rect(screen, GOAL_COLOR, goal)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # ⏱️ Timer
    if not game_won:
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render(f"Time: {elapsed}s", True, (0,255,0))
        screen.blit(timer_text, (10, 10))
    else:
        win_text = font.render("YOU WIN!", True, (0,255,0))
        screen.blit(win_text, (350, 200))

    pygame.display.update()

pygame.quit()