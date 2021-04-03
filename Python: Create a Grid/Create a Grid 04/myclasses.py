import pygame
import constants
from constants import TILESIZE
import sys, os
import random
import math
import utils
from dialogs import DialogFight
from shutil import copyfile

# ----------------------------------------------------------------
#                           class Player
# ----------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = -1
        self.y = -1
        self.name = ""
        self.kind = ""
        self.direction = constants.DOWN
        # ---------------------------------------------
        self.max_hit_points = -1
        self.hit_points = -1
        self.chance_to_hit = -1
        self.experience = -1
        # ---------------------------------------------
        x, y = utils.get_players_position_on_map()
        self.x = x
        self.y = y
        # ---------------------------------------------
        # self.read_data()
        # ---------------------------------------------
        filepath = os.path.join("data/images", constants.PLAYER_IMG)
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
        # ---------------------------------------------
        try:
            self.image_healthy = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG))
            raise ValueError(s)
        self.image_healthy = pygame.transform.scale(self.image_healthy, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        try:
            self.image_q1 = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG_q1)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG_q1))
            raise ValueError(s)
        self.image_q1 = pygame.transform.scale(self.image_q1, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        try:
            self.image_q2 = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG_q2)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG_q2))
            raise ValueError(s)
        self.image_q2 = pygame.transform.scale(self.image_q2, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        try:
            self.image_q3 = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG_q3)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG_q3))
            raise ValueError(s)
        self.image_q3 = pygame.transform.scale(self.image_q3, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        try:
            self.image_q4 = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG_q4)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG_q4))
            raise ValueError(s)
        self.image_q4 = pygame.transform.scale(self.image_q4, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        try:
            self.image_q5 = pygame.image.load(os.path.join("data/images", constants.PLAYER_IMG_q5)).convert_alpha()
        except:
            s = "Couldn't open {}".format(os.path.join("data/images", constants.PLAYER_IMG_q5))
            raise ValueError(s)
        self.image_q5 = pygame.transform.scale(self.image_q5, (TILESIZE, TILESIZE))
        # ---------------------------------------------
        # print("debugging: player: {},{}".format(self.x * TILESIZE, self.y * TILESIZE))
        # print("debugging: player: {},{}".format(self.x, self.y))

    def read_data(self):
        # print("mydict: {}".format(mydict))
        path = os.path.join("data", constants.PLAYER_DATA_FILE)
        print("path: {}".format(path))
        mylist = utils.read_data_file(path, num_of_fields=9)
        mydict = mylist[0]
        # ----
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
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
        print("player x,y: {},{}".format(player_x, player_y))
        if not (player_x == self.x and player_y == self.y):
            s = "The player's coords don't match!\n"
            s += "player_x, player_y: {},{}\n".format(player_x, player_y)
            s += "self.x, player.y: {},{}".format(self.x, self.y)
            raise ValueError(s)
        # else:
        #     print("Corrds match!")
        # raise NotImplemented

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * TILESIZE, new_y * TILESIZE)

    def in_fight_set_image(self):
        n, range1, range2, range3, range4 = utils.get_ranges(number_of_max_hit_points=self.max_hit_points,
                                                             number_of_quadrants=4)
        # print(n, range1, range2, range3, range4)
        if self.hit_points in n:
            self.image = utils.orient_image(self.image, self.direction)
        elif self.hit_points in range1:
            self.image = utils.orient_image(self.image_q1, self.direction)
        elif self.hit_points in range2:
            self.image = utils.orient_image(self.image_q2, self.direction)
        elif self.hit_points in range3:
            self.image = utils.orient_image(self.image_q3, self.direction)
        elif self.hit_points in range4:
            self.image = utils.orient_image(self.image_q4, self.direction)
        elif self.hit_points <= 0:
            self.image = utils.orient_image(self.image_q5, self.direction)
        else:
            raise ValueError("Something has gone wrong.")

    def is_dead(self):
        if self.hit_points <= 0: return True
        return False

    def move(self, dx=0, dy=0, walls=None):
        if not self.collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * TILESIZE, dy * TILESIZE)
            print("Player has moved. x,y: {},{}; dx={}, dy={}".format(self.x, self.y, dx, dy))

    def collide_with_walls(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def player_tries_to_hit_monster(self, monster):
        print("---- player_tires_to_hit_monster ----")
        print("Player ({} the {}) tries to hit monster ({} the {})".format(self.name, self.kind, monster.name, monster.kind))
        myran = random.randint(1, 100)
        print("random number: {}; chance_to_hit: {}".format(myran, self.chance_to_hit))
        if myran <= self.chance_to_hit:
            print("player HITS monster!")
            return True
        else:
            print("player MISSES monster.")
            return False

    def save_data(self):
        s = "x: {}\ny: {}\nname: {}\nkind: {}\ndirection: {}\nmax_hit_points: {}\nhit_points: {}\nchance_to_hit: {}\nexperience: {}"
        s = s.format(self.x, self.y, self.name, self.kind, utils.convert_direction(self.direction), self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        filepath = os.path.join("data", constants.PLAYER_DATA_FILE_TESTING)
        with open(filepath, "w") as f:
            f.write(s)

    def debug_print(self):
        mytext = "Debugging PLAYER"
        counter = 10
        print("-" * counter, mytext, "-" * counter)
        s = "x,y: ({},{}) | direction: {} | name: {}; kind: {}\nmax_hp: {}; hp: {}; chance to hit: {}; exp: {}"
        s = s.format(self.x, self.y, utils.convert_direction(self.direction), self.name, self.kind,
                     self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        print(s)
        print("-" * ((counter * 2) + 2 + len(mytext)))

# ----------------------------------------------------------------
#                           class Game
# ----------------------------------------------------------------

class Game:
    def __init__(self):
        self.init_pygame()
        self.keep_looping = True
        self.grasses = Grasses()
        self.walls = Walls()
        self.monsters = Monsters()
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        # ----------------------------------------
        self.fight = False
        # ----------------------------------------
        # Copy original file over to the temp file
        # The temp file can be altered and will only
        # last for the course of the game.
        # ----------------------------------------
        source_file = os.path.join("data", constants.MONSTERS_ORIGINAL_DATA_FILE)
        destination_file = os.path.join("data", constants.MONSTERS_DATA_FILE)
        copyfile(source_file, destination_file)
        # ---- debugging ----
        # self.player.debug_print()

    def restart_game(self):
        self.init_pygame()
        self.keep_looping = True
        self.grasses = Grasses()
        self.walls = Walls()
        self.monsters = Monsters()
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.fight = False
        # ----------------------------------------
        self.read_data()

    def read_data(self):
        self.player.read_data()
        self.monsters.read_data()

    def get_monster(self, x, y):
        monster = self.monsters.get_object(x, y)
        if monster is None:
            return None
        elif len(monster) == 0:
            return None
        elif len(monster) > 1:
            raise ValueError("Did you want to code for this?")
        else:
            return monster[0]

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.display_surface = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        # self.display_surface.fill(self.background_color)
        self.font = pygame.font.Font(None, 40)

    def there_is_a_monster_on_this_tile(self, x, y):
        this_monster = self.get_monster(x, y)
        if not this_monster is None:
            # this_monster.debug_print()
            # print("OMG!! IT'S A MONSTER!!!! 🙀")
            return True
        return False

    def dialog_have_a_fight(self):
        # get the monster that shares a tile with the player.
        this_monster = self.monsters.get_object(self.player.x, self.player.y)
        if len(this_monster) != 1:
            raise ValueError("Something has gone wrong! {} monsters were returned.".format(len(this_monster)))
        this_monster = this_monster[0]
        fight_dialog = DialogFight(self.player, this_monster)
        message = fight_dialog.main()
        # ----
        print("DEBUGGING: Monster after fight <-------------------")
        this_monster.debug_print()
        print("DEBUGGing ALL monsters <=================")
        self.monsters.debug_print()
        if this_monster.is_dead() == True:
            this_monster.image = this_monster.image_dead_monster
            print("Monster is dead!!")
        # raise NotImplemented
        # -----------------------------------------
        print("message: {}".format(message))
        self.monsters.save_data_to_temp_file()

        # self.monsters.debug_print()
        # self.monsters.update_monster(updated_monster_dict)
        # self.monsters.debug_print()
        # ----
        # self.player.resize(constants.TILESIZE, self.player.x, self.player.y)
        # self.monsters[0].resize(constants.TILESIZE, this_monster.x, this_monster.y)

    def have_a_fight(self):
        this_monster = self.get_monster(self.player.x, self.player.y)
        if this_monster is None:
            print("Player swings at nothing!!")
        else:
            # player gets the inititive by default.
            # player_hits = self.player.player_tries_to_hit_monster(this_monster)
            # if player_hits == True:
            #     this_monster.hit_points -= 1
            # if this_monster.is_dead() == True:
            #     self.fight = False
            #     self.player.experience += 1
            # ----
            monster_hits = this_monster.monster_tries_to_hit_player(self.player)
            if monster_hits == True:
                print("Monster tries to hit player and SUCCEEDS")
                self.player.hit_points -= 1
                self.player.in_fight_set_image()
            else:
                print("Monster tries to hit player and FAILS")
            if self.player.is_dead() == True:
                self.fight = False
                self.keep_looping = False
                print("Player has DIED!!!! 💀")
                self.keep_looping = False
        print("--- Debugging in handle_events in class Game ----")
        self.player.debug_print()
        self.monsters.debug_print()

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.myquit()
                return True
            if event.type == pygame.KEYDOWN:
                print("in fight: {}".format(self.fight))
                # self.move_monster()
                if event.key == pygame.K_ESCAPE:
                    self.myquit()
                    return True
                if event.key == pygame.K_LEFT:
                    if self.fight == True:
                        return False
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
                    if self.fight == True:
                        return False
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
                    if self.fight == True:
                        return False
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
                    if self.fight == True:
                        return False
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
                    print("Fight!!!")
                    self.dialog_have_a_fight()
                    # self.have_a_fight()
                elif event.key == pygame.K_t:
                    # testing/debugging
                    print("=" * 8, "Testing", "=" * 8)
                    self.player.hit_points -= 1
                    print("Player direction: {}".format(utils.convert_direction(self.player.direction)))
                    print("player's hit points: {}".format(self.player.hit_points))
                    n, range1, range2, range3, range4 = utils.get_ranges(number_of_max_hit_points=self.player.max_hit_points, number_of_quadrants=4)
                    print(n, range1, range2, range3, range4)
                    if self.player.hit_points in n:
                        self.player.image = utils.orient_image(self.player.image, self.player.direction)
                        # self.player.image_healthy
                    elif self.player.hit_points in range1:
                        self.player.image = utils.orient_image(self.player.image_q1, self.player.direction)
                    elif self.player.hit_points in range2:
                        self.player.image = utils.orient_image(self.player.image_q2, self.player.direction)
                    elif self.player.hit_points in range3:
                        self.player.image = utils.orient_image(self.player.image_q3, self.player.direction)
                    elif self.player.hit_points in range4:
                        self.player.image = utils.orient_image(self.player.image_q4, self.player.direction)
                    print("=" * ((8 * 2) + 2 + len("Testing")))
                elif self.there_is_a_monster_on_this_tile(self.player.x, self.player.y):
                    this_monster = self.get_monster(self.player.x, self.player.y)
                    this_monster.debug_print()
                    print("OMG!! IT'S A MONSTER!!!! 🙀")
                    self.fight = True
                    print("self.fight = True")
                    # self.player.in_fight_set_image()
            # elif event.type == pygame.MOUSEBUTTONUP:
                # pos = pygame.mouse.get_pos()
                # mouse_x = math.floor(pos[0]/constants.TILESIZE)
                # mouse_y = math.floor(pos[1]/constants.TILESIZE)
                # this_object = self.get_monster(mouse_x, mouse_y)
                # if not this_object is None:
                #     this_object.debug_print()
                #     print("OMG!! IT'S A MONSTER!!!! 🙀")

    def move_monster(self):
        for monster in self.monsters:
            monster.move(self.walls)

    def goodbye(self):
        print("Thank you for playing {}! 😀🧙⚔️‍".format(constants.TITLE))

    # def in_fight(self, player, monster):
    #     while monster.hit_points <= 0 or player.hit_points <= 0:
    #         pass

    # def update(self):
    #     if self.fight == True:
    #         print("---- Staring fight! ----")
    #         self.fight = False
    #         this_monster = self.get_monster(self.player.x, self.player.y)
    #         self.in_fight(self.player, this_monster)

    def update_classes(self):
        for elem in self.grasses:
            self.all_sprites.add(elem)
        for elem in self.walls:
            self.all_sprites.add(elem)
        for elem in self.monsters:
            self.all_sprites.add(elem)
        self.all_sprites.add(self.player)

    def draw_stuff(self):
        # print("debugging: background color: {}".format(self.BG_COLOR))
        self.display_surface.fill(self.BG_COLOR)
        self.update_classes()
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)
        pygame.display.flip()

    def myquit(self):
        pygame.quit()
        sys.exit()

    def main(self):
        self.clock.tick(50)
        while self.keep_looping:
            self.handle_events()
            # self.update()
            self.draw_stuff()
        self.goodbye()

# ----------------------------------------------------------------
#                           class Wall
# ----------------------------------------------------------------

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        filepath = os.path.join("data/images", constants.WALL_IMG)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)

    def debug_print(self):
        print("(x,y): {},{}".format(self.x, self.y))


# ----------------------------------------------------------------
#                           class Walls
# ----------------------------------------------------------------

class Walls:
    def __init__(self):
        self.walls = []
        self.loop_index = 0
        filepath = os.path.join("data", constants.MAPFILE)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles]
        # ------------------------------------------------------------------
        for col, tiles in enumerate(mytiles):
            for row, tile in enumerate(tiles):
                # print("row: {}, tile: {}".format(row, tile))
                if tile == 'm':
                    # print("walls")
                    mywall = Wall(row, col)
                    self.walls.append(mywall)
                    # print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.walls[item]

    def __next__(self):
        if self.loop_index >= len(self.walls):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.walls[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        pass

# ----------------------------------------------------------------
#                           class Grass
# ----------------------------------------------------------------

class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.filepath = os.path.join("data/images", constants.GRASS_IMG)
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILESIZE, y * TILESIZE)

    def debug_print(self):
        print("filepath: {}".format(self.filepath))
        print("x,y: {},{}".format(self.x, self.y))

