import random
import pygame
import utils
import constants
import os

# -------------------------------------------------------
#                     class MySprite
# -------------------------------------------------------
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_filename, x, y):
        super().__init__()
        self.init_pygame()
        # self.all_sprites = pygame.sprite.Group()
        self.x, self.y = x, y
        filepath = utils.get_filepath(image_filename)
        self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE * 3, constants.TILESIZE * 3))
        self.image = pygame.transform.scale(self.image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

# -------------------------------------------------------
#                     class MySprite
# -------------------------------------------------------
class MyMovingSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.first_time = True
        self.show_image = False
        self.begin_x, self.begin_y = -1, -1
        self.end_x, self.end_y = -1, -1
        self.real_begin_x, self.real_begin_y = -1, -1
        self.real_end_x, self.real_end_y = -1, -1
        self.filepath = ""
        self.image = None
        self.rect = None
        # print("in MySpriteNew: real_begin_x, real_begin_y: {},{} <<=========================".format(self.real_begin_x, self.real_begin_y))

    def read_data(self, begin_x, begin_y, end_x, end_y, image_filepath):
        if not begin_x in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
            raise ValueError("Error")
        if not begin_y in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
            raise ValueError("Error")
        if not end_x in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
            raise ValueError("Error")
        if not end_y in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
            raise ValueError("Error")
        # ----
        self.filepath = image_filepath
        if os.path.isfile(self.filepath) == False:
            self.filepath = utils.get_filepath(self.filepath)
        # print("image_filepath: {}".format(image_filepath))
        self.begin_x, self.begin_y = begin_x, begin_y
        self.end_x, self.end_y = end_x, end_y
        self.real_begin_x = (self.begin_x * constants.TILESIZE) #- (constants.TILESIZE)
        self.real_begin_y = self.begin_y * constants.TILESIZE
        self.real_end_x = (self.end_x * constants.TILESIZE) #- (constants.TILESIZE)
        self.real_end_y = (self.end_y * constants.TILESIZE)  # - (constants.TILESIZE)
        # ----
        if os.path.isfile(image_filepath) == False:
            # print("Checking whether the image file was not a full filepath...")
            self.filepath = utils.get_filepath(image_filepath)
            if self.filepath is None:
                raise ValueError("Error: This file does not exist: {}".format(image_filepath))
            if len(self.filepath) == 0:
                raise ValueError("Error: This filepath is empty.")
            print("This filepath: {}".format(self.filepath))
        # ----
        self.all_sprites = pygame.sprite.Group()
        self.image = pygame.image.load(self.filepath).convert_alpha()
        mysize = int(constants.TILESIZE)
        self.image = pygame.transform.scale(self.image, (mysize, mysize))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.real_begin_x, self.real_begin_y)
        # ----

    def turn_invisible(self):
        filepath = utils.get_filepath("empty.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        # self.rect = self.rect.move(self.real_begin_x, self.real_begin_y)

    def update_endpoint(self, new_end_x, new_end_y):
        self.real_end_x = (new_end_x * constants.TILESIZE) #- (constants.TILESIZE)
        self.real_end_y = (new_end_y * constants.TILESIZE)  # - (constants.TILESIZE)

    def load_apple_image(self):
        filepath = utils.get_filepath("apple01.png")
        self._load_image(filepath)

    def load_tomato_image(self):
        filepath = utils.get_filepath("tomato.png")
        self._load_image(filepath)

    def _load_image(self, filepath):
        self.image = pygame.image.load(filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.real_begin_x, self.real_begin_y)
        # ----

    def move_image(self):
        self.first_time = False
        myinc = 10
        myint = random.randint(0, 1)
        # print("end_x, end_y: {},{}".format(end_x, end_y))
        if utils.in_range(x_current=self.rect.x, y_current=self.rect.y,
                          x_end=self.real_end_x, y_end=self.real_end_y,
                          myincrement=myinc) == True:
            return False
        # todo: if the sprite has 'run into' a wall or other obstacle
        # return False and discontinue.
        if myint == 0:
            if self.rect.y < self.real_end_y:
                self.rect = self.rect.move(0, myinc)
            elif self.rect.y > self.real_end_y:
                self.rect = self.rect.move(0, myinc * -1)
        elif myint == 1:
            if self.rect.x < self.real_end_x:
                self.rect = self.rect.move(myinc, 0)
            elif self.rect.x > self.real_end_y:
                self.rect = self.rect.move(myinc * -1, 0)
        utils.log_text("testing.txt", "x: {}, y: {}".format(self.rect.x, self.rect.y))
        return True

# -------------------------------------------------------
#                     class DrawSprite
# -------------------------------------------------------

class HandleMovingSprite:
    def __init__(self, image_path):
        self.begin_x, self.begin_y = -1, -1
        self.end_x, self.end_y = -1, -1
        if os.path.isfile(image_path) == False:
            self.image_path = utils.get_filepath(image_path)
        else:
            self.image_path = image_path
        if os.path.isfile(self.image_path) == False:
            s = "This does not seem to be a valid file path: {}"
            s = s.format(self.image_path)
            raise ValueError(s)
        # ----

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        # print("screen width: {}, screen height: {}".format(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data(self, begin_x, begin_y, end_x, end_y):
        self.begin_x, self.begin_y = begin_x, begin_y
        self.end_x, self.end_y = end_x, end_y
        # ----
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping = True
        # ----
        self.mysprite = MyMovingSprite()
        self.mysprite.read_data(begin_x=self.begin_x, begin_y=self.begin_y,
                                end_x=self.end_x, end_y=end_y, image_filepath=self.image_path)
        self.mybackground = MySprite("background01.png", 0, 0)

    def _get_filepath(self, filename):
        filepath = filename
        if os.path.isfile(filepath) == False:
            # print("Checking whether the image file was not a full filepath...")
            filepath = utils.get_filepath(filepath)
            if filepath is None:
                raise ValueError("Error: This file does not exist: {}".format(filepath))
            if len(filepath) == 0:
                raise ValueError("Error: This filepath is empty.")
            # print("This filepath: {}".format(self.filepath))
            return filepath
        else:
            return filepath

    def fire_sprite(self):
        self.read_data(self.begin_x, self.begin_y, self.end_x, self.end_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_f:
                    self.fire_sprite()
                else:
                    # self.user_text += event.unicode
                    pass

    def update(self):
        if not self.mysprite is None:
            if self.mysprite.move_image() == False:
                self.all_sprites = pygame.sprite.Group()
                self.mysprite = None
            # self.keep_looping = False
        # pass

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        # utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
        #                   height_offset=50, line_length=60,
        #                   color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.add(self.mybackground)
        if not self.mysprite is None:
            self.all_sprites.add(self.mysprite)
        # print("x,y: {},{}".format(self.mysprite.begin_x, self.mysprite.begin_y))
        # print("end_x, end_y: {},{}".format(self.end_x, self.end_y))
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        # self.clock.tick(1)
        self.mysprite.show_image = True
        while self.keep_looping:
            self.clock.tick(30)
            self.handle_events()
            self.update()
            self.draw()

# -------------------------------------------------------
#                     class ColtrolYourSprite
# -------------------------------------------------------
class ControlMovingSprite:
    def __init__(self, image_name):
        self.x, self.y = -1, -1
        self.x_end, self.y_end = -1, -1
        self.image_path = utils.get_filepath(image_name)
        if self.image_path is None: raise ValueError("Error")
        # ----
        self.draw_moving_sprite = None

    def read_data(self, x, y, x_end, y_end):
        self.x, self.y = x, y
        self.x_end, self.y_end = x_end, y_end
        if not self.x in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
            raise ValueError("Error")
        if not self.y in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
            raise ValueError("Error")
        if not self.x_end in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
            raise ValueError("Error")
        if not self.y_end in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
            raise ValueError("Error")
        # ----
        # self.image_path = utils.get_filepath(image_name)
        # if self.image_path is None:
        #     raise ValueError("Error")
        # ----
        self.draw_moving_sprite = HandleMovingSprite(image_path=self.image_path)
        self.draw_moving_sprite.read_data(self.x, self.y, self.x_end, self.y_end)
        self.draw_moving_sprite.main()

    def fire_off_sprite(self):
        pass

    def reset_sprite(self):
        pass

# -------------------------------------------------------
#                     class MySpriteStrip
# -------------------------------------------------------

class MySpriteStrip(pygame.sprite.Sprite):
    def __init__(self, image_filename, x, y):
        super().__init__()
        # self.init_pygame()
        # self.all_sprites = pygame.sprite.Group()
        self.x, self.y = x, y
        filepath = utils.get_filepath(image_filename)
        self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE * 3, constants.TILESIZE * 3))
        self.image = pygame.transform.scale(self.image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)


# =======================================

if __name__ == "__main__":
    myobject = ControlMovingSprite(image_name="apple.png")
    myobject.read_data(x=1, y=8, x_end=1, y_end=1)
    # start_x = 1
    # start_y = 8
    # end_x = 4
    # end_y = 2
    # mydialog = MyDrawSprite(start_x, start_y, end_x, end_y, filename="Bee.png")
    # mydialog.main()