import pygame
import random
import sys

# Configuración
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
OBSTACLE_SPEED = 6
MUSIC_FILE = 'assets/tu_musica.mp3'  # Cambia por tu archivo

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

# Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, kind, top=False):
        super().__init__()
        self.kind = kind
        self.top = top
        if kind == 'tall':
            self.image = pygame.Surface((30, 80))
            self.image.fill((200, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 0 if top else SCREEN_HEIGHT - 80
        elif kind == 'wide':
            self.image = pygame.Surface((60, 40))
            self.image.fill((0, 200, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 0 if top else SCREEN_HEIGHT - 40
        elif kind == 'gravity_up':
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - 100
        elif kind == 'gravity_down':
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 70
        else:  # normal
            self.image = pygame.Surface((30, 60))
            self.image.fill((0, 0, 200) if not top else (0, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 0 if top else SCREEN_HEIGHT - 60

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

group_obstacles = pygame.sprite.Group()
OBSTACLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_EVENT, 1000)  # Obstáculo cada 1s

# Puntuación
score = 0
font = pygame.font.SysFont(None, 36)
game_over = False

def draw_player():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 200, 255), (0, 0, 50, 50))
    rotated = pygame.transform.rotate(surf, player_angle)
    rect = rotated.get_rect(center=player.center)
    screen.blit(rotated, rect.topleft)

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

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == OBSTACLE_EVENT and not game_over:
            # Obstáculos abajo
            kind = random.choice(['normal', 'tall', 'wide', 'normal', 'gravity_up'])
            obstacle = Obstacle(SCREEN_WIDTH, kind, top=False)
            group_obstacles.add(obstacle)
            # Obstáculos arriba si gravedad invertida
            if random.random() < 0.7:
                kind_top = random.choice(['normal', 'tall', 'wide', 'normal', 'gravity_down'])
                obstacle_top = Obstacle(SCREEN_WIDTH, kind_top, top=True)
                group_obstacles.add(obstacle_top)
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
        group_obstacles.update()

        # Colisiones y gravedad
        for obstacle in group_obstacles:
            if player.colliderect(obstacle.rect):
                if obstacle.kind == 'gravity_up' and player_gravity == 1:
                    player_gravity = -1
                    player.y = 10
                    obstacle.kill()
                elif obstacle.kind == 'gravity_down' and player_gravity == -1:
                    player_gravity = 1
                    player.y = SCREEN_HEIGHT - 60
                    obstacle.kill()
                elif 'gravity' not in obstacle.kind:
                    game_over = True

        # Puntuación
        score += 1

    # Dibujar
    # Fondo degradado
    for y in range(SCREEN_HEIGHT):
        color = (
            min(30, 255),
            min(30 + y // 4, 255),
            min(60 + y // 2, 255)
        )
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
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