# ----------------------------------------------------------------
#                           class Grasses
# ----------------------------------------------------------------

class Grasses:
    def __init__(self):
        self.grasses = []
        filepath = os.path.join("data", constants.MAPFILE)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles]
        # ------------------------------------------------------------------
        for col, tiles in enumerate(mytiles):
            for row, tile in enumerate(tiles):
                if tile == '.' or tile == 'p' or tile == 'c':
                    # print("grass")
                    mygrass = Grass(row, col)
                    # mygrass.debug_print()
                    self.grasses.append(mygrass)
                    # print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.grasses[item]

    def debug_print(self):
        print("Number of grasses: {}".format(len(self.grasses)))
        if len(self.grasses) == 0:
            s = "Error! There are no grasses to print."
            raise ValueError(s)
        for grass in self.grasses:
            grass.debug_print()

# ----------------------------------------------------------------
#                           class Monster
# ----------------------------------------------------------------
class Monster(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.name = mydict["name"]
        self.kind = mydict["kind"]
        # ---------------------------------------------
        self.filepath = os.path.join("data", "images", constants.MONSTER_IMG)
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
        # ---------------------------------------------
        filepath = os.path.join("data", "images", constants.MONSTER_IMG_DEAD)
        self.image_dead_monster = pygame.image.load(self.filepath).convert_alpha()
        self.image_dead_monster = pygame.transform.scale(self.image_dead_monster, (constants.TILESIZE, constants.TILESIZE))
        # ---------------------------------------------
        self.max_hit_points = mydict["max_hit_points"]
        self.hit_points = mydict["hit_points"]
        self.chance_to_hit = mydict["chance_to_hit"]
        self.experience = mydict["experience"]
        # ---------------------------------------------

    def resize(self, tilesize, new_x, new_y):
        self.image = pygame.transform.scale(self.image, (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(new_x * TILESIZE, new_y * TILESIZE)

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
            self.rect = self.rect.move(dx * TILESIZE, dy * TILESIZE)
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
        # print("DEBUGGING-->:", self.x, self.y, self.name, self.kind, self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        s = "x: {}\ny: {}\nname: {}\nkind: {}\nmax_hit_points: {}\nhit_points: {}\nchance_to_hit: {}\nexperience: {}"
        s = s.format(self.x, self.y, self.name, self.kind, self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience)
        return s

    def save_to_temp_file(self):
        filepath = os.path.join("data", "monster_after_fight_temp_file.txt")
        fileline = self.get_fileline()
        with open(filepath, "w") as f:
            f.write(fileline)

    def debug_print(self):
        s = "Debug Print Monster"
        print("-" * 10, s, "-" * 10)
        print("filepath: {}".format(self.filepath))
        print("monster name: {}; monster kind: {}".format(self.name, self.kind))
        print("x,y: {},{}".format(self.x, self.y))
        print("max_hp: {}; hp: {}; chance_to_hit: {}; exp: {}".format(self.max_hit_points, self.hit_points, self.chance_to_hit, self.experience))
        print(("-" * (len(s) + 20 + 2)))

# ----------------------------------------------------------------
#                           class Monsters
# ----------------------------------------------------------------

class Monsters:
    def __init__(self, game_reloading=False):
        self.monsters = []
        filepath = ""
        if game_reloading == True:
            self.filepath_data = os.path.join("data", constants.MONSTERS_TEMP_DATA_FILE)
        elif game_reloading == False:
            self.filepath_data = os.path.join("data", constants.MONSTERS_DATA_FILE)
        else:
            raise ValueError("Value not found: {}".format(game_reloading))
        raise NotImplemented
        # ----


    def read_data(self):
        mylist = utils.read_data_file(self.filepath_data, num_of_fields=8)
        # [print(i) for i in mylist]
        big_list = []
        for arecord in mylist:
            # print(arecord)
            mydict = {}
            for key, value in arecord.items():
                # print(key, value)
                mydict[key] = value
            new_monster = Monster(mydict)
            big_list.append(new_monster)
        debug_list = []
        debug_list.append(big_list[0])
        self.monsters = debug_list

    def save_data(self):
        for monster in self.monsters:
            fileline = monster.get_fileline()
        with open(filepath, "w") as f:
            for monster in self.monsters:
                this_line = monster.get_fileline()
                f.write(this_line)

    def get_object(self, x, y):
        monster_list = []
        print("* ----------- Debugging --------------*")
        self.monsters[0].debug_print()
        print("player.x, player.y: {},{}".format(x, y))
        for monster in self.monsters:
            print("x-axis: {} = {}".format(monster.x, x))
            print("y-axis: {} = {}".format(monster.y, y))
            if monster.x == x and monster.y == y:
                monster_list.append(monster)
                print("This monster was chosen: {} ({},{})".format(monster.name, monster.x, monster.y))
        return monster_list

    # def move(self):
    #     for monster in self.monsters:
    #         monster.move()

    def __getitem__(self, item):
        return self.monsters[item]

    def debug_print(self):
        print("Number of monsters: {}".format(len(self.monsters)))
        if len(self.monsters) == 0:
            s = "Error! There are no grasses to print."
            raise ValueError(s)
        for monster in self.monsters:
            monster.debug_print()

# ==================================================================
# ==================================================================

if __name__ == "__main__":
    mygame = Game()

    # monster = mygame.get_object(6, 8)
    # monster.debug_print()
