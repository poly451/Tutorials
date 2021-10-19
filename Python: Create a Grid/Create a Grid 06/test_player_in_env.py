import pygame
import constants
from graphics_fauna import Player, Npcs, Monsters
from graphics_environment import Obstacles, Walkables

class TestGame:
    def __init__(self):
        self.init_pygame()
        self.walkables = Walkables()
        self.obstacles = Obstacles()
        self.monsters = Monsters()
        self.player = Player()
        self.npcs = Npcs(constants.STARTING_ZONE_NPCS)
        # ----
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()

    def read_data(self):
        self.walkables.read_data()
        self.obstacles.read_data()
        self.monsters.read_data()
        # ----
        if len(self.walkables) <= 0:
            raise ValueError("Error!")
        if len(self.obstacles) <= 0:
            raise ValueError("Error!")
        # ----
        self.npcs.read_data()
        self.player.read_data_first()
        # self.player.debug_print()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)
        self.all_sprites = pygame.sprite.Group()

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.image = self.player.image_left
                    self.player.move(dx=-1, dy=0, obstacles=self.obstacles)
                    self.player.direction = constants.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.image = self.player.image_right
                    self.player.move(dx=1, obstacles=self.obstacles)
                    self.player.direction = constants.RIGHT
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.image = self.player.image_down
                    self.player.move(dy=1, obstacles=self.obstacles)
                    self.player.direction = constants.DOWN
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.image = self.player.image_up
                    self.player.move(dy=-1, obstacles=self.obstacles)
                    self.player.direction = constants.UP

    def update_classes(self):
        for elem in self.walkables:
            self.all_sprites.add(elem)
        for elem in self.obstacles:
            self.all_sprites.add(elem)
        for elem in self.npcs:
            self.all_sprites.add(elem)
        for elem in self.monsters:
            self.all_sprites.add(elem)
        # self.all_sprites.add(self.monster)
        self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

def main():
    mygame = TestGame()
    mygame.read_data()
    mygame.main()

if __name__ == "__main__":
    main()