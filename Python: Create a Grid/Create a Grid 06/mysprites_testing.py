import random
import pygame
import utils
import constants
import os

# -------------------------------------------------------
#                     class MySmallImage
# -------------------------------------------------------
class MySmallImage(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width=0, height=0):
        super().__init__()
        if os.path.isfile(filename) == False:
            filename = utils.get_filepath(filename)
            if filename is None:
                s = "This doesn't seem to be a valid file path: {}".format(filename)
                raise ValueError(s)
        self.filepath = filename
        # ----
        self.x, self.y = x, y
        self.width, self.height = width, height
        # ----
        if self.width == 0 or self.height == 0:
            self.width = constants.SCREEN_WIDTH
            self.height = constants.SCREEN_HEIGHT
        # ----
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.width, self.y * self.height)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def debug_print(self):
        s = "self.x: {}, self.y: {}\n".format(self.x, self.y)
        s += "self.width: {}, self.height: {}\n".format(self.width, self.height)
        s += "self.image_filename: {}\n".format(self.image_filename)
        s += "movement_action: {}\n".format(self.movement_action)
        s += "direction: {}\n".format(self.direction)
        print(s)

# -------------------------------------------------------
#                     class MyImage
# -------------------------------------------------------
class MyImage(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width=0, height=0):
        super().__init__()
        if os.path.isfile(filename) == False:
            filename = utils.get_filepath(filename)
            if filename is None:
                s = "This doesn't seem to be a valid file path: {}".format(filename)
                raise ValueError(s)
        self.filepath = filename
        # ----
        self.x, self.y = x, y
        self.width, self.height = width, height
        # ----
        if self.width == 0 or self.height == 0:
            self.width = constants.SCREEN_WIDTH
            self.height = constants.SCREEN_HEIGHT
        # ----
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.width, self.y * self.height)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def debug_print(self):
        s = "self.x: {}, self.y: {}\n".format(self.x, self.y)
        s += "self.width: {}, self.height: {}\n".format(self.width, self.height)
        s += "self.image_filename: {}\n".format(self.image_filename)
        s += "movement_action: {}\n".format(self.movement_action)
        s += "direction: {}\n".format(self.direction)
        print(s)

# -------------------------------------------------------
#                     class MySprite
# -------------------------------------------------------
class MySprite(pygame.sprite.Sprite):
    '''This class loads just ONE image.'''
    def __init__(self, sprite_name, filename, x, y, movement_action, direction, width=0, height=0):
        super().__init__()
        print("In MySprite.__init__")
        self.movement_action = movement_action
        if not self.movement_action in constants.MOVEMENT_ACTION:
            raise ValueError("Error")
        self.direction = direction
        if not self.direction in ["up", "down", "right", "left"]:
            raise ValueError("Error")
        # ----
        self.sprite_name = sprite_name
        temp = os.path.join("data", "images", "sprites")
        sprite_names = utils.get_subdirectories(temp)
        if not self.sprite_name in sprite_names:
            s = "This doesn't seem to be a sprite name: {}\n".format(self.sprite_name)
            s += "Sprite names: {}".format(sprite_names)
            raise ValueError(s)
        # ---- filename ----
        temp = os.path.join("data", "images", "sprites",
                            self.sprite_name, self.movement_action, self.direction)
        filenames = os.listdir(temp)
        if not filename in filenames:
            s = "This doesn't seem to be a valid file name: {}\n".format(filename)
            s += "Here are the filenames: {}".format(filenames)
            raise ValueError(s)
        # ----
        self.filename = filename
        self.filepath = os.path.join("data", "images", "sprites",
                                     self.sprite_name, self.movement_action,
                                     self.direction, self.filename)
        if os.path.isfile(self.filepath) == False:
            s = "This doesn't seem to be a valid file: {}".format(self.filepath)
            raise ValueError(s)
        # ----
        self.x, self.y = x, y
        self.width, self.height = width, height
        # ----
        if self.width == 0 or self.height == 0:
            self.width = constants.SCREEN_WIDTH
            self.height = constants.SCREEN_HEIGHT
        # ----
        self.image = pygame.image.load(self.filepath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.width, self.y * self.height)

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def debug_print(self):
        s = "self.x: {}, self.y: {}\n".format(self.x, self.y)
        s += "self.width: {}, self.height: {}\n".format(self.width, self.height)
        s += "self.filepath: {}\n".format(self.filepath)
        s += "movement_action: {}\n".format(self.movement_action)
        s += "direction: {}\n".format(self.direction)
        print(s)

# -------------------------------------------------------
#                     class MyDancingSprite
# -------------------------------------------------------

class MyDancingSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, direction, x, y, movement_action, maximum_loops):
        super().__init__()
        sprite_names = utils.get_subdirectories(constants.SPRITES_SUBDIRECTORY)
        if not sprite_name in sprite_names:
            s = "I don't recognize this as the name of a sprite: {}\n".format(sprite_name)
            s += "Here are the sprite names: {}".format(sprite_names)
            raise ValueError(s)
        self.sprite_name = sprite_name
        # ----
        self.direction = direction
        if not self.direction in ["up", "down", "left", "right"]: raise ValueError("Error")
        self.x, self.y = x, y
        self.real_x = self.x * constants.TILESIZE
        self.real_y = self.y * constants.TILESIZE
        self.movement_action = movement_action
        if not self.movement_action in constants.MOVEMENT_ACTION: raise ValueError("Error")
        # ----
        self.filepath = os.path.join("data", "images", "sprites", sprite_name, self.movement_action, self.direction)
        if os.path.isdir(self.filepath) == False:
            s = "This is not a valid directory: {}".format(self.filepath)
            raise ValueError(s)
        # ----
        self.init_pygame()
        # ----
        self.counter = 0
        self.number_of_loops = 0
        self.maximum_loops = maximum_loops
        self.inner = self.load_sprites()
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        # ----
        self.mybackground = MyImage(filename="background01.png", x=0, y=0,
                                     width=constants.SCREEN_WIDTH,
                                     height=constants.SCREEN_HEIGHT)
        # ----
        self.keep_looping = True

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def load_sprites(self):
        filenames = os.listdir(self.filepath)
        if filenames is None: raise ValueError("Error")
        if len(filenames) == 0:
            s = "This doesn't seem to be a valid directory: {}".format(self.filepath)
            raise ValueError(s)
        # ----
        sprite_list = []
        for filename in filenames:
            new_filepath = os.path.join(self.filepath, filename)
            if os.path.isfile(new_filepath) == False:
                s = "This is not a valid filepath: {}".format(new_filepath)
                raise ValueError(s)
            # ----
            # sprite_name, filename, x, y, movement_action, direction, width=0, height=0
            mysprite = MySprite(sprite_name=self.sprite_name, filename=filename,
                                x=self.x, y=self.y,
                                movement_action=self.movement_action,
                                direction=self.direction,
                                width=constants.TILESIZE, height=constants.TILESIZE)
            print("in load_sprites. filename added: {}".format(filename))
            sprite_list.append(mysprite)
        self.counter = 0
        return sprite_list

    # def set_next_sprite(self, x_offset, y_offset):
    #     old_x, old_y = self.x, self.y
    #     self.x += x_offset
    #     self.y += y_offset
    #     if len(self.inner) == 1:
    #         self.image = self.inner[0]
    #         self.rect = self.image.get_rect()
    #         self.rect = self.rect.move((self.x) * constants.TILESIZE, (self.y) * constants.TILESIZE)
    #         return True
    #     # ----
    #     if self.counter >= len(self.inner):
    #         t = "len(self.inner) = {}; self.counter = {}".format(len(self.inner), self.counter)
    #         s = "{}\n".format(t)
    #         raise ValueError(s)
    #     try:
    #         self.image = self.inner[self.counter]
    #     except Exception as e:
    #         t = "len(self.inner) = {}; self.counter = {}".format(len(self.inner), self.counter)
    #         s = "{}\n{}\n".format(e, t)
    #         raise ValueError(s)
    #     self.rect = self.image.get_rect()
    #     self.rect = self.rect.move((self.x + x_offset) * constants.TILESIZE, (self.y + y_offset) * constants.TILESIZE)
    #     self.counter += 1
    #     if len(self.inner) == self.counter + 1:
    #         self.counter = 0
    #     return self.x, self.y

    # ----------------------------------------------------

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

    def update(self):
        pass

    def draw(self):
        print("---- def draw BEGIN ----")
        print("def draw just entered")
        print("Here is the current tile being drawn:")
        self.inner[self.counter].debug_print()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.mybackground)
        self.all_sprites.add(self.inner[self.counter])
        # -----------------------------------------
        print("counter: {}".format(self.counter))
        self.counter += 1
        print("len(self.inner): {}, self.counter: {}".format(len(self.inner), self.counter))
        if len(self.inner) <= self.counter:
            self.counter = 0
            self.number_of_loops += 1
        if self.number_of_loops >= self.maximum_loops:
            # stop looping
            self.counter = 0
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()
        print("---- def draw END ----")

    def main(self):
        # self.clock.tick(1)
        # self.mysprite.show_image = True
        while self.keep_looping:
            self.clock.tick(3)
            self.handle_events()
            self.update()
            self.draw()

    def update_classes(self, all_sprites):
        all_sprites.add(self.inner[self.counter])
        self.counter += 1
        if len(self.inner) >= self.counter:
            self.counter = 0
        return all_sprites

    def debug_print(self):
        s = "filepath: {}\n".format(self.filepath)
        s += "self_x, self_y: {},{}\n".format(self.x, self.y)
        s += "real_x, real_y: {},{}\n".format(self.real_x, self.real_y)
        s += "movement_action: {}\n".format(self.movement_action)
        s += "direction: {}\n".format(self.direction)
        print(s)
        print("---- self.inner ----")
        for elem in self.inner:
            elem.debug_print()
            print("----")
        print("There are {} sprites in self.inner.".format(len(self.inner)))
