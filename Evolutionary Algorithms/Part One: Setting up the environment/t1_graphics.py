import os, sys
import pygame
import t1_constants as con
import t1_utils as utils


# ------------------------------------------------------------
#                         class TileBackground
# ------------------------------------------------------------

class BackgroundTile:
    def __init__(self, zone_kind, mydict):
        if not zone_kind in con.ZONE_NAMES:
            raise ValueError("Error!")
        self.zone_kind = zone_kind
        self.col_num = int(mydict["y"])
        self.row_num = int(mydict["x"])
        self.kind = mydict["kind"]
        self.value = mydict["value"]
        self.filename = mydict["filename"]
        # ----
        image_filepath = os.path.join("data", "images")
        try:
            self.image = pygame.image.load(os.path.join(image_filepath, self.filename)).convert_alpha()
        except Exception as e:
            print("This path was not found: {}".format(os.path.join(image_filepath, self.filename)))
            raise ValueError(e)
        self.image = pygame.transform.scale(self.image, (con.TILESIZE, con.TILESIZE))

    def draw(self, screen):
        screen.blit(self.image, (self.col_num * con.TILESIZE, self.row_num * con.TILESIZE, con.TILESIZE, con.TILESIZE))

    def debug_print(self):
        s = "x,y: {},{}; kind: {}, value: {}, filename: {}"
        s = s.format(self.col_num, self.row_num, self.kind, self.value, self.filename)
        print(s)

# ------------------------------------------------------------
#                  class TileBackgrounds
# ------------------------------------------------------------

class BackgroundTiles:
    def __init__(self, zone_name):
        # print("--------->>>>> Zone Name: {}".format(zone_name))
        if not zone_name in con.ZONE_NAMES:
            raise ValueError("Error!")
        self.zone_name = zone_name
        self.init_pygame()
        # ---------------------------------------
        self.keep_looping = True
        self.inner = self.read_tiles()

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(con.TITLE)
        self.surface = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def read_tiles(self):
        filename = "{}.txt".format(self.zone_name)
        filepath = os.path.join("data", filename)
        # print(filepath)
        print("--------->>>>> filepath: {}".format(filepath))
        with open(filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        # [print(i) for i in mylines]
        # sys.exit("kdkddk")
        big_list = []
        number_of_fields = 5
        for i in range(0, len(mylines), number_of_fields):
            mydict = {}
            for j in range(number_of_fields):
                elem = mylines[i + j]
                mydict = utils.key_value(elem, mydict)
            new_env_tile = BackgroundTile(self.zone_name, mydict)
            # new_env_tile.debug_print()
            big_list.append(new_env_tile)
        return big_list

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_RETURN:
                    self.user_input = self.text.lower().strip()
                    self.text = ""
                elif event.key == pygame.K_a:
                    self.act_on_object = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        pass

    def draw(self):
        self.surface.fill(con.LIGHTGREY)
        for elem in self.inner:
            elem.draw(self.surface)
        # pygame.display.update()

    def main(self):
        self.clock.tick(50)
        while self.keep_looping:
            # time.sleep(1)
            self.events()
            self.update()
            self.draw()

    def debug_print(self):
        mylist = []
        for elem in self.inner:
            elem.debug_print()

# *********************************************************

if __name__ == "__main__":
    mygraphics = BackgroundTiles(con.ENVIRONMENT_VARIABLE)
    mygraphics.main()