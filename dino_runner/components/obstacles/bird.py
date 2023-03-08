import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird (Obstacle):
    def __init__(self, image):
        self.image = BIRD[0]
        self.rect = self.image.get_rect()
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(220, 300)
        self.fly_index = 0 

    def update(self, game_speed, obstacles):
        self.fly()
        if self.fly_index >= 10:
            self.fly_index = 0
        return super().update(game_speed, obstacles)
  
    def fly(self):
        if self.fly_index < 5:
            self.image = BIRD[0]
        else:
            self.image = BIRD[1]   
        
        self.fly_index += 1

    def draw(self, screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
