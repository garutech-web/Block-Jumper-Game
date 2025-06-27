import pygame
import sys
from config import *
from level import Obstacle, generate_obstacle

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Block Jumper')
clock = pygame.time.Clock()

# Cargar música
try:
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"No se pudo cargar la música: {e}")

# Jugador
player = pygame.Rect(80, SCREEN_HEIGHT - 60, 50, 50)
player_vel_y = 0
on_ground = True
player_angle = 0
player_gravity = 1  # 1 = normal, -1 = invertido

def draw_player():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 200, 255), (0, 0, 50, 50))
    rotated = pygame.transform.rotate(surf, player_angle)
    rect = rotated.get_rect(center=player.center)
    screen.blit(rotated, rect.topleft)

# Obstáculos
group_obstacles = pygame.sprite.Group()
last_obstacle_x = SCREEN_WIDTH

# Puntuación
score = 0
font = pygame.font.SysFont(None, 36)

def reset():
    global player, player_vel_y, on_ground, group_obstacles, last_obstacle_x, score, player_angle, player_gravity, game_over
    player.x, player.y = 80, SCREEN_HEIGHT - 60 if player_gravity == 1 else 10
    player_vel_y = 0
    on_ground = True
    group_obstacles.empty()
    last_obstacle_x = SCREEN_WIDTH
    score = 0
    player_angle = 0
    player_gravity = 1
    game_over = False

game_over = False

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = JUMP_STRENGTH * player_gravity
                    on_ground = False
                if event.key == pygame.K_r:
                    reset()
            else:
                if event.key == pygame.K_r:
                    reset()

    if not game_over:
        # Movimiento jugador
        player_vel_y += GRAVITY * player_gravity
        player.y += int(player_vel_y)
        if player_gravity == 1:
            if player.y >= SCREEN_HEIGHT - 60:
                player.y = SCREEN_HEIGHT - 60
                player_vel_y = 0
                on_ground = True
            elif player.y < 0:
                player.y = 0
                player_vel_y = 0
        else:
            if player.y <= 10:
                player.y = 10
                player_vel_y = 0
                on_ground = True
            elif player.y > SCREEN_HEIGHT - 50:
                player.y = SCREEN_HEIGHT - 50
                player_vel_y = 0

        # Giro en el aire
        if not on_ground:
            player_angle = (player_angle + 15) % 360
        else:
            player_angle = 0

        # Obstáculos
        last_obstacle_x = generate_obstacle(group_obstacles, last_obstacle_x)
        group_obstacles.update()

        # Colisiones y gravedad
        for obstacle in group_obstacles:
            if player.colliderect(obstacle.rect):
                if getattr(obstacle, 'kind', 'normal') == 'gravity':
                    player_gravity *= -1
                    if player_gravity == -1:
                        player.y = 10
                    else:
                        player.y = SCREEN_HEIGHT - 60
                    obstacle.kill()
                else:
                    game_over = True

        # Puntuación
        score += 1

    # Dibujar
    screen.fill((30, 30, 30))
    group_obstacles.draw(screen)
    draw_player()
    score_text = font.render(f"Score: {score//10}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    if game_over:
        over_text = font.render("Game Over! Presiona R para reiniciar", True, (255,100,100))
        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()

pygame.quit()
sys.exit()