# -------------------------------------------------------
#                     class DrawSprite
# -------------------------------------------------------

class HandleDancingSprite:
    def __init__(self, x, y, directory_name, tilesize, direction, movement_action, obstacles):
        # ----
        self.init_pygame()
        # ----
        self.x, self.y = x, y
        self.directory_path = directory_name
        self._movement_action = movement_action
        if not self._movement_action in constants.MOVEMENT_ACTION:
            raise ValueError("Error")
        if os.path.isdir(self.directory_path) == False:
            self.directory_path = os.path.join("data", "images", "sprites", self.directory_path)
            if os.path.isdir(self.directory_path) == False:
                s = "This does not seem to be a valid file directory: {}"
                s = s.format(self.directory_path)
                raise ValueError(s)
        self.image_directory = self.directory_path
        self.tilesize = tilesize
        if self.tilesize > constants.TILESIZE * 4: raise ValueError("Error")
        if self.tilesize < constants.TILESIZE: raise ValueError("Error")
        self.direction = direction
        if not self.direction in ["down", "up", "left", "right"]: raise ValueError("Error")
        # self.sprites = MyDancingSprite(self.image_directory, direction=self.direction,
        #                                x=self.x, y=self.y, movement_action=movement_action)
        self.obstacles = obstacles
        if self.obstacles is None: raise ValueError("Error")
        if len(self.obstacles) == 0: raise ValueError("Error")
        # ----
        self.mybackground = MySprite("background01.png", 0, 0)
        # ----
        self.keep_looping = True
        self.loop_counter = 0
        # ----
        self.sprites = None
        self.read_data()

    @property
    def movement_action(self):
        """I'm the 'x' property."""
        return self._movement_action

    @movement_action.setter
    def movement_action(self, value):
        if not value in constants.MOVEMENT_ACTION: raise ValueError("Error")
        self.loop_counter = 0
        self._movement_action = value
        self.read_data()

    @movement_action.deleter
    def movement_action(self):
        del self._movement_action

    def read_data(self):
        self.sprites = MyDancingSprite(self.image_directory, direction=self.direction,
                                       x=self.x, y=self.y, movement_action=self.movement_action)

    # def move_sprite_strip(self):
    #     self.x += constants.TILESIZE

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        # print("screen width: {}, screen height: {}".format(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    # def move_down(self):
    #     new_y = self.y + 0.25
    #     if self.obstacles.collision(self.x, new_y) == False:
    #         self.sprites.move_down()
    #         self.y = new_y

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
                    # --------------------------
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                    self.movement_action = "walking"
                    # self.move_down()
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                    self.movement_action = "walking"
                    new_x = self.x - 1
                    if self.obstacles.collision(new_x, self.y) == False:
                        self.x = new_x
                elif event.key == pygame.K_UP:
                    self.direction = "up"
                    self.movement_action = "walking"
                    new_y = self.y - 1
                    if self.obstacles.collision(self.x, new_y) == False:
                        self.y = new_y
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
                    self.movement_action = "walking"
                    new_x = self.x + 1
                    if self.obstacles.collision(new_x, self.y) == False:
                        self.x = new_x
                    # --------------------------
                elif event.key == pygame.K_f:
                    pass
                    # self.fire_sprite()
                else:
                    # self.user_text += event.unicode
                    pass

    def update(self):
        if self.movement_action == "walking":
            if self.direction == "down":
                print("self.x, self.y: {},{}".format(self.x, self.y))
                if self.obstacles.collision(self.x, self.y) == True:
                    raise NotImplemented
                    return False
            self.loop_counter += 1
            myoffset = 1 / len(self.sprites)
            self.x, self.y = self.sprites.set_next_sprite(0, myoffset)
            if len(self.sprites) < self.loop_counter:
                self.loop_counter = 0
                self.movement_action = "standing"
        else:
            self.sprites.set_next_sprite(0, 0)
        # if not self.mysprite is None:
        #     if self.mysprite.move_image() == False:
        #         self.all_sprites = pygame.sprite.Group()
        #         self.mysprite = None
        #     # self.keep_looping = False
        # # pass

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        # utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
        #                   height_offset=50, line_length=60,
        #                   color=constants.BLACK)
        # -----------------------------------------
        # self.all_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.mybackground)
        # self.all_sprites = self.sprites.update_class(self.all_sprites)
        # self.all_sprites.add(self.sprite_sheet)
        self.all_sprites.add(self.sprites)
        # print("x,y: {},{}".format(self.mysprite.begin_x, self.mysprite.begin_y))
        # print("end_x, end_y: {},{}".format(self.end_x, self.end_y))
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        # self.clock.tick(1)
        # self.mysprite.show_image = True
        while self.keep_looping:
            self.clock.tick(3)
            self.handle_events()
            self.update()
            self.draw()

