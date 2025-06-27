import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, OBSTACLE_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, kind):
        super().__init__()
        if kind == 'tall':
            self.image = pygame.Surface((30, 80))
            self.image.fill((200, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - 80
        elif kind == 'wide':
            self.image = pygame.Surface((60, 40))
            self.image.fill((0, 200, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - 40
        elif kind == 'gravity':
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - 100
        else:  # normal
            self.image = pygame.Surface((30, 60))
            self.image.fill((0, 0, 200))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - 60
        self.kind = kind

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

def generate_obstacle(obstacles, last_obstacle_x):
    if last_obstacle_x < SCREEN_WIDTH - random.randint(200, 400):
        kind = random.choice(['normal', 'tall', 'wide', 'gravity', 'normal'])
        obstacle = Obstacle(SCREEN_WIDTH, kind)
        obstacles.add(obstacle)
        return SCREEN_WIDTH
    return last_obstacle_x
