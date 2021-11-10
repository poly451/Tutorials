import pygame
import constants
import os, sys

import utils
# from environment import Walkables, Obstacles
from environment import Environment
# ------------------------------------------------------
#                       class Player
# ------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, movement_increment):
        super().__init__()
        self.movement_increment = movement_increment
        # ----
        self.image_list = []
        self.image_list_walk = []
        self.image_list_idle = []
        self.image_list_slash = []
        self.image_list_spell = []
        self.image_list_unconscious = []
        self.image_list_fall = []
        # ----
        self.movement_increment = movement_increment
        self.movement = "idle"
        self.direction = "right"
        # ----
        self.number_of_steps_taken = 0
        self.counter = 0
        self.index = 0
        self.image = None
        self.rect = None
        self.x, self.y = 1, 1
        # ----

    def read_data(self):
        self.image_list_walk = self.read_in_image_list_complex("walk", "front")
        self.image_list_idle = self.read_in_image_list_complex("idle", "front")
        self.image_list_slash = self.read_in_image_list_complex("slash", "front")
        self.image_list_spell = self.read_in_image_list_complex("spell", "front")
        self.image_list_unconscious = self.read_in_image_list_simple("unconscious")
        self.image_list_fall = self.read_in_image_list_simple("fall")
        # ----
        if self.movement == "walk":
            self.image_list = self.image_list_walk
        elif self.movement == "idle":
            self.image_list = self.image_list_idle
        elif self.movement == "slash":
            self.image_list = self.image_list_slash
        elif self.movement == "spell":
            self.image_list = self.image_list_spell
        elif self.movement == "unconscious":
            self.image_list = self.image_list_unconscious
        elif self.movement == "fall":
            self.image_list = self.image_list_fall
        else:
            s = "I don't recognize this: {}".format(self.movement)
            raise ValueError(s)
        # ----
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()

    def read_in_image_list_simple(self, kind):
        directory_path = os.path.join("data", "images", "characters", "baldric", kind)
        if os.path.isdir(directory_path) == False: raise ValueError("Error")
        filenames = os.listdir(directory_path)
        images = []
        for filename in filenames:
            path = os.path.join(directory_path, filename)
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (constants.TILESIZE, constants.TILESIZE))
            # self.rect = image.get_rect()
            images.append(image)
        return images

    def read_in_image_list_complex(self, kind, direction):
        directory_path = os.path.join("data", "images", "characters", "baldric", kind, direction)
        if os.path.isdir(directory_path) == False: raise ValueError("Error")
        # ----
        images = []
        filenames = os.listdir(directory_path)
        for filename in filenames:
            path = os.path.join(directory_path, filename)
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (constants.TILESIZE, constants.TILESIZE))
            # self.rect = image.get_rect()
            images.append(image)
        return images

    # def move(self, advance_x, advance_y):
    #     dx = self.movement_increment * advance_x # if advance_x = 0 then dx will be 0 and sprite will not move along that axis.
    #     dy = self.movement_increment * advance_y # if advance_y = 0 then dy will be 0 and sprite will not move along that axis.
    #     # self.rect = self.rect.move(dx, dy)
    #     print("DEBUGGING: dx,dy: {},{}".format(dx, dy))
    #     # ----
    #     self.x += dx
    #     self.y += dy
    #     print("DEBUGGING: def move: self.x, self.y: {},{}".format(self.x, self.y))
    #     # return x, y

    # def change_movement(self, movement):
    #     self.movement = movement
    #     if not movement in constants.MOVEMENT_VALUES:
    #         s = "I do not recognize this movement: {}".format(movement)
    #         raise ValueError(s)
    #     self.change_animation(movement)

    def change_animation(self, movement):
        self.movement = movement
        # ----
        if self.movement not in constants.MOVEMENT_VALUES: raise ValueError("Error")
        if self.direction not in constants.DIRECTION_VALUES:
            s = "I do not recognize this direction: {}".format(self.direction)
            raise ValueError(s)
        # ----
        self.counter = 0
        if self.movement == "walk":
            self.image_list = self.image_list_walk
        elif self.movement == "spell":
            self.image_list = self.image_list_spell
        elif self.movement == "slash":
            self.image_list = self.image_list_slash
        elif self.movement == "idle":
            self.image_list = self.image_list_idle
        elif self.movement == "fall":
            self.image_list = self.image_list_fall
        else:
            s = "I don't recognize this kind of movement: {}".format(self.movement)
            raise ValueError(s)
        if self.image_list is None: raise ValueError("Error")
        if len(self.image_list) == 0: raise ValueError("Error")

    # in class Player
    def update_classes(self, environment):
        self.image = self.image_list[self.counter]
        self.rect = self.image.get_rect()
        # ----
        if self.movement == "walk":
            if self.direction == "right":
                if self.counter == 0:
                    temp_x = self.x + 1
                    temp_y = self.y
                    temp_x = round(temp_x)
                    temp_y = round(temp_y)
                    if environment.obstacles.collision(temp_x, temp_y) == True:
                        self.movement = "idle"
                        self.change_animation(self.movement)
                    else:
                        self.x += self.movement_increment
                else:
                    self.x += self.movement_increment
            elif self.direction == "left":
                if self.counter == 0:
                    temp_x = self.x - 1
                    temp_y = self.y
                    temp_x = round(temp_x)
                    temp_y = round(temp_y)
                    # print("temp_x,tempy: {},{}".format(temp_x, temp_y))
                    if environment.obstacles.collision(temp_x, temp_y) == True:
                        self.movement = "idle"
                        self.change_animation(self.movement)
                    else:
                        self.x -= self.movement_increment
                else:
                    self.x -= self.movement_increment
            elif self.direction == "front":
                if self.counter == 0:
                    temp_x = self.x
                    temp_y = self.y + 1
                    temp_x = round(temp_x)
                    temp_y = round(temp_y)
                    if environment.obstacles.collision(temp_x, temp_y) == True:
                        self.movement = "idle"
                        self.change_animation(self.movement)
                    else:
                        self.y += self.movement_increment
                else:
                    self.y += self.movement_increment
            elif self.direction == "back":
                if self.counter == 0:
                    temp_x = self.x
                    temp_y = self.y - 1
                    temp_x = round(temp_x)
                    temp_y = round(temp_y)
                    if environment.obstacles.collision(temp_x, temp_y) == True:
                        self.movement = "idle"
                        self.change_animation(self.movement)
                    else:
                        self.y -= self.movement_increment
                else:
                    self.y -= self.movement_increment
            else:
                raise ValueError("Error")
        # ---- ---- ---- ----
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        print("self.x, self.y: {},{}".format(self.x, self.y))
        # ----
        self.counter += 1
        # ----
        print("counter: {}".format(self.counter))
        print("movement: {}".format(self.movement))
        print("number_of_steps_taken: {}".format(self.number_of_steps_taken))
        if self.counter + 1 >= len(self.image_list):
            self.counter = 0
            # ----
            print("----------------------------------")
            print("self.x,self.y: {},{}".format(self.x, self.y))
            self.x = round(self.x)
            self.y = round(self.y)
            print("ROUNDED self.x,self.y: {},{}".format(self.x, self.y))
            print("----------------------------------")
            # ----
            if self.movement == "walk":
                self.movement = "idle"

    def debug_print(self):
        print("rect: {}".format(self.image.get_rect()))
        # print("x,y: {},{}".format(self.x, self.y))

