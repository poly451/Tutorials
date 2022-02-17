import pygame
import constants
import sys, os
import utils

# ------------------------------------------------------
#                   class Tile
# ------------------------------------------------------
class RichTile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_name, image_dict):
        super().__init__()
        if tile_name is None: raise ValueError("Error")
        if image_dict is None: raise ValueError("Error")
        if image_dict["map_name"] != tile_name: raise ValueError("Error")
        # ---- ----
        self.tile_name = tile_name
        self.image_name = image_dict["image_name"]
        self.the_image_itself = image_dict["the_image_itself"]
        # ---- ----
        self.size = ""
        self.tilesize = constants.TILESIZE
        self.imagesize = constants.TILESIZE
        self.x, self.y = x, y
        # self.image_name = image_name
        # print(self.image_name)
        self.image = self.the_image_itself
        self.image = pygame.transform.scale(self.image, (self.imagesize, self.imagesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.tilesize, self.y * self.tilesize)
        # ---- ----
        self.hit_points = 10

    def read_data(self, obstacle_dicts):
        def helper():
            for mydict in obstacle_dicts:
                if mydict["name"] == self.tile_name:
                    return mydict
            return None
        # ---- ---- ---- ----
        mydict = helper()
        if mydict is None: raise ValueError("Error")
        # ----
        self.size = mydict["size"]
        if mydict is None:
            self.debug_print()
            print("-" * 40)
            print("self.image_name:", self.image_name)
            print("obstacle_dicts:", obstacle_dicts)
            raise ValueError("Error")
        if self.size == "original":
            pass
        elif self.size == "custom":
            pass
        elif self.size == "small":
            self.x += 0.3
            self.y += 0.3
            self.imagesize = int(self.imagesize * 0.4)
            self.image = pygame.transform.scale(self.image, (self.imagesize, self.imagesize))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x * self.tilesize, self.y * self.tilesize)
        else:
            s = "I don't understand this: {}".format(mydict["size"])
            raise ValueError(s)

    def get_tile_kind(self):
        return self.__class__.__name__

    def debug_print(self):
        s = "class: {}\n".format(self.__class__.__name__)
        if self.rect == None:
            s += "x: {}, y: {}, hit_points: {}, image_name: {}, image: {}"
            s = s.format(self.x, self.y, self.hit_points, self.image_name, self.image)
        else:
            s += "x: {}, y: {}, hit_points: {}, image_name: {}, rect.x: {}, rect.y: {}, image: {}"
            s = s.format(self.x, self.y, self.hit_points, self.image_name, self.rect.x, self.rect.y, self.image)
        print(s)

