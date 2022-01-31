import pygame
import constants
import utils
import sys, os

# ------------------------------------------------------
#                   class Tile
# ------------------------------------------------------
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, image, imagesize=constants.TILESIZE):
        super().__init__()
        if image is None: raise ValueError("Error")
        self.tilesize = constants.TILESIZE
        self.imagesize = imagesize
        self.x = x
        self.y = y
        self.image_name = image_name
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.imagesize, self.imagesize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.tilesize, self.y * self.tilesize)
        # ---- ----
        self.hit_points = 10

    def debug_print(self):
        s = "class: {}\n".format(self.__class__.__name__)
        if self.rect == None:
            s += "x: {}, y: {}, image_name: {}, image: {}"
            s = s.format(self.x, self.y, self.image_name, self.image)
        else:
            s += "x: {}, y: {}, image_name: {}, rect.x: {}, rect.y: {}, image: {}"
            s = s.format(self.x, self.y, self.image_name, self.rect.x, self.rect.y, self.image)
        print(s)

# ------------------------------------------------------
#                   class Tiles
# ------------------------------------------------------
class Tiles:
    def __init__(self, zone_name, map_name):
        self.zone_name = zone_name
        self.map_name = map_name
        self.mapkind = self.__class__.__name__.lower()
        # ---- ----
        if self.zone_name not in constants.ZONE_NAMES:
            s = "I don't recognize this zone name: {}".format(self.zone_name)
            raise ValueError(s)
        if self.mapkind not in constants.MAPKINDS:
            s = "I don't recognize this mapkind: {}".format(self.mapkind)
            raise ValueError(s)
        # ---- ----
        self.init_pygame()
        # ---- ----
        self.inner = pygame.sprite.Group()
        self.tilesize = constants.TILESIZE
        self.imagesize = constants.TILESIZE
        self.images_used = {}

    def read_data(self):
        self._read_in_images()
        self._read_tiles()

    def _read_in_images(self):
        def helper(tiles, name):
            for mydict in tiles:
                if mydict["name"] == name:
                    return mydict
            return None
        # ---- ----
        self.images_used = {}
        unique_values = utils.get_map_values(self.zone_name, self.map_name, self.mapkind)
        # print(unique_values)
        # raise NotImplemented
        filepath = os.path.join("data", "master_files", "tiles.txt")
        if os.path.isfile(filepath) == False: raise ValueError("Error")
        tile_list = utils.read_data_file(filepath, 4)
        # ---- ----
        for tile_name in unique_values:
            mydict = helper(tile_list, tile_name)
            if mydict is None: raise ValueError("Error")
            imagepath = utils.get_filepath(mydict["image"], constants.IMAGES)
            if imagepath is None:
                s = "I couldn't find a path for this image: {}".format(mydict["image"])
                raise ValueError(s)
            myimage = pygame.image.load(imagepath).convert_alpha()
            self.images_used[tile_name] = myimage

    def _read_tiles(self):
        filename = "{}_{}.txt".format(self.map_name, self.mapkind)
        filepath = os.path.join("data", "zones", self.zone_name, self.map_name, filename)
        if os.path.isfile(filepath) == False: raise ValueError("Error")
        if utils.file_is_empty(filepath) == True:
            return False
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles if len(i.strip()) > 0]
        mytiles = [i[3:] for i in mytiles[2:]]
        # print("mytiles: ", mytiles)
        # raise NotImplemented
        # ------------------------------------------------------------------
        big_list = []
        for map_row in mytiles:
            mylist = map_row.split(";")
            mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
            big_list.append(mylist)
        for j, a_row in enumerate(big_list):
            for i, tile_name in enumerate(a_row):
                if tile_name == "...":
                    pass
                else:
                    if len(tile_name) != 3:
                        s = "tile_name: {}".format(tile_name)
                        raise ValueError(s)
                    the_image = self.images_used[tile_name]
                    if the_image is None:
                        s = "I could not find an image for this tile name: {}"
                        s = s.format(tile_name)
                        raise ValueError(s)
                    # print("i: {}, j: {}, tile_name: {}, the_image: {}".format(i, j, tile_name, the_image))
                    # raise NotImplemented
                    new_object = Tile(i, j, tile_name, the_image)
                    self.inner.add(new_object)

    def collision(self, a_sprite):
        collides = pygame.sprite.spritecollideany(a_sprite, self.inner, collided=None)
        if collides is not None:
            return True
        else:
            return False

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption(constants.TITLE)
        self.clock = pygame.time.Clock()

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
        print("---- debug_print Class: {}----\n".format(self.__class__.__name__))
        s = "zone_name: {}, map_name: {}, tilesize: {}, imagesize: {}"
        s = s.format(self.zone_name, self.map_name, self.tilesize, self.imagesize)
        s += "{}".format(self.images_used)
        print("----")
        for elem in self.inner.sprites() :
            elem.debug_print()
        print("---------------------------------------")

# ------------------------------------------------------
#                   class Walkables
# ------------------------------------------------------

class Walkables(Tiles):
    def __init__(self, zone_map, map_name):
        super().__init__(zone_map, map_name)

# *****************************************************
# *****************************************************

def main():
    zone_name = "docks"
    map_name = "map00"
    mydriver = Walkables(zone_name, map_name)
    mydriver.read_data()
    # mydriver.debug_print()

if __name__ == "__main__":
    main()
















