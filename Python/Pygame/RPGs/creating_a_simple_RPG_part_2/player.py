import pygame
import utils
import sys, os
import constants
from player_behaviors import LPCModel

# ------------------------------------------------------
#                 class Player
# ------------------------------------------------------

class Player:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        if self.zone_name not in constants.ZONE_NAMES: raise ValueError("Error")
        if self.map_name not in constants.MAP_NAMES: raise ValueError("Error")
        # ----
        player_info = utils.get_user_data()
        self.name = player_info["character_name"]
        # ----
        # self.init_pygame()
        self.inner = []
        self.image_counter = 0
        # ----
        # self.scale = 3
        # ----
        self.default_behavior = "stand"
        self.x, self.y = -1, -1
        self.keep_looping = True
        # ---- ---- ---- ----
        self.species = ""
        self.profession = ""
        self.max_hit_points = -1
        self.hit_points = -1
        self.constitution = -1
        self.attack_distance = -1
        self.maximum_damage = -1
        self.chance_to_hit = -1
        self.experience = -1
        self.gold = -1
        self.is_monster = False
        self.model_type = ""
        self.model_name = ""
        self.sheet_kinds = ""
        self.sheet_name = ""
        # ---- ----
        self.player_body = None  # current behavior: base, eat, etc.
        self.image_counter = 0
        self.movement_inc = 0.05
        self.random_walk = True
        self.health_counter = 0
        self.facing_direction = None
        # ---- ---- ---- ----
        self.inventory = None

    # --------------------------------------------------------

    def read_data(self):
        filename = "{}_player.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        self.x, self.y = utils.get_player_map_coords(filepath)
        # ----
        self.facing_direction = utils.get_player_direction(self.zone_name, self.map_name)
        # ---- ----
        self._read_player_data()
        self._validate_data()
        self._read_in_body()
        # self.inventory = Inventory("player")
        # self.inventory.read_data()

    def _read_player_data(self):
        filename = "{}_file.txt".format(self.name)
        self.player_file = os.path.join("data", "pc_files", self.name, filename)
        if os.path.isfile(self.player_file) == False:
            s = "This is not a valid file: {}".format(self.player_file)
            raise ValueError(s)
        # ----
        mydict = utils.read_file(self.player_file)[0]
        if mydict is None: raise ValueError("Error")
        # ----
        # self.name = player_name
        self.species = mydict["species"]
        self.profession = mydict["profession"]
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.constitution = mydict["constitution"]
        self.attack_distance = mydict["attack_distance"]
        self.maximum_damage = mydict["maximum_damage"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        self.gold = mydict["gold"]
        self.is_monster = mydict["is_monster"]
        self.model_type = mydict["model_type"]
        self.model_name = mydict["model_name"]
        self.sheet_kinds = mydict["sheet_kinds"]
        self.sheet_name = mydict["sheet_name"]

    def _validate_data(self):
        # if os.path.isfile(self.player_file) == False: raise ValueError("Error")
        # if utils.get_filepath(self.player_file) is None: raise ValueError("Error")
        # if not self.player_position in constants.DIRECTION_LIST:  # up, down, etc.
        #     s = "npc_position: {}".format(self.player_position)
        #     raise ValueError(s)
        # ---- ----
        if self.species not in constants.SPECIES:
            s = "I don't recognize this species: {}".format(self.species)
            raise ValueError(s)
        if self.profession not in constants.PROFESSIONS:
            s = "I don't recognize this profession: {}".format(self.profession)
            raise ValueError(s)
        if self.max_hit_points <= 0: raise ValueError("Error")
        if self.hit_points <= 0: raise ValueError("Error")
        if self.constitution <= 0: raise ValueError("Error")
        if self.attack_distance < 0: raise ValueError("Error")
        if self.maximum_damage < 0: raise ValueError("Error")
        if self.chance_to_hit < 0: raise ValueError("Error")
        if self.experience < 0: raise ValueError("Error")
        if self.gold < 0: raise ValueError("Error")
        if self.is_monster.lower() not in ["true", "false"]: raise ValueError("Error")
        self.is_monster = True if self.is_monster.lower() == True else False
        if self.model_type not in constants.MODEL_TYPES:
            raise ValueError("Not found: {}".format(self.model_type))
        if self.model_name not in constants.MODEL_NAMES:
            raise ValueError("Not found: {}".format(self.model_name))
        # ----
        mylist = self.sheet_kinds.split(",")
        self.sheet_kinds = [i.strip() for i in mylist if len(i.strip()) > 0]
        for elem in self.sheet_kinds:
            if not elem in constants.SHEET_KINDS:
                s = "I don't recognize this sheet kind: {}".format(elem)
                raise ValueError(s)
        if self.sheet_name not in constants.SHEET_KINDS: raise ValueError("Error")

    def _read_in_body(self):
        for sheet_kind in self.sheet_kinds:
            if self.model_type == "lpc":
                # print("sheet kind: {}".format(sheet_kind))
                myobject = LPCModel(self.model_name, sheet_kind, self.name, self.facing_direction)
                myobject.read_data()
                self.inner.append(myobject)
            elif self.model_type == "simple":
                raise NotImplemented
            # myobject = NPC_Behavior_SimpleModel(self.model_name, sheet_kind, self.animation_kind)
            # myobject.read_data()
            # self.inner.append(myobject)
            else:
                s = "I don't recognize this: {}".format(self.model_type)
                raise ValueError(s)
        if len(self.inner) == 0: raise ValueError("Error")
        self.change_behavior(self.default_behavior)

    def move(self, dx, dy, obstacles=None):
        if obstacles is None:
            temp_x = dx * self.movement_inc
            temp_y = dy * self.movement_inc
            self.x += temp_x
            self.y += temp_y
        # else:
        #     previous_x = self.x
        #     previous_y = self.y
        #     temp_x = dx * self.movement_inc
        #     temp_y = dy * self.movement_inc
        #     self.x += temp_x
        #     self.y += temp_y
        #     self.rect = self.player_body.image.get_rect()
        #     self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        #     col_result = pygame.sprite.spritecollideany(self, obstacles.inner, collided=None)
        #     if col_result is not None:
        #         print("Player encountered obstacle and therefore will not move.")
        #         # an obstacle was run into.
        #         # put critter back to previous position.
        #         self.x = previous_x
        #         self.y = previous_y
        #         self.rect = self.player_body.image.get_rect()
        #         self.rect = self.player_body.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        #         # self.change_direction(utils.get_random_direction())
        #         return False
        #     else:
        #         return True

    def move_left(self, obstacles=None):
        self.move(-1, 0, obstacles)

    def move_right(self, obstacles=None):
        self.move(1, 0, obstacles)

    def move_up(self, obstacles=None):
        self.move(0, -1, obstacles)

    def move_down(self, obstacles=None):
        self.move(0, 1, obstacles)

    def change_direction(self, new_direction):
        if new_direction not in constants.DIRECTION_VALUES:
            if not new_direction in ["up", "down"]:
                s = "I don't recognize this direction: {}".format(new_direction)
                raise ValueError(s)
        self.image_counter = 0
        # self.direction = new_direction
        self.facing_direction = new_direction
        if self.facing_direction in ["front", "down"]:
            self.player_body.change_direction("down")
        elif self.facing_direction in ["back", "up"]:
            self.player_body.change_direction("up")
        elif self.facing_direction == "right":
            self.player_body.change_direction("right")
        elif self.facing_direction == "left":
            self.player_body.change_direction("left")
        else:
            s = "I don't recognize this direction: {}".format(self.facing_direction)
            raise ValueError(s)

    def change_behavior(self, sheet_name):
        def get_a_sheet(the_name_of_the_sheet):
            if sheet_name == "idle": raise ValueError("Error")
            for elem in self.inner:
                if elem.sheet_name == the_name_of_the_sheet:
                    return elem
            return None
        # ---- ----
        self.player_body = get_a_sheet(sheet_name)
        if self.player_body == None:
            s = "It seems as though that behavior might\n"
            s += "not exist for this model: {}\n".format(sheet_name)
            s += ", ".join(self.sheet_kinds)
            raise ValueError(s)
        self.player_body.change_direction(self.facing_direction)
        self.sheet_name = self.player_body.sheet_name
        self.image_counter = 0
        print("player sheet name: {}".format(self.player_body.sheet_name))
        # ---- ----
        if self.sheet_name in ["walk", "base"]:
            self.move_player = True
        else:
            self.move_player = False
        # ---- ----
        self.player_body.update_class(self.x, self.y)
        if self.player_body.image is None:
            raise ValueError("Error")

    def update_class(self, all_sprites):
        if self.player_body is None: raise ValueError("Error")
        # ---- ----
        try:
            self.player_body.update_class(self.x, self.y)
        except Exception as e:
            t = "image_counter: {}; image_list_length: {}\n"
            t += "model_name: {}; direction_faced: {}"
            t = t.format(self.image_counter, len(self.player_body.image_list),
                         self.player_body.model_name, self.facing_direction)
            s = "{}\n{}".format(e, t)
            raise ValueError(s)
        # ---- ---- ---- ----
        all_sprites.add(self.player_body)

    # --------------------------------------------------------

    # def init_pygame(self):
    #     pygame.init()
    #     self.all_sprites = pygame.sprite.Group()
    #     self.font = pygame.font.Font(None, 30)
    #     self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    #     pygame.display.set_caption(constants.TITLE)
    #     self.clock = pygame.time.Clock()

# ------------------------------------------------------
#                 class PlayerDriver
# ------------------------------------------------------
class PlayerDriver:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        if self.zone_name not in constants.ZONE_NAMES: raise ValueError("Error")
        if self.map_name not in constants.MAP_NAMES: raise ValueError("Error")
        # ---- ----
        self.init_pygame()
        self.keep_looping = True
        self.player = None

    def read_data(self):
        self.player = Player(self.zone_name, self.map_name)
        self.player.read_data()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                # ----------------------------------------------
                elif event.key == pygame.K_UP:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("up")
                    self.player.move_up(None)
                elif event.key == pygame.K_DOWN:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("down")
                    self.player.move_down(None)
                elif event.key == pygame.K_RIGHT:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("right")
                    self.player.move_right(None)
                elif event.key == pygame.K_LEFT:
                    self.all_sprites = pygame.sprite.Group()
                    self.player.move_player = True
                    self.player.change_behavior("base")
                    self.player.change_direction("left")
                    self.player.move_left(None)
                # ==============================================
                elif event.key == pygame.K_h:
                    # interact with something in the environment
                    pass
                elif event.key == pygame.K_i:
                    # look at the convents of the player's backpack,
                    # their inventory
                    pass
            elif event.type == pygame.KEYUP:
                self.player.move_player = False
                self.player.change_behavior("stand")
                self.player.change_direction(self.player.facing_direction)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     x = pos[0] / constants.TILESIZE
            #     y = pos[1] / constants.TILESIZE
            #     print(pos)
            #     print(x, y)

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        self.clock = pygame.time.Clock()

    def think(self):
        if len(self.player.facing_direction) == 0: return False
        if self.player.move_player == True:
            if self.player.facing_direction == "right":
                self.player.move_right(None)
            elif self.player.facing_direction == "left":
                self.player.move_left(None)
            elif self.player.facing_direction in ["front", "up"]:
                self.player.move_up(None)
            elif self.player.facing_direction in ["back", "down"]:
                self.player.move_down(None)
            else:
                s = "I don't recognize this: -{}-".format(self.player.facing_direction)
                raise ValueError(s)

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        self.player.update_class(self.all_sprites)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.clock.tick(12)
            self.handle_events()
            self.think()
            self.draw()

# *************************************************************
# *************************************************************

def main():
    zone_name = "docks"
    map_name = "map00"
    myclass = PlayerDriver(zone_name, map_name)
    myclass.read_data()
    myclass.main()

if __name__ == "__main__":
    main()
