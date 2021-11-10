import pygame
import utils
import constants
import os, sys

# -----------------------------------------------------------
#                      class Environment
# -----------------------------------------------------------

class Environment:
    def __init__(self, zone_name, map_name):
        if zone_name is None or map_name is None:
            raise ValueError("Error!")
        if len(zone_name) == 0 or len(map_name) == 0:
            raise ValueError("Error!")
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.init_pygame()
        # ----
        self.zone_description = ""
        self.obstacles = Obstacles(self.zone_name, self.map_name)
        self.walkables = Walkables(self.zone_name, self.map_name)
        # self.persistents = PersistentObjects(self.zone_name, self.map_name)
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True

    def read_data(self):
        self.walkables.read_data()
        self.obstacles.read_data()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def get_walkable_tile(self, x, y):
        # for a_tile in self.obstacles:
        #     if a_tile.x == x:
        #         if a_tile.y == y:
        #             return a_tile
        for a_tile in self.walkables:
            if a_tile.x == x:
                if a_tile.y == y:
                    return a_tile
        return None

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
                # else:
                #     print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        all_sprites = self.walkables.update_classes(all_sprites)
        # all_sprites = self.persistents.update_classes(all_sprites)
        all_sprites = self.obstacles.update_classes(all_sprites)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites = self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping == True:
            self.handle_events()
            self.draw()
        self.goodbye()
        self.myquit()

    def goodbye(self):
        print("Goodbye!")

    def myquit(self):
        pygame.quit()

    def debug_print(self):
        s = "zone_name: {}\nzone_description: {}"
        s = s.format(self.zone_name, self.zone_description)
        print(s)
        self.obstacles.debug_print()
        self.walkables.debug_print()

# -----------------------------------------------------------
#                      class Walkable
# -----------------------------------------------------------

