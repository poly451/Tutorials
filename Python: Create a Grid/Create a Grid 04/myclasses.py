import pygame
import constants
from graphics_environment import Grasses, Walls
from shutil import copyfile
import os, sys
from graphics_fauna import Player, Monster
from dialogs import DialogFight, TextDialog

class Game:
    def __init__(self):
        self.init_pygame()
        self.grasses = Grasses()
        self.walls = Walls()
        self.monster = Monster()
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        # -------------------------------------
        self.keep_looping = True
        # -------------------------------------
        # Copy the original data files over to temporary
        # files that will last only as long as the
        # game is running.
        source_file = os.path.join("data", constants.MONSTERS_ORIGINAL_DATA_FILE)
        destination_file = os.path.join("data", constants.MONSTERS_DATA_FILE)
        copyfile(source_file, destination_file)
        source_file = os.path.join("data", constants.PLAYER_ORIGINAL_DATA_FILE)
        destination_file = os.path.join("data", constants.PLAYER_DATA_FILE)
        copyfile(source_file, destination_file)

    def read_data(self):
        self.player.read_data_first()
        self.monster.read_data()

    def player_died(self):
        s = "You're dead! Game over."
        mydialog = TextDialog(s)
        mydialog.main()
        self.keep_looping = False
        self.init_pygame()

    def restart_game(self):
        self.init_pygame()
        self.keep_looping = True
        self.grasses = Grasses()
        self.walls = Walls()
        self.monster = Monster()
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.fight = False
        # ----------------------------------------
        self.player.read_data_restart()
        self.monster.read_data()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def there_is_a_monster_on_this_tile(self, x, y):
        if self.monster.x == x and self.monster.y == y:
            return True
        return False

    def dialog_have_a_fight(self):
        fight_dialog = DialogFight(self.player, self.monster)
        fight_dialog.main()
        # message = fight_dialog.main()
        # ----
        print("in myclasses in dialog_have_a_fight. monster.hit_points: {}".format(self.monster.hit_points))
        if self.monster.is_dead() == True:
            print("Monster is dead")
            self.restart_game()
            self.monster.image = self.monster.image_dead_monster
        elif self.player.is_dead() == True:
            print("Player is dead")
            self.restart_game()
            self.player.image = self.player.image_dead

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
                if event.key == pygame.K_LEFT:
                    if self.player.direction == constants.DOWN:
                        self.player.image = pygame.transform.rotate(self.player.image, -90)
                    elif self.player.direction == constants.UP:
                        self.player.image = pygame.transform.rotate(self.player.image, 90)
                    elif self.player.direction == constants.LEFT:
                        self.player.image = pygame.transform.rotate(self.player.image, 0)
                    elif self.player.direction == constants.RIGHT:
                        self.player.image = pygame.transform.rotate(self.player.image, -180)
                    self.player.move(dx=-1, dy=0, walls=self.walls)
                    self.player.direction = constants.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.player.direction == constants.DOWN:
                        self.player.image = pygame.transform.rotate(self.player.image, 90)
                    elif self.player.direction == constants.UP:
                        self.player.image = pygame.transform.rotate(self.player.image, -90)
                    elif self.player.direction == constants.LEFT:
                        self.player.image = pygame.transform.rotate(self.player.image, -180)
                    elif self.player.direction == constants.RIGHT:
                        self.player.image = pygame.transform.rotate(self.player.image, 0)
                    self.player.move(dx=1, walls=self.walls)
                    self.player.direction = constants.RIGHT
                elif event.key == pygame.K_DOWN:
                    if self.player.direction == constants.DOWN:
                        self.player.image = pygame.transform.rotate(self.player.image, 0)
                    elif self.player.direction == constants.UP:
                        self.player.image = pygame.transform.rotate(self.player.image, 180)
                    elif self.player.direction == constants.LEFT:
                        self.player.image = pygame.transform.rotate(self.player.image, 90)
                    elif self.player.direction == constants.RIGHT:
                        self.player.image = pygame.transform.rotate(self.player.image, -90)
                    self.player.move(dy=1, walls=self.walls)
                    self.player.direction = constants.DOWN
                elif event.key == pygame.K_UP:
                    if self.player.direction == constants.DOWN:
                        self.player.image = pygame.transform.rotate(self.player.image, 180)
                    elif self.player.direction == constants.UP:
                        self.player.image = pygame.transform.rotate(self.player.image, 0)
                    elif self.player.direction == constants.LEFT:
                        self.player.image = pygame.transform.rotate(self.player.image, -90)
                    elif self.player.direction == constants.RIGHT:
                        self.player.image = pygame.transform.rotate(self.player.image, 90)
                    self.player.move(dy=-1, walls=self.walls)
                    self.player.direction = constants.UP
                elif event.key == pygame.K_h: # <=================================================
                    if self.there_is_a_monster_on_this_tile(self.player.x, self.player.y) == False:
                        print("Player swings at the air!")
                        return False
                    if self.monster.is_dead() == True:
                        return False
                    print("Fight!!!")
                    self.dialog_have_a_fight()
                    if self.player.is_dead() == True:
                        self.player_died()
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self):
        for elem in self.grasses:
            self.all_sprites.add(elem)
        for elem in self.walls:
            self.all_sprites.add(elem)
        self.all_sprites.add(self.monster)
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
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        self.goodbye()
        self.myquit()

    def myquit(self):
        pygame.quit()
        # sys.exit()

    def goodbye(self):
        s = "Thank you for playing {}!️‍️".format(constants.TITLE)
        mydialog = TextDialog(s)
        mydialog.main()

if __name__ == "__main__":
    mygame = Game()
    mygame.read_data()
    mygame.main()