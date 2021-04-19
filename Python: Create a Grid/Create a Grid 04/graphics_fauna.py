import os, sys
import pygame
import utils
import constants
import random

# -----------------------------------------------------------
#                      class Player
# -----------------------------------------------------------
"""
As you can see, class Player uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.direction = constants.DOWN
        # ---------------------------------------------
        self.maximum_damage = 2
        self.max_hit_points = -1
        self.hit_points = -1
        self.chance_to_hit = -1
        self.experience = -1
        # ---------------------------------------------
        x, y = utils.get_players_position_on_map()
        self.x = x
        self.y = y
        # ---------------------------------------------
        filepath = os.path.join("data/images", constants.PLAYER_IMG)
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        filepath = os.path.join("data/images", constants.PLAYER_IMG_DEAD)
        self.image_dead = pygame.image.load(filepath).convert_alpha()
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def read_data_first(self):
        # print("mydict: {}".format(mydict))
        path = os.path.join("data", constants.PLAYER_DATA_FILE)
        # print("path: {}".format(path))
        mylist = utils.read_data_file(path, num_of_fields=9)
        mydict = mylist[0]
        # print("mydict: {}".format(mydict))
        # ----
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        if utils.is_int(mydict["direction"]) == True:
            self.direction = int(mydict["direction"])
        else:
            self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ----
        # Check players location from the file against their
        # location on the map.
        # ----
        filepath = os.path.join("data", constants.MAPFILE)
        player_x, player_y = utils.get_player_position_from_map(filepath)
        # print("player x,y: {},{}".format(player_x, player_y))
        if not (player_x == self.x and player_y == self.y):
            s = "The player's coords don't match!\n"
            s += "Position from map: player_x, player_y: {},{}\n".format(player_x, player_y)
            s += "self.x, self.y: {},{}".format(self.x, self.y)
            raise ValueError(s)

    def read_data_restart(self):
        # print("mydict: {}".format(mydict))
        path = os.path.join("data", constants.PLAYER_DATA_FILE)
        # print("path: {}".format(path))
        mylist = utils.read_data_file(path, num_of_fields=9)
        mydict = mylist[0]
        print("mydict: {}".format(mydict))
        # ----
        self.x = mydict["x"]
        print("this is x: {}".format(self.x))
        self.y = mydict["y"]
        print("this is y: {}".format(self.y))
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        if utils.is_int(mydict["direction"]) == True:
            self.direction = int(mydict["direction"])
        else:
            self.direction = utils.convert_direction_to_integer(mydict["direction"])
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ----
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        self.direction = "DOWN"

    def calculate_damage(self):
        return self.maximum_damage

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def get_fileline(self):
        s = "x: {}\ny: {}\nname: {}\nkind: {}\ndirection: {}\nmax_hit_points: {}\nhit_points: {}\nchance_to_hit: {}\nexperience: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.direction, self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        return s

    def save_data(self):
        s = self.get_fileline()
        filepath = os.path.join("data", constants.PLAYER_DATA_FILE)
        with open(filepath, "w") as f:
            f.write(s)

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def _collide_with_walls(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def move(self, dx=0, dy=0, walls=None):
        if not self._collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            # print("Player has moved. x,y: {},{}; dx={}, dy={}".format(self.x, self.y, dx, dy))

    def debug_print(self):
        title = " The Player "
        print("-" * 10, title, '-' * 10)
        s = "x,y: ({},{}); name: {}; kind: {}; direction: {}; max_hit_points: {}; hit_points: {}; chance_to_hit: {}; experience: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.direction, self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        print(s)
        print("-" * (20 + len(title)))

# -----------------------------------------------------------
#                      class Monster
# -----------------------------------------------------------
"""
As you can see, class Monster uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.max_hit_points = -1
        self.hit_points = -1
        # ---------------------------------------------
        self.maximum_damage = 4
        self.chance_to_hit = -1
        self.experience = -1
        # ---------------------------------------------
        self.image = None
        self.image_dead_monster = None
        self.rect = None
        # ---------------------------------------------

    def read_data(self):
        filepath = os.path.join("data", constants.MONSTERS_DATA_FILE)
        number_of_fields = 8
        mylist = utils.read_data_file(filepath, number_of_fields)
        mydict = mylist[0]
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ---------------------------------------------
        filepath = os.path.join("data", "images", constants.MONSTER_IMG)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ---------------------------------------------
        filepath = os.path.join("data", "images", constants.MONSTER_IMG_DEAD)
        self.image_dead_monster = pygame.image.load(filepath).convert_alpha()
        self.image_dead_monster = pygame.transform.scale(self.image_dead_monster, (constants.TILESIZE, constants.TILESIZE))

    def calculate_damage(self):
        return self.maximum_damage

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * constants.TILESIZE, new_y * constants.TILESIZE)

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def collide_with_walls(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def check_for_collision(self, dx, dy, walls):
        if not self.collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            print("Monster has moved. x,y: {},{}. dx={}, dy={}".format(self.x, self.y, dx, dy))

    def move(self, walls):
        myran = random.randint(0, 4)
        if myran == 0:
            self.check_for_collision(0, 1, walls)
        elif myran == 1:
            self.check_for_collision(1, 0, walls)
        elif myran == 2:
            self.check_for_collision(0, -1, walls)
        elif myran == 3:
            self.check_for_collision(-1, 0, walls)
        elif myran == 4:
            pass
        else:
            raise ValueError("Error!")

    def monster_tries_to_hit_player(self, player):
        myran = random.randint(1, 100)
        if myran <= self.chance_to_hit:
            return True
        else:
            return False

    def get_fileline(self):
        s = "x: {}\ny: {}\nname: {}\nkind: {}\nmax_hit_points: {}\nhit_points: {}\nchance_to_hit: {}\nexperience: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        return s

    def save_data(self):
        filepath = os.path.join("data", constants.MONSTERS_DATA_FILE)
        fileline = self.get_fileline()
        with open(filepath, "w") as f:
            f.write(fileline)

    def debug_print(self):
        s = "Debug Print Monster"
        print("-" * 10, s, "-" * 10)
        # print("filepath: {}".format(self.filepath))
        print("monster name: {}; monster kind: {}".format(self.name, self.kind))
        print("x,y: {},{}".format(self.x, self.y))
        print("max_hp: {}; hp: {}; chance_to_hit: {}; exp: {}".format(self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience))
        print(("-" * (len(s) + 20 + 2)))

# -----------------------------------------------------------
#                      class Monsters
# -----------------------------------------------------------
# class Monsters:
#     def __init__(self):
#         pass