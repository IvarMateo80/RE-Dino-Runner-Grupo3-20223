import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.power_ups.power_up import PowerUp
from dino_runner.components.obstacles.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BIRD, DEFAULT_TYPE, DINO, LARGE_CACTUS, SCREEN_WIDTH, SHIELD_TYPE, SMALL_CACTUS

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
                if not game.player.shield:
                    game.death_counter += 1
                    pygame.time.delay(1000)
                    game.playing = False
                    self.obstacles = []
                    game.x_pos_cloud = SCREEN_WIDTH
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    #def reset_obstacle(self):
        #self.obstacles = []

    
        
