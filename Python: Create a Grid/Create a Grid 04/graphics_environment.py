import sys, os
import pygame
import constants

# -----------------------------------------------------------
#                      class Grass
# -----------------------------------------------------------
"""
As you can see, class Grass uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
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
        self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)

    def debug_print(self):
        print("filepath: {}".format(self.filepath))
        print("x,y: {},{}".format(self.x, self.y))

# -----------------------------------------------------------
#                      class Grasses
# -----------------------------------------------------------
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

# -----------------------------------------------------------
#                      class Wall
# -----------------------------------------------------------
"""
As you can see, class Wall uses inheritance. We do this so that 
we can add this class--which is now a subclass of the pygame.sprite.Sprite
class and so, now, is itself a Sprite--to a pygame.sprite.Group.

If none of that makes any sense to you, don't worry!
I would recommend that you start using inheritance and, 
as you see how it works, you will come
to understand it. And, please, ask questions! Ask me, ask on 
Stack Overflow (https://stackoverflow.com/) or even Twitter.
"""
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
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def debug_print(self):
        print("(x,y): {},{}".format(self.x, self.y))

# -----------------------------------------------------------
#                      class Walls
# -----------------------------------------------------------
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