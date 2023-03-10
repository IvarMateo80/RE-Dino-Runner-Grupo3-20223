import random
import pygame
from dino_runner.components.dino import Dino
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components import text_utils
from dino_runner.components.obstacles.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, CLOUD, DINO, GAMEOVER_RESTART, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = SCREEN_WIDTH
        self.player = Dino()
        self.obstacle_manager = ObstacleManager()
        self.points = 0 
        self.running = True
        self.death_counter = 0
        self.power_up_manager = PowerUpManager()
        self.dino = Dino()


    def run(self):
        # Game loop: events - update - draw
        self.create_components()
        self.playing = True
        self.game_speed = 20
        self.x_pos_cloud = SCREEN_WIDTH
        self.points = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player, self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_clouds()
        self.score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_clouds(self):
        self.screen.blit(CLOUD, (self.x_pos_cloud, 50))
        self.screen.blit(CLOUD, (self.x_pos_cloud - 300, 140))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 100, 160))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 450, 180))
        self.screen.blit(CLOUD, (self.x_pos_cloud + 900, 200))
        self.x_pos_cloud -= 1
        if self.x_pos_cloud < -1000:
            self.x_pos_cloud = SCREEN_WIDTH


    def execute (self):
        while self.running: 
            if not self.playing:
                self.show_menu()

    def show_menu(self):
        self.running = True
        
        white_color = (255, 255, 255)
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()

    def print_menu_elements(self):
        if self.death_counter == 0:
            text, text_rect = text_utils.get_centered_message('Press any Key to start', 550, 350)
            self.screen.blit(text, text_rect)
            self.screen.blit(DINO[1], (500, 230))
        
        elif self.death_counter > 0:
            text, text_rect = text_utils.get_centered_message("Death Count: " + str(self.death_counter), 550, 300)
            self.screen.blit(text, text_rect)
            text, text_rect = text_utils.get_centered_message("your score is: " + str(self.points - 1), 540, 350)
            self.screen.blit(text, text_rect)
            text, text_rect = text_utils.get_centered_message('Press any Key to start again', 540, 400)
            self.screen.blit(text, text_rect)
            self.screen.blit(GAMEOVER_RESTART[0], (355, 150))
            self.screen.blit(GAMEOVER_RESTART[1], (500, 200))
            self.screen.blit(DINO[0], (490, 450))


    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
            
    def score(self):
        self.points += 1 
        if self.points % 100 == 0:
            self.game_speed +=1
        text, text_rect = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)
        self.player.check_invincibility

    def create_components (self):
        self.power_up_manager.reset_power_ups(self.points)