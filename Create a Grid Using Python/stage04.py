"""
Draws a window filled with tiles and mosnters.
MOVE THE MONSTERS!
"""
import pygame
import constants as con
import os
import utils

TITLE = "beasties"
TILES_HORIZONTAL = 4
TILES_VERTICAL = 4
TILESIZE = 128
WINDOW_WIDTH = TILESIZE * TILES_HORIZONTAL
WINDOW_HEIGHT = TILESIZE * TILES_VERTICAL

# --------------------------------------------------------
#                   class Monster
# --------------------------------------------------------
class Monster:
    def __init__(self, id, x, y, monster_kind):
        self.id = id
        self.x, self.y = int(x), int(y)
        self.myinc = .05
        self.monster_image = ""
        if monster_kind == "m":
            self.monster_image = con.DOG
        else:
            s = "Sorry, I don't recognize that: {}".format(monster_kind)
            raise ValueError(s)
        # ---------------------
        image_path = os.path.join("data", "images")
        self.image = pygame.image.load(os.path.join(image_path, self.monster_image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        # ---------------------

    def move(self, x, y):
        if not utils.in_range(self.x, x, .05):
            if self.x < x:
                self.x += self.myinc
            elif self.x > x:
                self.x -= self.myinc
            else:
                self.x = x
        # ---------------------------
        if not utils.in_range(self.y, y, .05):
            if self.y < y:
                self.y += self.myinc
            elif self.y > y:
                self.y -= self.myinc
            else:
                self.y = y

    def debug_print(self):
        s = "id: {}, x: {}, y: {}".format(self.id, self.x, self.y)
        print(s)

# --------------------------------------------------------
#                   class Monsters
# --------------------------------------------------------
class Monsters:
    def __init__(self, surface):
        self.surface = surface
        self.inner = []
        self.current_monster = None
        # ------------------------------------
        id = 0
        filepath = os.path.join("data", "monster_map.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        for count_i, line in enumerate(mylines):
            for count_j, elem in enumerate(line):
                if elem == "m":
                    new_monster = Monster(id, count_j, count_i, elem)
                    self.inner.append(new_monster)
                    id += 1

    def get_monster(self, x, y):
        for elem in self.inner:
            if elem.x == x and elem.y == y:
                return elem
        return None

    def format_xy(self):
        for elem in self.inner:
            elem.x = round(elem.x)
            elem.y = round(elem.y)

    def has_collided(self, mouse_pos):
        for elem in self.inner:
            myrect = pygame.Rect(elem.x * TILESIZE, elem.y * TILESIZE, TILESIZE, TILESIZE)
            if myrect.collidepoint(mouse_pos[0], mouse_pos[1]) == 1:
                # print("**** YES !!!!!! ****")
                # if s.rect.collidepoint(mouse_pos):
                return elem.x, elem.y
        return None, None

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Doh! There are no tiles to display. 😕")
        for elem in self.inner:
            myrect = pygame.Rect(elem.x * TILESIZE, elem.y * TILESIZE, TILESIZE, TILESIZE)
            self.surface.blit(elem.image, myrect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

# --------------------------------------------------------
#                   class Tile
# --------------------------------------------------------

class Tile:
    def __init__(self, id, x, y, kind_of_tile):
        filename = ""
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.kind_of_tile = kind_of_tile
        # ----
        if kind_of_tile == "g": filename = con.GRASS
        elif kind_of_tile == "d" : filename = con.DIRT
        else: raise ValueError("Error! kind of tile: ", kind_of_tile)
        # ---------------------
        self.rect = pygame.Rect(self.x * TILESIZE, self.y * TILESIZE, TILESIZE, TILESIZE)
        image_path = os.path.join("data", "images")
        self.image = pygame.image.load(os.path.join(image_path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

    def debug_print(self):
        s = "id: {}, x: {}, y: {}, kind: {}"
        s = s.format(self.id, self.x, self.y, self.kind_of_tile)
        print(s)

# --------------------------------------------------------
#                   class Tiles
# --------------------------------------------------------

class Tiles:
    def __init__(self, screen):
        self.screen = screen
        self.inner = []
        self.current_tile = None
        self._load_data()

    def _load_data(self):
        self.inner = []
        filepath = os.path.join("data", "animal_map.txt")
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        id = 0
        for count_i, myline in enumerate(mylines):
            temp_list = myline.split(";")
            temp_list = [i.strip() for i in temp_list if len(i.strip()) > 0]
            for count_j, elem in enumerate(temp_list):
                new_tile = Tile(id, count_j, count_i, elem)
                self.inner.append(new_tile)
                id += 1

    def get_tile(self, x, y):
        for elem in self.inner:
            if elem.x == x:
                if elem.y == y:
                    return elem
        return None

    def has_collided(self, mouse_pos):
        for elem in self.inner:
            if elem.rect.collidepoint(mouse_pos) == 1:
                # print("**** YES !!!!!! ****")
                # if s.rect.collidepoint(mouse_pos):
                return elem.x, elem.y
        return None, None

    def draw(self, surface):
        if len(self.inner) == 0:
            raise ValueError("Doh! There are no tiles to display. 😕")
        for elem in self.inner:
            self.screen.blit(elem.image, elem.rect)

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

# --------------------------------------------------------
#                   class Game
# --------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.BG_COLOR = con.LIGHTGREY
        self.keep_looping = True
        # ----
        self.tiles = Tiles(self.surface)
        self.monsters = Monsters(self.surface)

    def _current_monster_recorded(self, monster, x, y):
        # a monster is recorded in monsters.current_monster
        if not monster is None:
            self.monsters.current_monster = monster
            self.tiles.current_tile = None
        else:
            self.tiles.current_tile = self.tiles.get_tile(x, y)

    def _not_current_monster_recorded(self, monster, x, y):
        # no monster is recorded in monsters.current_monster
        if not monster is None:
            self.monsters.current_monster = monster
            self.tiles.current_tile = None
        else:
            self.monsters.current_monster = None
            self.tiles.current_tile = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # Make sure x,y coords of Monsters are okay.
                self.monsters.format_xy()
                # ------------------------------
                mouse_pos = pygame.mouse.get_pos()
                x, y = self.tiles.has_collided(mouse_pos)
                monster = self.monsters.get_monster(x, y)
                if not self.monsters.current_monster is None:
                    self._current_monster_recorded(monster, x, y)
                else:
                    self._not_current_monster_recorded(monster, x, y)
                self.monsters.debug_print()

    def update(self):
        if self.monsters.current_monster == None or self.tiles.current_tile == None: return False
        self.monsters.current_monster.move(self.tiles.current_tile.x, self.tiles.current_tile.y)

    def draw(self):
        self.surface.fill(self.BG_COLOR)
        self.tiles.draw(self.surface)
        self.monsters.draw(self.surface)
        pygame.display.update()

    def main(self):
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    mygame = Game()
    mygame.main()
