import time
import pygame
import constants
import utils
import os
import random

# -----------------------------------------------------------
#                      class Npc (The Parent Class)
# -----------------------------------------------------------
class Npc(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        print("class NewNPC.__init__-->mydict:")
        print("mydict: {}".format(mydict))
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"].lower().strip()
        self.species = mydict["species"]
        if not self.species in constants.SPECIES:
            s = "Error! {} is not in {}".format(self.species, constants.SPECIES)
            raise ValueError(s)
        self.profession = mydict["profession"]
        if not self.profession in constants.NPC_PROFESSIONS:
            s = "Error! {} is not in {}".format(self.profession, constants.NPC_PROFESSIONS)
            raise ValueError(s)
        # the function field will conroll which class is used to create an NPC child object
        self.function = mydict["function"]
        if not self.function in constants.NPC_FUNCTION:
            s = "{} is not a constant in NPC_FUNCTION\n".format(self.function.upper())
            s += ", ".join(constants.NPC_FUNCTION)
            raise ValueError(s)
        self.gold = int(mydict["gold"])
        if self.gold < 0: raise ValueError("Error")
        self.attack_distance = mydict["attack_distance"]
        # ----
        self.inventory_type = mydict["inventory_type"]
        # ----
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.agro_level = mydict["agro_level"]
        if not self.agro_level in constants.AGRO_LEVEL:
            raise ValueError("Error!")
        self.maximum_damage = mydict["maximum_damage"]
        self.chance_to_hit = mydict["chance_to_hit"]
        if not ((self.chance_to_hit >= 0) and (self.chance_to_hit <= 100)):
            s = "Error! Chance to hit must be between 0 and 100, inclusive."
            raise ValueError(s)
        self.experience = mydict["experience"]
        self.model_name = mydict["model_name"]
        self.on_contact = mydict["on_contact"]
        # ----
        self.destination_point_x = mydict["destination_point_x"]
        self.destination_point_y = mydict["destination_point_y"]
        if not utils.is_int(self.destination_point_x):
            self.destination_point_x = self.destination_point_x.lower().strip()
        if not utils.is_int(self.destination_point_y):
            self.destination_point_y = self.destination_point_y.lower().strip()
        if self.destination_point_x == "none": self.destination_point_x = None
        if self.destination_point_y == "none": self.destination_point_y = None
        # self.destination_point_x = int(mydict["destination_point_x"])
        # self.destination_point_y = int(mydict["destination_point_y"])
        # print("debugging ***********")
        # print("debugging: destination_point_x: {}, destination_point_y: {}".format(self.destination_point_x, self.destination_point_y))
        # raise NotImplemented
        # ----
        if not self.on_contact in constants.CONTACT_KINDS:
            raise ValueError("Error")
        if not self.model_name in constants.NPC_MODEL_NAMES:
            s = "model_name ({}) is not in {}".format(self.model_name, constants.NPC_MODEL_NAMES)
            raise ValueError(s)
        self.command = None
        # -------------------
        # ---- Images ----
        # -------------------
        s = os.path.join("data", "images", "npc_models", self.model_name, "down.png")
        if os.path.isfile(s) == False:
            s = "Error! I can't find this file: {}".format(s)
            raise ValueError(s)
        self.image_down = pygame.image.load(s).convert_alpha()
        self.image_down = pygame.transform.scale(self.image_down, (constants.TILESIZE, constants.TILESIZE))
        s = os.path.join("data", "images", "npc_models", self.model_name, "left.png")
        if os.path.isfile(s) == False:
            s = "Error! I can't find this file: {}".format(s)
            raise ValueError(s)
        self.image_left = pygame.image.load(s).convert_alpha()
        self.image_left = pygame.transform.scale(self.image_left, (constants.TILESIZE, constants.TILESIZE))
        s = os.path.join("data", "images", "npc_models", self.model_name, "up.png")
        if os.path.isfile(s) == False:
            s = "Error! I can't find this file: {}".format(s)
            raise ValueError(s)
        self.image_up = pygame.image.load(s).convert_alpha()
        self.image_up = pygame.transform.scale(self.image_up, (constants.TILESIZE, constants.TILESIZE))
        s = os.path.join("data", "images", "npc_models", self.model_name, "right.png")
        if os.path.isfile(s) == False:
            s = "Error! I can't find this file: {}".format(s)
            raise ValueError(s)
        self.image_right = pygame.image.load(s).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (constants.TILESIZE, constants.TILESIZE))
        filepath_dead = utils.get_filepath("skull_and_bones.png")
        self.image_dead = pygame.image.load(filepath_dead).convert_alpha()
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))
        s = utils.get_filepath("apple_tree_full.png")
        self.image_testing = pygame.image.load(s).convert_alpha()
        self.image_testing = pygame.transform.scale(self.image_testing, (constants.TILESIZE, constants.TILESIZE))
        # ----
        self.initial_position = mydict["npc_position"]
        print(self.initial_position)
        if not self.initial_position in ["up", "down", "right", "left"]:
            raise ValueError("Error!")
        if self.initial_position == "up":
            self.image = self.image_up
        elif self.initial_position == "down":
            self.image = self.image_down
        elif self.initial_position == "right":
            self.image = self.image_right
        elif self.initial_position == "left":
            self.image = self.image_left
        # print(self.image_up)
        # ----
        s = utils.get_filepath("skull_and_bones.png")
        self.image_dead = pygame.image.load(s).convert_alpha()
        self.rect = None
        # ----
        s = mydict["is_monster"].lower().strip()
        self.is_monster = True if s=="true" else False
        self.comment = ""
        # ----
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # ----
        self.image_dead = pygame.transform.scale(self.image_dead, (constants.TILESIZE, constants.TILESIZE))
        # ----
        self.alternate_increment = 0.25

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def is_a_questgiver(self, zone_name, map_name):
        filename = "{}_quest.txt".format(self.name).replace(" ", "_")
        filepath = os.path.join("data", "zones", zone_name, map_name, "texts", filename)
        if utils.is_file(filepath) == True:
            return True
        return False

    # ----

    def is_involved_in_a_quest(self, quests):
        this_quest = quests.get_quest_by_npc_name(self.name)
        if this_quest is None:
            return False
        return True

    # ----

    def get_fileline(self):
        s = "name: {}\nfunction: {}\nspecies: {}\nprofession: {}\n".format(self.name, self.function, self.species, self.profession)
        s += "max_hit_points: {}\nhit_points: {}\n".format(self.max_hit_points, self.hit_points)
        s += "agro_level: {}\nattack_distance:{}\n".format(self.agro_level, self.attack_distance)
        s += "maximum_damage: {}\nchance_to_hit: {}\n".format(self.maximum_damage, self.chance_to_hit)
        s += "experience: {}\n".format(self.experience)
        s += "gold: {}\ninventory_type: {}\n".format(self.gold, self.inventory_type)
        s += "is_monster: {}\nmodel_name: {}\n".format(self.is_monster, self.model_name)
        # s += "destination_point_x: {}\n".format(self.destination_point_x)
        # s += "destination_point_y: {}\n".format(self.destination_point_y)
        return s

    def move(self, dx=0, dy=0, obstacles=None):
        new_x = self.x + dx
        new_y = self.y + dy
        if obstacles.collision(new_x, new_y) == False:
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    # def move_alternate(self, dx=0.0, dy=0.0, obstacles=None):
    #     new_x = self.x + dx
    #     new_y = self.y + dy
    #     if obstacles.collision(new_x, new_y) == False:
    #         self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
    #         self.x += dx
    #         self.y += dy
    #         return True
    #     else:
    #         return False

    def move_alternate(self, dx=0.0, dy=0.0, obstacles=None):
        new_x = self.x + dx
        new_y = self.y + dy
        if obstacles.collision_is_close(new_x, new_y) == False:
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def move_right(self, obstacles=None):
        dx, dy = -1, 0
        if self.move(dx, dy, obstacles) == True:
            self.image = self.image_left
            return True
        else:
            return False

    def move_right_alternative(self, obstacles=None):
        # dx, dy = -0.5, 0.0
        dx, dy = self.alternate_increment * -1.0, 0.0
        if self.move_alternate(dx, dy, obstacles) == True:
            self.image = self.image_left
            return True
        else:
            return False

    def move_left(self, obstacles=None):
        dx, dy = 1, 0
        if self.move(dx, dy, obstacles) == True:
            # self.image = self.image_left
            self.image = self.image_right
            # self.image = self.image_testing
            return True
        else:
            return False

    def move_left_alternate(self, obstacles=None):
        # dx, dy = 0.5, 0.0
        dx, dy = self.alternate_increment, 0.0
        if self.move_alternate(dx, dy, obstacles) == True:
            # self.image = self.image_left
            self.image = self.image_right
            # self.image = self.image_testing
            return True
        else:
            return False

    def move_down(self, obstacles=None):
        dx, dy = 0, 1
        if self.move(dx, dy, obstacles) == True:
            self.image = self.image_down
            return True
        else:
            return False

    def move_down_alternate(self, obstacles=None):
        dx, dy = 0.0, 0.5
        dx, dy = 0.0, self.alternate_increment
        if self.move_alternate(dx, dy, obstacles) == True:
            self.image = self.image_down
            return True
        else:
            return False

    def move_up(self, obstacles=None):
        dx, dy = 0, -1
        if self.move(dx, dy, obstacles) == True:
            self.image = self.image_up
            # self.image = self.image_testing
            return True
        else:
            return False

    def move_up_alternate(self, obstacles=None):
        # dx, dy = 0.0, -0.5
        dx, dy = 0.0, self.alternate_increment * -1.0
        if self.move_alternate(dx, dy, obstacles) == True:
            self.image = self.image_up
            # self.image = self.image_testing
            return True
        else:
            return False

    def move_random(self, obstacles):
        print("obstacles: {}".format(obstacles))
        if obstacles is None: raise ValueError("Error")
        if len(obstacles) == 0: ValueError("Error")
        # ----
        def random_move():
            myran = random.randint(0, 3)
            if myran == 0:
                return self.move_up(obstacles)
            elif myran == 1:
                return self.move_down(obstacles)
            elif myran == 2:
                return self.move_right(obstacles)
            elif myran == 3:
                return self.move_left(obstacles)
            else:
                raise ValueError("Error")
        # ----
        be_safe = 0
        it_worked = False
        while it_worked == False:
            it_worked = random_move()
            be_safe += 1
            if be_safe > 1000:
                raise ValueError("Error")
        print(self.x, self.y)
        return True

    def move_random_alternate(self, obstacles):
        print("obstacles: {}".format(obstacles))
        if obstacles is None: raise ValueError("Error")
        if len(obstacles) == 0: ValueError("Error")
        # ----
        def random_move():
            myran = random.randint(0, 3)
            if myran == 0:
                return self.move_up_alternate(obstacles)
            elif myran == 1:
                return self.move_down_alternate(obstacles)
            elif myran == 2:
                return self.move_right_alternative(obstacles)
            elif myran == 3:
                return self.move_left_alternate(obstacles)
            else:
                raise ValueError("Error")
        # ----
        be_safe = 0
        it_worked = False
        while it_worked == False:
            it_worked = random_move()
            be_safe += 1
            if be_safe > 1000:
                raise ValueError("Error")
        print(self.x, self.y)

    def move_toward(self, x, y, obstacles):
        if type(x) != type(123):
            s = "This isn't type integer, and it SHOULD be: {} ({})".format(x, type(x))
            raise ValueError(s)
        if type(y) != type(123):
            raise ValueError("Error")
        # ----
        # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        if self.x == x and self.y == y:
            print("The NPC ({},{}) has reached its destination: ({},{})".format(self.x, self.y, x, y))
            return True
        # else:
        #     time.sleep(1)
        print("The NPC (h{}) ({},{}) has not reached its desired location ({},{}).".format(self.name, self.x, self.y, x, y))
        if self.x == x and self.y != y:
            if self.y - y < 0:
                if self.move_down(obstacles) == False:
                    # self.image = self.image_down
                    if self.move_random(obstacles=obstacles) == False:
                        pass
            else:
                if self.move_up(obstacles) == False:
                    # self.image = self.image_up
                    if self.move_random(obstacles=obstacles) == False:
                        pass
        elif self.x != x and self.y == y:
            if (self.x - x) < 0:
                if self.move_left(obstacles) == False:
                    # self.image = self.image_left
                    if self.move_random(obstacles=obstacles) == False:
                        pass
            else:
                if self.move_right(obstacles) == False:
                    # self.image = self.image_right
                    if self.move_random(obstacles=obstacles) == False:
                        pass
        elif self.x !=x and self.y != y:
            myrand = random.randint(0, 1)
            if myrand == 0:
                if self.y - y < 0:
                    if self.move_down(obstacles) == False:
                        # self.image = self.image_down
                        if self.move_random(obstacles=obstacles) == False:
                            pass
                else:
                    if self.move_up(obstacles) == False:
                        # self.image = self.image_up
                        if self.move_random(obstacles=obstacles) == False:
                            pass
            # ----
            elif myrand == 1:
                if (self.x - x) < 0:
                    if self.move_left(obstacles) == False:
                        if self.move_random(obstacles=obstacles) == False:
                            pass
                else:
                    if self.move_right(obstacles) == False:
                        if self.move_random(obstacles=obstacles) == False:
                            pass
            else:
                raise ValueError("Error!")
        else:
            raise ValueError("Error!")
        return False

    def move_toward_alternate(self, player_x, player_y, obstacles):
        def move_random():
            if obstacles.collision_is_close(self.x, self.y) == True:
                # self.image = self.image_up
                if self.move_random_alternate(obstacles=obstacles) == False:
                    pass
        # ----
        if type(player_x) != type(123) and type(player_x) != type(0.0):
            s = "This isn't type integer or float, and it should be: {} ({})".format(x, type(x))
            raise ValueError(s)
        if type(player_y) != type(123) and type(player_y) != type(0.0):
            raise ValueError("Error")
        # ----
        # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        if utils.points_are_close(self.x, player_x) == True and utils.points_are_close(self.y, player_y) == True:
            print("The NPC ({},{}) has reached its destination: ({},{})".format(self.x, self.y, player_x, player_y))
            return True
        s = "The NPC ({}) ({},{}) has not reached its desired location ({},{})."
        s = s.format(self.name, self.x, self.y, player_x, player_y)
        print(s)
        if utils.points_are_close(self.x, player_x) == True and utils.points_are_close(self.y, player_y) == False:
            # npc_y = self.y
            if (self.y - player_y) < 0:
                if self.move_down_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
            else:
                if self.move_up_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
        elif utils.points_are_close(self.x, player_x) == False and utils.points_are_close(self.y, player_y) == True:
            # npc_x = self.x
            if (self.x - player_x) < 0:
                if self.move_left_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
            else:
                if self.move_right_alternative(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
        elif utils.points_are_close(self.x, player_x) == False and utils.points_are_close(self.y, player_y) == False:
        # elif self.x !=x and self.y != y:
            myrand = random.randint(0, 1)
            if myrand == 0:
                if self.y - player_y < 0:
                    if self.move_down_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
                else:
                    if self.move_up_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
            # ----
            elif myrand == 1:
                if (self.x - player_x) < 0:
                    if self.move_left_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
                else:
                    if self.move_right_alternative(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
            else:
                raise ValueError("Error!")
        else:
            raise ValueError("Error!")
        return False

    def move_away(self, point_x, point_y, obstacles):
        def move_random():
            if obstacles.collision_is_close(self.x, self.y) == True:
                # self.image = self.image_up
                if self.move_random_alternate(obstacles=obstacles) == False:
                    pass
        # ----
        if type(point_x) != type(123) and type(point_x) != type(0.0):
            s = "This isn't type integer or float, and it should be: {} ({})".format(point_x, type(point_x))
            raise ValueError(s)
        if type(point_y) != type(123) and type(point_y) != type(0.0):
            s = "This isn't type integer or float, and it should be: {} ({})".format(point_y, type(point_y))
            raise ValueError(s)
        # ----
        # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
        if utils.points_are_close(self.x, point_x) == True and utils.points_are_close(self.y, point_y) == True:
            print("The NPC ({},{}) has reached its destination: ({},{})".format(self.x, self.y, point_x, point_y))
            return True
        s = "The NPC ({}) ({},{}) has not reached its desired location ({},{})."
        s = s.format(self.name, self.x, self.y, point_x, point_y)
        print(s)
        if utils.points_are_close(self.x, point_x) == True and utils.points_are_close(self.y, point_y) == False:
            # npc_y = self.y
            if (self.y - point_y) < 0:
                if self.move_down_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
            else:
                if self.move_up_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
        elif utils.points_are_close(self.x, point_y) == False and utils.points_are_close(self.y, point_y) == True:
            # npc_x = self.x
            if (self.x - point_x) < 0:
                if self.move_left_alternate(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
            else:
                if self.move_right_alternative(obstacles) == False:
                    self.move_random_alternate(obstacles=obstacles)
        elif utils.points_are_close(self.x, point_x) == False and utils.points_are_close(self.y, point_y) == False:
        # elif self.x !=x and self.y != y:
            myrand = random.randint(0, 1)
            if myrand == 0:
                if self.y - point_y < 0:
                    if self.move_down_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
                else:
                    if self.move_up_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
            # ----
            elif myrand == 1:
                if (self.x - point_x) < 0:
                    if self.move_left_alternate(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
                else:
                    if self.move_right_alternative(obstacles) == False:
                        self.move_random_alternate(obstacles=obstacles)
            else:
                raise ValueError("Error!")
        else:
            raise ValueError("Error!")
        return False

    def has_caught(self, x, y):
        if self.x == x and self.y == y: return True
        return False

    def calculate_damage(self, a_player):
        # This is just a thumbnail. In a future version of this program
        # the amount of damage received will depend on
        # - the strength of the attacker
        # - the amount of damage the weapon can deliver
        # - the quality of shielding the attacked has
        return self.maximum_damage

    def save_data(self):
        ud = utils.get_user_data()
        filename = "{}.txt".format(self.name)
        filepath = os.path.join("data", "playing_characters", ud["character_name"], "npcs", filename)
        with open(filepath, "w") as f:
            s = self.get_fileline()
            if len(s.strip()) == 0:
                raise ValueError("Error!")
            f.write(self.get_fileline())

    def debug_print(self):
        s = "x,y: ({},{})\nname: {}, function: {}, species: {}, profession: {}\n"
        s = s.format(self.x, self.y, self.name, self.function, self.species, self.profession)
        s += "gold: {}, inventory_type: {}\n".format(self.gold, self.inventory_type)
        s += "max_hit_points: {}, hit_points: {}, agro_level: {}, is_monster: {}\n".format(self.max_hit_points, self.hit_points, self.agro_level, self.is_monster)
        s += "maximum_damage: {}, chance_to_hit: {}, experience: {}\n".format(self.maximum_damage, self.chance_to_hit, self.experience)
        s += "is_monster: {}, on_contact: {},\n".format(self.is_monster, self.on_contact)
        s += "destination_point_x: {}, destination_point_y: {}\n".format(self.destination_point_x, self.destination_point_y)
        s += "comment: {}".format(self.on_contact)
        print(s)