# # -------------------------------------------------------
# #                     class ColtrolYourSprite
# # -------------------------------------------------------
# class ControlMovingSprite:
#     def __init__(self, image_name):
#         self.x, self.y = -1, -1
#         self.x_end, self.y_end = -1, -1
#         self.image_path = utils.get_filepath(image_name)
#         if self.image_path is None: raise ValueError("Error")
#         # ----
#         self.draw_moving_sprite = None
#
#     def read_data(self, x, y, x_end, y_end):
#         self.x, self.y = x, y
#         self.x_end, self.y_end = x_end, y_end
#         if not self.x in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
#             raise ValueError("Error")
#         if not self.y in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
#             raise ValueError("Error")
#         if not self.x_end in list(range(0, constants.NUMBER_OF_BLOCKS_WIDE)):
#             raise ValueError("Error")
#         if not self.y_end in list(range(0, constants.NUMBER_OF_BLOCKS_HIGH)):
#             raise ValueError("Error")
#         # ----
#         # self.image_path = utils.get_filepath(image_name)
#         # if self.image_path is None:
#         #     raise ValueError("Error")
#         # ----
#         self.draw_moving_sprite = HandleMovingSprite(image_path=self.image_path)
#         self.draw_moving_sprite.read_data(self.x, self.y, self.x_end, self.y_end)
#         self.draw_moving_sprite.main()
#
#     def fire_off_sprite(self):
#         pass
#
#     def reset_sprite(self):
#         pass




# =======================================

def debug_handle_dancing_sprite():
    # myobject = ControlMovingSprite(image_name="apple.png")
    # myobject.read_data(x=1, y=8, x_end=1, y_end=1)
    zone_name = "swindon"
    map_name = "map00"
    from graphics_environment import Obstacles
    myobstacles = Obstacles(zone_name, map_name)
    myobstacles.read_data()

    directory_name = "dragon_red_01"
    direction = "down"
    x, y = 5, 5
    tilesize = constants.TILESIZE
    movement_action = "standing"
    if not movement_action in constants.MOVEMENT_ACTION:
        s = "I don't recognize this as a movement action: {}".format(movement_action)
        raise ValueError(s)
    mydragon = HandleDancingSprite(x=x, y=y, directory_name=directory_name,
                                   tilesize=tilesize, direction=direction,
                                   movement_action=movement_action,
                                   obstacles=myobstacles)
    # mydragon.read_data()
    mydragon.main()
    # start_x = 1
    # start_y = 8
    # end_x = 4
    # end_y = 2
    # mydialog = MyDrawSprite(start_x, start_y, end_x, end_y, filename="Bee.png")
    # mydialog.main()

def debug_my_dancing_sprite():
    # image_directory = os.path.join("data", "images", "sprites", "testing_strips")
    sprite_name = "testing_strips"
    # sprite_name = "dragon_red_01"
    # direction = "down"
    # direction = "up"
    # direction = "right"
    direction = "left"
    myspriteobect = MyDancingSprite(sprite_name=sprite_name,
                                    direction=direction, x=5, y=5,
                                    movement_action="flying",
                                    maximum_loops=100)
    print("Debugging ----print----begin")
    myspriteobect.debug_print()
    print("Debugging ----print----end")
    myspriteobect.main()

# def debug_mysprite():
#     filepath = os.path.join("data", "images", "sprites", "dragon_red_01", "walking", "down", "down01.png")
#     myobject = MySprite(filepath, x=5, y=5)
#     myobject.main()

if __name__ == "__main__":
    # debug_my_sprite_sheet()
    debug_my_dancing_sprite()
    # debug_handle_dancing_sprite()