# ------------------------------------------------------
#                 class ControllingMySprite
# ------------------------------------------------------
class Game:
    def __init__(self, zone_name, map_name, movement_increment):
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.init_graphics()
        # self.movement_increment = movement_increment
        # self.step_size = step_size
        # ----
        # self.environment = Walkables("testing", "map00")
        self.environment = Environment(zone_name=zone_name,
                                       map_name=map_name)
        self.player = Player(movement_increment)
        # ----
        self.keep_looping = True

    def read_data(self):
        self.environment.read_data()
        self.player.read_data()

    def init_graphics(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        self.all_sprites = pygame.sprite.Group()

    # #####################################################

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True
                elif event.key == pygame.K_w:
                    self.player.change_animation("walk")
                elif event.key == pygame.K_f:
                    self.player.change_animation("fall")
                elif event.key == pygame.K_l:
                    self.player.change_animation("slash")
                elif event.key == pygame.K_s:
                    self.player.change_animation("spell")
                elif event.key == pygame.K_u:
                    self.player.change_animation("unconscious")
                # ----
                elif event.key == pygame.K_RIGHT:
                    self.player.direction = "right"
                    self.player.change_animation("walk")
                elif event.key == pygame.K_LEFT:
                    self.player.direction = "left"
                    self.player.change_animation("walk")
                elif event.key == pygame.K_DOWN:
                    self.player.direction = "front"
                    self.player.change_animation("walk")
                elif event.key == pygame.K_UP:
                    self.player.direction = "back"
                    self.player.change_animation("walk")

    def update(self):
        pass

    # in class Game
    def update_classes(self):
        self.all_sprites = self.environment.update_classes(self.all_sprites)
        self.player.update_classes(self.environment)
        self.all_sprites.add(self.player)

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        self.update_classes()
        # pygame.display.update()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        # ---- ----
        # self.counter += 1
        # if self.counter >= len(self.player.image_list):
        #     self.image_counter = 0

    # #####################################################

    def goodbye(self):
        pygame.quit()
        sys.exit()

    def main(self):
        while self.keep_looping == True:
            self.clock.tick(10)
            self.handle_events()
            self.update()
            self.draw()
        self.goodbye()

# *****************************************************

def main():
    zone_name = "testing"
    map_name = "map01"
    movement_inc = 0.12
    control_sprite_strip = Game(zone_name=zone_name,
                                map_name=map_name,
                                movement_increment=movement_inc)
    control_sprite_strip.read_data()
    control_sprite_strip.main()

if __name__ == "__main__":
    main()