"""
As you can see, class Walkable uses inheritance. We do this so that
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and,
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
class Walkable(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        self.image_filename = mydict["image"]
        self.image_path = utils.get_filepath(self.image_filename)
        self.image = None
        self.rect = None
        self.comment = ""
        # ----
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.image_filename)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def _collide(self, dx=0, dy=0, obstacles=None):
        for a_tile in obstacles:
            if a_tile.x == self.x + dx and a_tile.y == self.y + dy:
                return True
        return False

    def move(self, dx=0, dy=0, obstacles=None):
        if not self._collide(dx, dy, obstacles):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
            # print("Player has moved. x,y: {},{}; dx={}, dy={}".format(self.x, self.y, dx, dy))

    def debug_print(self):
        s = "x,y: ({},{}); kind: {}, image: {}, comment: {}"
        s = s.format(self.x, self.y, self.kind, self.image_filename, self.comment)
        print(s)

# -----------------------------------------------------------
#                      class Walkables
# -----------------------------------------------------------
class Walkables:
    def __init__(self, zone_name, map_name):
        if zone_name == None:
            raise ValueError("Error!")
        if len(zone_name) == 0:
            raise ValueError("Error!")
        if map_name == None:
            raise ValueError("Error!")
        if len(map_name) == 0:
            raise ValueError("Error!")
        self.zone_name = zone_name
        self.map_name = map_name
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.init_pygame()
        self.loop_index = 0
        # self.walkables = self.read_data()
        self.walkables = []
        self.keep_looping = True
        # if self.walkables is None:
        #     raise ValueError("Doh!")

    def read_data(self):
        self._load_map()

    def _load_map(self):
        filename = "{}_walkables.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        filepath = os.path.join("data", "master_files", "tiles.txt")
        file_tiles = utils.read_data_file(filepath, num_of_fields=4)
        # ------------------------------------------------------------------
        self.walkables = []
        for col, tiles in enumerate(mytiles):
            tile_list = tiles.split(";")
            tile_list = [i.strip() for i in tile_list if len(i.strip()) > 0]
            for row, tile in enumerate(tile_list):
                # print("tile: {}".format(tile))
                if not tile == "..":
                    mydict = utils.get_dictionary(file_tiles, tile)
                    if mydict is None:
                        s = "tile: {}\n".format(tile)
                        raise ValueError(s)
                    mydict["x"] = row
                    mydict["y"] = col
                    mywalk = Walkable(mydict)
                    self.walkables.append(mywalk)
                if tile == "..":
                    pass

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))

    def update_classes(self, all_sprites):
        if len(self.walkables) == 0: raise ValueError("Error")
        for elem in self.walkables:
            all_sprites.add(elem)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    def __len__(self):
        return len(self.walkables)

    def __getitem__(self, item):
        return self.walkables[item]

    def __next__(self):
        if self.loop_index >= len(self.walkables):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.walkables[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        print("Number of grasses: {}".format(len(self.walkables)))
        if len(self.walkables) == 0:
            s = "Error! There are no grasses to print."
            raise ValueError(s)
        for grass in self.walkables:
            grass.debug_print()

# -----------------------------------------------------------
#                      class Obstacle
# -----------------------------------------------------------

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, mydict):
        super().__init__()
        self.x = mydict["x"]
        self.y = mydict["y"]
        self.kind = mydict["kind"]
        # self.trigger = mydict["trigger"]
        # self.image_filename = mydict["image_filename"]
        self.image_filename = mydict["image"]
        self.image_path = utils.get_filepath(self.image_filename)
        self.image = None
        self.rect = None
        # ----
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(self.image_path)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def read_data(self, zone_name, map_name):
        filepath = os.path.join("data", "zones", zone_name, map_name, "actions.txt")
        mylines = utils.read_data_file(filepath, 8)
        if mylines is None or len(mylines) == 0:
            raise ValueError("Error!")
        # ----
        target_dict = {}
        for elem in mylines:
            if elem["name"] == self.name:
                target_dict = elem
        if len(target_dict) == 0:
            s = "The name {} was not found in {}".format(self.name, target_dict)
            raise ValueError(s)
        self.command = target_dict["command"]
        if not self.command in constants.MAP_COMMANDS:
            raise ValueError("Error! {} is not in {}".format(target_dict["command"], constants.MAP_COMMANDS))
        self.image_display = target_dict["image_display"]
        self.data = target_dict["data"]
        self.inventory_condition = target_dict["inventory_condition"]
        if self.inventory_condition == "none":
            self.inventory_condition = None
        # Need to be able to check that the player has successfully
        # completed a conversation.
        # Perhaps also check to see that the conversation is in the
        # events file.
        self.game_condition = target_dict["game_condition"].lower().strip()
        if self.game_condition == "none":
            self.game_condition = None
        self.dialog_text = target_dict["dialog_text"]
        self.comment = target_dict["comment"]
        self.completed = False
        # ----
        self.image_display = self.image_display.replace(" ", "_")
        if self.image_display.find(".png") == -1:
            self.image_display = "{}.png".format(self.image_display)
        filepath = utils.get_filepath(self.image_display)
        if filepath is None:
            s = "I wasn't able to find a path for the file: {}".format(self.image_display)
            raise ValueError(s)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except Exception as e:
            print(e)
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def debug_print(self):
        s = "(x,y): {},{}; kind:{}, image_filename: {}, rect: {}"
        s = s.format(self.x, self.y, self.kind, self.image_filename, self.rect)
        print(s)

# -----------------------------------------------------------
#                      class Obstacles
# -----------------------------------------------------------
class Obstacles:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.init_pygame()
        self.obstacles = []
        self.loop_index = 0
        self.keep_looping = True
        self.all_sprites = pygame.sprite.Group()

    def read_data(self):
        self._load_map()

    def _load_map(self):
        # Load in the map
        filename = "{}_obstacles.txt".format(self.map_name)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        print("Reading in obstacle map ...")
        print("zone: {}, map: {}".format(self.zone_name, self.map_name))
        print("filepath for obstacle file: {}".format(filepath))
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        filepath = os.path.join("data", "master_files", "tiles.txt")
        file_tiles = utils.read_data_file(filepath, num_of_fields=4)
        # ------------------------------------------------------------------
        self.obstacles = []
        for col, tiles in enumerate(mytiles):
            list_tiles = tiles.split(";")
            list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
            for row, tile in enumerate(list_tiles):
                if not tile == "..":
                    tile_dict = utils.get_dictionary(file_tiles, tile)
                    if tile_dict is None:
                        raise ValueError("tile: {}".format(tile))
                    tile_dict["x"] = row
                    tile_dict["y"] = col
                    my_obstacle = Obstacle(tile_dict)
                    self.obstacles.append(my_obstacle)
                elif tile == "..":
                    pass
                else:
                    s = "Error! I don't recognize this: {}".format(tile)
                    raise ValueError(s)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def collision(self, x, y):
        if self.obstacles is None:
            raise ValueError("Error")
        if len(self.obstacles) == 1:
            raise ValueError("Error")
        for a_tile in self.obstacles:
            if a_tile.kind == "empty":
                continue
            if a_tile.x == x:
                # print("tile y: {}, player y: {}".format(a_tile.y, y))
                if a_tile.y == y:
                    print("tile x,y: ({},{}), player x,y: ({},{})".format(a_tile.x, a_tile.y, x, y))
                    return True
        return False

    def collision_is_close(self, x, y):
        if self.obstacles is None:
            raise ValueError("Error")
        if len(self.obstacles) == 1:
            raise ValueError("Error")
        # ----
        for a_tile in self.obstacles:
            if a_tile.kind == "empty":
                continue
            if utils.points_are_close(a_tile.x, x) == True:
                # print("tile y: {}, player y: {}".format(a_tile.y, y))
                if utils.points_are_close(a_tile.y, y) == True:
                    print("tile x,y: ({},{}), player x,y: ({},{})".format(a_tile.x, a_tile.y, x, y))
                    return True
        return False

    # --------------------------------------------------------

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
                else:
                    print("I don't recognize this event.key in handle_events: {}".format(event.key))
                # ------------------------------------------------------

    def update_classes(self, all_sprites):
        for elem in self.obstacles:
            all_sprites.add(elem)
        return all_sprites

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes(self.all_sprites)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

    # --------------------------------------------------------

    def __len__(self):
        return len(self.obstacles)

    def __getitem__(self, item):
        return self.obstacles[item]

    def __next__(self):
        if self.loop_index >= len(self.obstacles):
            self.loop_index = 0
            raise StopIteration
        else:
            this_value = self.obstacles[self.loop_index]
            self.loop_index += 1
            return this_value

    def __iter__(self):
        return self

    def debug_print(self):
        for elem in self.obstacles:
            elem.debug_print()

# **************************************************
zone_name = "testing"
map_name = "map00"

def debug_walkables():
    mywalkables = Walkables(zone_name, map_name)
    mywalkables.read_data()
    # mywalkables.debug_print()
    mywalkables.main()

def debug_obstacles():
    myobstacles = Obstacles(zone_name, map_name)
    myobstacles.read_data()
    # myobstacles.debug_print()
    myobstacles.main()

def debug_environment():
    myenv = Environment(zone_name, map_name)
    myenv.read_data()
    myenv.main()

if __name__ == "__main__":
    # debug_walkables()
    # debug_obstacles()
    debug_environment()