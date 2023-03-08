import random
import pygame
from dino_runner.components import game
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import BIRD, LARGE_CACTUS, SMALL_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            self.type = random.randint(0,2)
            if self.type == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif self.type == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS))
            elif self.type == 2:
                self.obstacles.append(Bird(BIRD))
            
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False
                self.obstacles = []
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    #def reset_obstacle(self):
        #self.obstacles = []

    
        