# ------------------------------------------------------
#                   class RichTiles
# ------------------------------------------------------
class RichTiles:
    def __init__(self, zone_name, map_name):
        # self.mapkind = "obstacles"
        self.zone_name = zone_name
        self.map_name = map_name
        if not self.zone_name in constants.ZONE_NAMES: raise ValueError("Error")
        if not self.map_name in constants.MAP_NAMES: raise ValueError("Error")
        # ---- ----
        self.inner = pygame.sprite.Group()
        # ---- ----
        # <class '__main__.PersistentsLower'>
        self.mapkind = self.__class__.__name__.lower()
        self.tilesize = constants.TILESIZE
        self.imagesize = constants.TILESIZE
        self.images_used = {}

    def remove_me(self, a_sprite):
        pygame.sprite.Group.remove(self.inner, a_sprite)

    def read_data(self):
        self._read_in_images()
        self._read_tiles()

    def _read_in_images(self):
        # Puts key, image in a dictionary
        def helper(list_of_dicts, name):
            for mydict in list_of_dicts:
                if mydict["name"] == name:
                    return mydict
            return None
        # ---- ---- ---- ----
        filename = "{}.txt".format(self.mapkind)
        obstacle_path = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        if os.path.isfile(obstacle_path) == False:
            s = "This isn't a file path: {}".format(obstacle_path)
            raise ValueError(s)
        # ---- ----
        self.images_used = {}
        # ---- ----
        obstacle_map_unique_values = utils.get_map_values(self.zone_name, self.map_name, self.mapkind)
        # ----
        obstacle_file = utils.read_data_file(obstacle_path, 6)
        # ---- ----
        obstacle_tiles = []
        for tile_name in obstacle_map_unique_values:
            mydict = helper(obstacle_file, tile_name)
            if mydict is None:
                s = "obstacle_path: {}\n".format(obstacle_path)
                s += "tile_name: {}\n".format(tile_name)
                raise ValueError(s)
            obstacle_tiles.append(mydict)
        # ---- ----
        for a_tile in obstacle_tiles:
            try:
                filepath = utils.get_filepath(a_tile["image"], constants.IMAGES)
            except Exception as e:
                s = "a_tile[image]: {}".format(a_tile["image"])
                t = "\n{}\n{}\n".format(e, s)
                raise ValueError(t)
            if filepath is None: raise ValueError("Error")
            # ---- ----
            temp_dict = {}
            temp_dict["the_image_itself"] = pygame.image.load(filepath).convert_alpha()
            temp_dict["image_name"] = a_tile["image"]
            temp_dict["map_name"] = a_tile["name"]
            # ----
            self.images_used[a_tile["name"]] = temp_dict

    def _read_tiles(self):
        filename = "{}_{}.txt".format(self.map_name, self.mapkind)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        if utils.file_is_empty(filepath) == True:
            return False
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # ------------------------------------------------------------------
        big_list = []
        for map_row in mytiles:
            mylist = map_row.split(";")
            mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
            big_list.append(mylist)
        # counter = 0
        # ----
        filename = "{}.txt".format(self.mapkind)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        if os.path.isfile(filepath) == False: raise ValueError("Error")
        obstacle_dicts = utils.read_data_file(filepath, 6)
        # ----
        for j, a_row in enumerate(big_list):
            for i, tile_name in enumerate(a_row):
                if tile_name == "...":
                    pass
                else:
                    if len(tile_name) != 3:
                        s = "tile_name: {}".format(tile_name)
                        raise ValueError(s)
                    the_image_dict = self.images_used[tile_name]
                    if the_image_dict is None:
                        s = "I could not find an image for this tile name: {}"
                        s = s.format(tile_name)
                        raise ValueError(s)
                    # ---- ----
                    new_object = RichTile(i, j, tile_name, the_image_dict)
                    new_object.read_data(obstacle_dicts)
                    self.inner.add(new_object)
                    # counter += 1

    def collision(self, a_sprite):
        collides = pygame.sprite.spritecollideany(a_sprite, self.inner, collided=None)
        if collides is not None:
            return True
        else:
            return False

    def get_tile(self, x, y):
        if type(x) != type(123) and type(x) != type(12.3): raise ValueError("Error")
        for a_tile in self.inner.sprites():
            # print("a_tile.x, a_tile.y: {}, {} || {}, {}".format(a_tile.x, a_tile.y, type(a_tile.x), type(a_tile.y)))
            # print("x, y: {}, {} || {}, {}".format(x, y, type(x), type(y)))
            if math.floor(a_tile.x) == x and math.floor(a_tile.y) == y: return a_tile
        return None

    def get_closest(self, animal):
        list_of_sprites = self.inner.sprites()
        animal_position = [animal.x, animal.y]
        furthest_distance = 100000
        closest_sprite = None
        for a_sprite in list_of_sprites:
            sprite_position = [a_sprite.x, a_sprite.y]
            a_distance = utils.distance_between_two_points(animal_position, sprite_position)
            if a_distance < furthest_distance:
                furthest_distance = a_distance
                closest_sprite = a_sprite
        return closest_sprite

    def get_touching(self, a_sprite):
        return pygame.sprite.spritecollideany(a_sprite, self.inner, collided=None)

    def update_class(self, all_sprites):
        for elem in self.inner:
            all_sprites.add(elem)
        return all_sprites

    def get_position_text(self):
        a_sprite = self.inner.sprites()[0]
        s = "rect.x: {}, rect.y: {}; x: {}, y: {}"
        s = s.format(a_sprite.rect.left, a_sprite.rect.top, a_sprite.x, a_sprite.y)
        return s

    def debug_print(self):
        print("---- debug_print Class: ----\n")
        s = "zone_name: {}, map_name: {}, tilesize: {}, imagesize: {}, len(): {}, number of tiles used: {}, mapkind: {}"
        s = s.format(self.zone_name, self.map_name, self.tilesize, self.imagesize, len(self.images_used), len(self.inner.sprites()), self.mapkind)
        # s += "{}".format(self.images_used)
        print("----")
        print(s)
        for elem in self.inner.sprites() :
            print(elem)
        print("---------------------------------------")

# ------------------------------------------------------
#                   class Obstacles
# ------------------------------------------------------
class Obstacles(RichTiles):
    def __init__(self, zone_map, map_name):
        super().__init__(zone_map, map_name)

# ------------------------------------------------------
#                   class PersistentsLower
# ------------------------------------------------------
class PersistentsLower(RichTiles):
    def __init__(self, zone_map, map_name):
        super().__init__(zone_map, map_name)

# ------------------------------------------------------
#                   class Environment_Driver
# ------------------------------------------------------
class Environment_Driver:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        if self.zone_name not in constants.ZONE_NAMES: raise ValueError("Error")
        if self.map_name not in constants.MAP_NAMES: raise ValueError("Error")
        # ---- ----
        self.init_pygame()
        self.enviornment = None
        self.keep_looping = True
        # self.player = None

    def read_data(self):
        self.environment = Obstacles(self.zone_name, self.map_name)
        self.environment.read_data()

    def debug_print(self):
        self.environment.debug_print()

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Spritesheets')
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        # print(len(self.all_sprites))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main(self):
        # self.all_sprites.add(self.background_sprite)
        self.environment.update_class(self.all_sprites)
        # self.environment.load_all_sprites(self.all_sprites)
        while self.keep_looping == True:
            self.clock.tick(10)
            self.handle_events()
            self.draw()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    zone_name, map_name = "docks", "map00"
    mydriver = Environment_Driver(zone_name, map_name)
    choices = ["obstacles", "persistentslower", "grid"]
    mydriver.read_data()
    mydriver.main()
