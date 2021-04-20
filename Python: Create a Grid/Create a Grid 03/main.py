import pygame
import constants
import sys, os

TILESIZE = 64
WIDTH = TILESIZE * 16
HEIGHT = TILESIZE * 16


# ----------------------------------------------------------------
#                           class Player
# ----------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = -1
        self.y = -1
        self.direction = constants.DOWN
        # ---------------------------------------------
        filepath = os.path.join("data", constants.MAPFILE)
        with open(filepath, "r") as f:
            mytiles = f.readlines()
            mytiles = [i.strip() for i in mytiles]
        for col, tiles in enumerate(mytiles):
            for row, tile in enumerate(tiles):
                if tile == 'P':
                    self.x = row
                    self.y = col
                    print("player at: row: {}, col: {}".format(row, col))
        # ---------------------------------------------
        filepath = os.path.join("data", "images", constants.PLAYER_IMG)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)

    def move(self, dx=0, dy=0, walls=None):
        if not self.collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            # self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)
            self.rect = self.rect.move(dx * TILESIZE, dy * TILESIZE)
            print("Player has moved. x,y: {},{}. dx={}, dy={}".format(self.x, self.y, dx, dy))

    def collide_with_walls(self, dx=0, dy=0, walls=None):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


# ----------------------------------------------------------------
#                           class Game
# ----------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My World')
        self.all_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_surface.fill(constants.RED)
        self.grasses = Grasses()
        self.walls = Walls()
        self.player = Player()
        # ----------------------------------------
        # self.all_sprites.add(mygrasses.sprite_group)

    def update_classes(self):
        for elem in self.grasses:
            self.all_sprites.add(elem)
        for elem in self.walls:
            self.all_sprites.add(elem)
        self.all_sprites.add(self.player)

    def handle_events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.myquit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.myquit()
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

    def draw_stuff(self):
        self.all_sprites.update()
        self.all_sprites.draw(self.display_surface)

    def myquit(self):
        pygame.quit()
        sys.exit()


# ----------------------------------------------------------------
#                           class Wall
# ----------------------------------------------------------------

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        filepath = os.path.join("data", "images", constants.WALL_IMG)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * TILESIZE, self.y * TILESIZE)


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
                if tile == '1':
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


# ----------------------------------------------------------------
#                           class Grass
# ----------------------------------------------------------------

class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        filepath = os.path.join("data", "images", constants.GRASS_IMG)
        try:
            self.image = pygame.image.load(filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILESIZE, y * TILESIZE)


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
                if tile == '.' or tile == 'P':
                    # print("grass")
                    mygrass = Grass(row, col)
                    self.grasses.append(mygrass)
                    print("row: {}, col: {}".format(row, col))

    def __getitem__(self, item):
        return self.grasses[item]


# ==================================================================
# ==================================================================

def setup():
    mygame = Game()
    mygame.update_classes()

    while True:
        mygame.handle_events()
        mygame.draw_stuff()
        pygame.display.update()


if __name__ == "__main__":
    setup()
