import time
import pygame
import constants
import random
import utils
import os, sys
from speech import Speech
from mysprites import MySprite
from mysprites_testing import MyImage

# ------------------------------------------------------------
#                    class DialogDisplayImage
# ------------------------------------------------------------
class DialogDisplayImage:
    def __init__(self, image_name):
        super().__init__()
        if image_name is None: raise ValueError("Error")
        if len(image_name) == 0: raise ValueError("Error")
        # ----
        filepath = ""
        if not os.path.isfile(image_name):
            filepath = utils.get_filepath(image_name)
        else:
            filepath = image_name

        self.mypicture = MyImage(filepath, 0, 0)
        # ----
        self.init_pygame()
        # ----
        self.keep_looping = True

    def init_pygame(self):
        """I'm including this for debugging."""
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

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
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        # self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.mypicture)
        # self.all_sprites.add(self.inner[self.counter])
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        # self.clock.tick(1)
        # self.mysprite.show_image = True
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.update()
            self.draw()

    # def update_classes(self, all_sprites):
    #     all_sprites.add(self.inner[self.counter])
    #     self.counter += 1
    #     if len(self.inner) >= self.counter:
    #         self.counter = 0
    #     return all_sprites

    # def debug_print(self):
    #     s = "filepath: {}\n".format(self.filepath)
    #     s += "self_x, self_y: {},{}\n".format(self.x, self.y)
    #     s += "real_x, real_y: {},{}\n".format(self.real_x, self.real_y)
    #     s += "movement_action: {}\n".format(self.movement_action)
    #     s += "direction: {}\n".format(self.direction)
    #     print(s)
    #     print("---- self.inner ----")
    #     for elem in self.inner:
    #         elem.debug_print()
    #         print("----")
    #     print("There are {} sprites in self.inner.".format(len(self.inner)))

# ------------------------------------------------------------
#                    class DialogViewMapTiles
# ------------------------------------------------------------

# class DialogViewMapTiles:
#     def __init__(self, line_width=50):
#         self.width = constants.SCREEN_WIDTH
#         self.height = constants.SCREEN_HEIGHT
#         self.line_width = line_width
#         # --------------------------------------
#         self.all_sprites = pygame.sprite.Group()
#         self.init_pygame()
#         # --------------------------------------
#         self.BG_COLOR = constants.UGLY_PINK
#         # --------------------------------------
#         self.inner = []
#         self.keep_looping = True
#         # --------------------------------------
#
#     def init_pygame(self):
#         pygame.init()
#         # self.BG_COLOR = constants.WHITE
#         self.clock = pygame.time.Clock()
#         pygame.display.set_caption("Enter {}".format(constants.TITLE))
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         # self.font = pygame.font.Font(None, 40)
#         self.font = pygame.font.Font(None, 30)
#         # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)
#
#     def read_data(self):
#         for x in range(constants.NUMBER_OF_BLOCKS_WIDE):
#             for y in range(constants.NUMBER_OF_BLOCKS_HIGH):
#
#         for col, tiles in enumerate(mytiles):
#             list_tiles = tiles.split(";")
#             list_tiles = [i.strip() for i in list_tiles if len(i.strip()) > 0]
#             for row, tile in enumerate(list_tiles):
#                 if not tile == "..":
#                     tile_dict = utils.get_dictionary(file_tiles, tile)
#                     if tile_dict is None:
#                         raise ValueError("tile: {}".format(tile))
#                     tile_dict["x"] = row
#                     tile_dict["y"] = col
#                     my_obstacle = Obstacle(tile_dict)
#                     self.obstacles.append(my_obstacle)
#                 elif tile == "..":
#                     pass
#                 else:
#                     s = "Error! I don't recognize this: {}".format(tile)
#                     raise ValueError(s)
#
#     def handle_events(self):
#         # catch all events here
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.keep_looping = False
#                 return True
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     self.keep_looping = False
#                     return True
#                 else:
#                     print("I don't recognize this event.key in handle_events: {}".format(event.key))
#
#     def update_classes(self, all_sprites):
#         for elem in self.obstacles:
#             all_sprites.add(elem)
#         return all_sprites
#
#     def draw(self):
#         self.screen.fill(self.BG_COLOR)
#         self.update_classes(self.all_sprites)
#         # ----
#         self.all_sprites.update()
#         self.all_sprites.draw(self.screen)
#         # ----
#         pygame.display.flip()
#
#     def main(self):
#         self.clock.tick(constants.FRAME_RATE)
#         # self.window_text_list = self.separate_text_into_lines(
#         #     text, self.line_width)
#         while self.keep_looping:
#             self.handle_events()
#             self.draw()
#         # self.save_data()
#         # return self.text
#         # return self.return_value
#
#     def debug_print(self):
#         for elem in self.obstacles:
#             elem.debug_print()

# ------------------------------------------------------------
#                    class DialogShowQuests
# ------------------------------------------------------------

class DialogShowQuests:
    def __init__(self, height=900, width=500, line_width=50):
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        self.init_pygame()
        # --------------------------------------
        self.user_text = ""
        self.text = ""
        self.text_color = constants.BLACK
        self.background_colour_of_text_box = constants.LIGHTGREY
        # --------------------------------------
        self.display_quests = []
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.font = pygame.font.Font(None, 40)
        self.font = pygame.font.Font(None, 30)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def read_data(self):
        # self.display_quests = utils.get_all_quests()
        self.display_quests = utils.get_accepted_quests()

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        def is_wrong():
            self.background_colour_of_text_box = constants.RED
            self.user_text = ""
            return False
        # ----
        command = ""
        for event in pygame.event.get():
            def invalid_text():
                self.background_colour_of_text_box = constants.RED
                self.user_text = ""
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.background_colour_of_text_box = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    temp_text = self.user_text
                    mylist = temp_text.split(" ")
                    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
                    # if len(mylist) != 2:
                    #     invalid_text()
                    #     return False
                    direction = mylist[0]
                    if not direction in ["show", "reset", "read"]:
                        invalid_text()
                        return False
                    command = ' '.join(mylist[1:])
                    # ----
                    if direction == "show":
                        if command == "accepted":
                            self.display_quests = utils.get_accepted_quests()
                            # print(self.display_quests)
                        elif command == "completed":
                            self.display_quests = utils.get_completed_quests()
                            # print(self.display_quests)
                        elif command == "all":
                            self.display_quests = utils.get_all_quests()
                            # print(self.display_quests)
                        else:
                            invalid_text()
                            return False
                    elif direction == "reset":
                        if not command in constants.QUEST_NAMES:
                            invalid_text()
                            return False
                        if utils.reset_conversation_by_name(command) == False:
                            raise NotImplemented
                    elif direction == "read":
                        mydict = utils.get_quest(command)
                        mylist = []
                        s = "Bring {} {} to {}".format(mydict["quest_area_number_of_success_items"],
                                                       mydict["quest_area_success_item"],
                                                       mydict["npc_name_receiver"])
                        mylist.append(s)
                        s = "{}".format(mydict["quest_summary"])
                        mylist.append(s)
                        self.display_quests = mylist
                    else:
                        raise ValueError("Error: I don't recognize this: {}".format(direction))
                    self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        pygame.draw.rect(self.screen, self.background_colour_of_text_box, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        pass
        # self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_quests, self.font, width_offset=20, height_offset=20, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = []
        # mylist.append("Return = Exit")
        # mylist.append("ESC = Exit")
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
        #                   color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        # return self.return_value

# ------------------------------------------------------------
#                    class DialogUseItemInInventory
# ------------------------------------------------------------

class DialogUseItemInInventory:
    def __init__(self, player, height=900, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.user_text = ""
        self.text_color = constants.BLACK
        self.background_colour_of_text_box = constants.LIGHTGREY
        # --------------------------------------
        # mylist = []
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        self.display_player_goods = []
        self.npc_goods_display = []
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        self.warning = "You are at MAXIMUM heath!"

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def display_text(self):
        mylist = []
        mylist.append("{} the {}".format(self.player.name, self.player.profession))
        mylist.append("index | name | (cost) | hps | #")
        mylist.append("HPs: {}".format(self.player.hit_points))
        mylist.append(" ")
        return mylist

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        def is_wrong():
            self.background_colour_of_text_box = constants.RED
            self.user_text = ""
            return False
        # ----
        for event in pygame.event.get():
            def eat_drink_use(mylist):
                item_name = "{} {}".format(mylist[1], mylist[2])
                if item_name is None:
                    raise ValueError("Error")
                if not item_name in constants.ITEMS_PLAYER_CAN_USE:
                    s = "item_name: {}\n".format(item_name)
                    s += ', '.join(constants.ITEMS_PLAYER_CAN_USE)
                    raise ValueError(s)
                an_item = self.player.inventory.get_item_by_name(item_name)
                if an_item is None:
                    return is_wrong()
                # ----
                self.player.hit_points += (an_item.hp * number_of_items)
                if self.player.hit_points > self.player.max_hit_points:
                    self.player.hit_points = self.player.max_hit_points
                    self.background_colour_of_text_box = constants.RED
                    self.user_text = self.warning
                if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                    raise ValueError("Error")
                    # return is_wrong()
            # ----
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if self.user_text == self.warning:
                    self.user_text = ""
                self.background_colour_of_text_box = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.user_text is None: raise ValueError("Error")
                    if len(self.user_text) == 0: raise ValueError("Error")
                    if utils.is_int(self.user_text): raise ValueError("Error!")
                    # ----
                    mylist = self.user_text.split((" "))
                    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
                    if not len(mylist) in [3, 4]:
                        return is_wrong()
                    if not mylist[0] in ["drink", "eat", "add", "remove", "use"]:
                        # 'add' and 'remove' are for debugging ONLY!!!!
                        return is_wrong()
                    # ----
                    if utils.check_for_all(mylist) == False:
                        try:
                            number_of_items = int(mylist[3])
                        except:
                            number_of_items = 1
                    elif mylist[3] == "all":
                        if mylist[0] in ["add"]:
                            s = "The command must be one that takes something out of the player's inventory. It cannot be added."
                            print(s)
                            return is_wrong()
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        an_item = self.player.inventory.get_item_by_name(item_name)
                        if an_item is None:
                            s = "I didn't find this item: -{}-".format(item_name)
                            raise ValueError(s)
                        number_of_items = an_item.units
                        # s = "number_of_items: {}, item_name: {}".format(number_of_items, item_name)
                        # print(s)
                    else:
                        raise ValueError("Error")
                    # ----
                    command = mylist[0]
                    item_name = "{} {}".format(mylist[1], mylist[2])
                    # ---- ---- ---- ----
                    if command in ["eat", "drink"]:
                        eat_drink_use(mylist)
                        # an_item = self.player.inventory.get_item_by_name(item_name)
                        # if an_item is None:
                        #     raise ValueError("Error")
                        # self.player.hit_points += (an_item.hp * number_of_items)
                        # if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                        #     return is_wrong()
                    elif command in ["add"]:
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        if item_name is None:
                            raise ValueError("Error")
                        self.player.inventory.add_item_by_name_for_dialog(item_name, number_of_items)
                        self.user_text = ""
                        # npc_goods = self.player.inventory.display_string()
                        # self.npc_goods_display = utils.format_npc_goods(npc_goods)
                    elif command in ["remove"]:
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        if item_name is None:
                            raise ValueError("Error")
                        if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                            return is_wrong()
                        # npc_goods = self.player.inventory.display_string()
                        # self.npc_goods_display = utils.format_npc_goods(npc_goods)
                        self.user_text = ""
                    elif command == "use":
                        eat_drink_use(mylist)
                    else:
                        return is_wrong()
                    # self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        pygame.draw.rect(self.screen, self.background_colour_of_text_box, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_text(), self.font, width_offset=20, height_offset=275, line_length=60,
                          color=constants.BLACK)

        self.display_player_goods = self.player.inventory.display_string()
        utils.talk_dialog(self.screen, self.display_player_goods, self.font, width_offset=20, height_offset=400, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        self.player.inventory.save_data()
        # self.save_data()
        # return self.text
        # return self.return_value

# ------------------------------------------------------------
#                    class DialogPlayerModels
# ------------------------------------------------------------

class DialogPlayerModels:
    def __init__(self, height=400, line_width=50):
        # self.height = height
        # self.width = height
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # ----
        self.display_text = "What would you like your character to look like? (1/2/3/4/5/6/7/8)"
        self.number_chosen = -1
        self.message = ""
        # ----
        self.init_pygame()
        # ----
        self.keep_looping = True
        # ----
        self.all_sprites = pygame.sprite.Group()
        filepath = utils.get_filepath("splash_screen_square.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.image = pygame.transform.scale(self.image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        # ----
        # filepath01 = os.path.join("data", "images", "player_images", "wanderer01", "down_health_100.png")
        filepath01 = os.path.join("data", "images", "player_images", "braids01", "down_health_100.png")
        filepath02 = os.path.join("data", "images", "player_images", "braids02", "down_health_100.png")
        filepath03 = os.path.join("data", "images", "player_images", "hooded_figure01", "down_health_100.png")
        filepath04 = os.path.join("data", "images", "player_images", "hooded_figure02", "down_health_100.png")
        filepath05 = os.path.join("data", "images", "player_images", "magic01", "down_health_100.png")
        filepath06 = os.path.join("data", "images", "player_images", "magic02", "down_health_100.png")
        filepath07 = os.path.join("data", "images", "player_images", "warrior01", "down_health_100.png")
        filepath08 = os.path.join("data", "images", "player_images", "warrior02", "down_health_100.png")
        # path = "data/images/player_images/wanderer01/down_health_100.png"
        self.my_picture01 = MySpriteNew(image_filepath=filepath01, x=0, y=0)
        self.my_picture02 = MySpriteNew(image_filepath=filepath02, x=1, y=0)
        self.my_picture03 = MySpriteNew(image_filepath=filepath03, x=2, y=0)
        self.my_picture04 = MySpriteNew(image_filepath=filepath04, x=3, y=0)
        self.my_picture05 = MySpriteNew(image_filepath=filepath05, x=0, y=1.2)
        self.my_picture06 = MySpriteNew(image_filepath=filepath06, x=1, y=1.2)
        self.my_picture07 = MySpriteNew(image_filepath=filepath07, x=2, y=1.2)
        self.my_picture08 = MySpriteNew(image_filepath=filepath08, x=3, y=1.2)
        # self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        # self.my_picture01.move_image_0()
        # self.my_picture02.move_image_1()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.GREEN
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)

    # def get_model(self):
    #     mylist = ["braids01", "braids02", "hooded_figure01", "hooded_figure02"]
    #     mylist += ["magic01", "magic02", "warrior01", "warrior02"]
    #     return mylist[self.number_chosen+1]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                # self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # mytext = self.user_text.lower().strip()
                    self.keep_looping = False
                elif event.key == pygame.K_1:
                    mylist = ["You chose: 1"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.message = "braids01"
                elif event.key == pygame.K_2:
                    mylist = ["You chose: 2"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.number_chosen = 2
                    self.message = "braids02"
                elif event.key == pygame.K_3:
                    mylist = ["You chose: 3"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.number_chosen = 3
                    self.message = "hooded_figure01"
                elif event.key == pygame.K_4:
                    mylist = ["You chose: 4"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.number_chosen = 4
                    self.message = "hooded_figure02"
                elif event.key == pygame.K_5:
                    mylist = ["You chose: 5"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.number_chosen = 5
                    self.message = "magic01"
                elif event.key == pygame.K_6:
                    mylist = ["You chose: 6"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.number_chosen = 6
                    self.message = "magic02"
                elif event.key == pygame.K_7:
                    mylist = ["You chose: 7"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.message = "warrior01"
                elif event.key == pygame.K_8:
                    mylist = ["You chose: 8"]
                    mylist.append(" ")
                    mylist.append("Press <EXC> or <RETURN> to continue.")
                    self.display_text = mylist
                    self.message = "warrior02"
                else:
                    self.display_text = []
                    self.message = None

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites.add(self.my_picture01)
        self.all_sprites.add(self.my_picture02)
        self.all_sprites.add(self.my_picture03)
        self.all_sprites.add(self.my_picture04)
        utils.talk_dialog(self.screen, ["(1)"], self.font, 70, 180)
        utils.talk_dialog(self.screen, ["(2)"], self.font, 260, 180)
        utils.talk_dialog(self.screen, ["(3)"], self.font, 450, 180)
        utils.talk_dialog(self.screen, ["(4)"], self.font, 640, 180)
        self.all_sprites.add(self.my_picture05)
        self.all_sprites.add(self.my_picture06)
        self.all_sprites.add(self.my_picture07)
        self.all_sprites.add(self.my_picture08)
        y2 = 405
        utils.talk_dialog(self.screen, ["(5)"], self.font, 70, y2)
        utils.talk_dialog(self.screen, ["(6)"], self.font, 260, y2)
        utils.talk_dialog(self.screen, ["(7)"], self.font, 450, y2)
        utils.talk_dialog(self.screen, ["(8)"], self.font, 640, y2)
        # ----
        utils.talk_dialog(self.screen, self.display_text, self.font, 20, 500, line_length=60)
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        # loop_counter = 0
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
            # self.keep_looping = False
            # ----
            # loop_counter += 1
            # if loop_counter > 50:
            #     self.keep_looping = False
        return self.message

# ------------------------------------------------------------
#                    class TextDialog
# ------------------------------------------------------------

class DialogText:
    def __init__(self, text_list, height=400, width=600, line_width=50):
        self.display_list = text_list
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

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
                    # added sept 26, 2021
                    self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=50, line_length=60,
                          color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.player.debug_print()
        # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
        # self.save_data()
        return self.message

# ------------------------------------------------------------
#                    class DialogDisplayItem
# ------------------------------------------------------------
class DialogDisplayItem:
    def __init__(self, merchant_inventory, item_name):
        self.init_pygame()
        self.merchant_inventory = merchant_inventory
        self.item_name = item_name
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False

    def draw(self):
        # self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        mylist = []
        the_item = self.merchant_inventory.get_item_by_name(self.item_name)
        if the_item is None:
            t = self.merchant_inventory.display_string()
            print(t)
            s = "item: {} was not found in the inventory.".format(self.item_name.upper())
            raise ValueError(s)
        display_object = the_item.display_string()
        utils.talk_dialog(self.screen, display_object, self.font, width_offset=20, height_offset=25, line_length=60,
                          color=constants.BLACK)
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=650, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        # self.all_sprites.update()
        # self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        while self.keep_looping == True:
            self.handle_events()
            self.draw()

# ------------------------------------------------------------
#                    class DialogPlayerInfo
# ------------------------------------------------------------

class DialogPlayerInfo:
    def __init__(self, player, line_width=50):
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.user_text = ""
        self.text_color = constants.BLACK
        # --------------------------------------
        # mylist = []
        # mylist.append("{} the {}".format(self.player.name, self.player.profession))
        # mylist.append("name | hps ")
        # mylist.append(" ")
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        # a_constant = 4
        # self.player.resize(constants.TILESIZE * a_constant, 0, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                    # if not utils.is_int(self.user_text):
                    #     raise ValueError("Error!")
                    # myint = int(self.user_text)
                    # if not myint in self.number_range:
                    #     self.user_text = ""
                    # else:
                    #     mytext = self.npc_goods[myint - 1][1]
                    #     consumable_name = mytext.split(": ")
                    #     consumable_name = consumable_name[0].lower().strip()
                    #     mydialog = DialogDisplayConsumable(self.player, consumable_name)
                    #     mydialog.main()
                    #     self.init_pygame()
                    #     self.user_text = ""
                else:
                    self.user_text += event.unicode

    # def _draw_user_input_window(self):
    #     left = self.width - int(self.width / 1.05)
    #     top = self.height - 90
    #     # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
    #     pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
    #     # ----
    #     surface = self.font.render(self.user_text, True, self.text_color)
    #     user_response_width, user_response_height = self.font.size(self.user_text)
    #     mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
    #     self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        # self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        # self._draw_user_input_window()
        # -----------------------------------------
        # mylist = []
        # mylist.append("{} the {} | {}".format(self.player.name, self.player.kind, self.player.profession))
        # # self.player.debug_print()
        # mylist.append(" ")
        # # mylist.append("{}".format(self.merchant.inventory.display_string()))
        mylist = []
        mylist.append("{} the {}".format(self.player.name.upper(), self.player.profession.upper()))
        mylist.append(" ")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=25, line_length=60,
                          color=constants.BLACK)

        utils.talk_dialog(self.screen, self.player.display_list(), self.font, width_offset=20, height_offset=125, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = self.player.inventory.display_string()
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # # [print(i) for i in mylist]
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # mylist.append("gold: {}".format(self.player.gold))
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=300, line_length=60,
        #                   color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=650, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        # return self.return_value

# ------------------------------------------------------------
#                    class DialogConversation
# ------------------------------------------------------------

# class DialogConversation:
#     def __init__(self, player_name, npc_name, zone_name, map_name, player_gold,
#                  list_of_possible_responses, line_width=50):
#         self.player_name = player_name
#         self.npc_name = npc_name
#         self.zone_name = zone_name
#         self.map_name = map_name
#         self.player_gold = player_gold
#         # ----
#         self.display_list = []
#         self.choices = list_of_possible_responses
#         self.width = constants.SCREEN_WIDTH
#         self.height = constants.SCREEN_HEIGHT
#         self.line_width = line_width
#         # --------------------------------------
#         self.init_pygame()
#         self.all_sprites = pygame.sprite.Group()
#         # --------------------------------------
#         self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
#         self.input_text_color = constants.ORANGE
#         self.text_background_color = constants.LIGHTGREY
#         # --------------------------------------
#         self.text = ""
#         self.user_text = ""
#         self.big_window_background_color = constants.WHITE
#         self.user_text_rect_background_color = constants.WHITE
#         self.text_color = constants.BLACK
#         self._initialize_rectangles()
#         # --------------------------------------
#         self.message = ""
#         self.keep_looping = True
#         # --------------------------------------
#         # self.player_inventory = Inventory(player_name=player_name,
#         #                                   npc_name= npc_name,
#         #                                   character_type="player")
#         # self.npc_inventory = Inventory(player_name=player_name,
#         #                                npc_name=npc_name,
#         #                                character_type="npc")
#         self.current_card_index = 0
#         self.current_card = None
#         # --------------------------------------
#
#
#     def init_pygame(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption("{}".format(constants.TITLE))
#         self.clock = pygame.time.Clock()
#         self.BG_COLOR = constants.WHITE
#         self.font = pygame.font.Font(None, 35)
#
#     def _initialize_rectangles(self):
#         long_thin_rectangle_width = self.width - 20
#         long_thin_rectangle_height = 45
#         top = 10
#         left = 330 + 375
#         self.user_rect = pygame.Rect(10,
#                                      left,
#                                      long_thin_rectangle_width,
#                                      long_thin_rectangle_height)
#
#     def handle_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.keep_looping = False
#             elif event.type == pygame.KEYDOWN:
#                 self.text_background_color = constants.LIGHTGREY
#                 if event.key == pygame.K_ESCAPE:
#                     self.keep_looping = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     self.user_text = self.user_text[:-1]
#                 elif event.key == pygame.K_RETURN:
#                     self.text = self.user_text.lower().strip()
#                     if not self.text in self.choices:
#                         self.text_background_color = constants.RED
#                         self.user_text = ""
#                         return False
#                     self.keep_looping = False
#                     self.message = self.text
#                 else:
#                     self.user_text += event.unicode
#
#     def _position_input_text(self):
#         # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
#         pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
#         # ----
#         surface = self.font.render(self.user_text, True, self.text_color)
#         user_response_width, user_response_height = self.font.size(self.user_text)
#         left = 14
#         top = 337
#         mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
#         self.screen.blit(surface, mytext_rect)
#
#     def draw(self):
#         # -----------------------------------------
#         self.screen.fill(self.BG_COLOR)
#         # -----------------------------------------
#         utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
#                           height_offset=50, line_length=60,
#                           color=constants.BLACK)
#         # ----
#         # mylist = []
#         # mylist.append("1 = Reload Player")
#         # mylist.append("Q = Exit")
#         # mylist.append("ESC = Exit")
#         # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=200, line_length=60,
#         #                   color=constants.BLACK)
#         # -----------------------------------------
#         self._position_input_text()
#         # -----------------------------------------
#         pygame.display.flip()
#
#     def main(self):
#         self.clock.tick(constants.FRAME_RATE)
#         # self.window_text_list = self.separate_text_into_lines(
#         #     text, self.line_width)
#         while self.keep_looping:
#             self.handle_events()
#             self.draw()
#         # self.player.debug_print()
#         # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
#         # self.save_data()
#         return self.message
# ------------------------------------------------------------
#                    class DialogGetFreeformText
# ------------------------------------------------------------
class DialogGetFreeformText:
    def __init__(self, text_list, max_text_length, line_width=50):
        self.display_list = text_list
        if utils.is_int(max_text_length) == False:
            raise ValueError("Error")
        self.max_text_length = int(max_text_length)
        # ----
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(10,
                                     700,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

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
                    self.text = self.user_text.lower().strip()
                    if len(self.text) > self.max_text_length:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    elif self.text.find(" ") >= 0:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    if utils.is_alpha(self.text) == False:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    if utils.validate_player_name(self.text) == True:
                        # Check to make sure that this isn't the name of another character.
                        # If this code is execulted then this name is a duplicate.
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.keep_looping = False
                    self.message = self.text
                else:
                    self.user_text += event.unicode

    def _position_input_text(self):
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
        # ----
        # surface = self.font.render(self.user_text, True, self.text_color)
        # user_response_width, user_response_height = self.font.size(self.user_text)
        # left = 14
        # top = 337
        # mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        # self.screen.blit(surface, mytext_rect)

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=20, line_length=60,
                          color=constants.BLACK)

        # -----------------------------------------
        self._position_input_text()
        # -----------------------------------------

        utils.talk_dialog(self.screen, self.user_text, self.font, width_offset=20,
                          height_offset=700, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = []
        # mylist.append("1 = Reload Player")
        # mylist.append("Q = Exit")
        # mylist.append("ESC = Exit")
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=200, line_length=60,
        #                   color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.player.debug_print()
        # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
        # self.save_data()
        return self.message
# ------------------------------------------------------------
#                    class DialogInput2
# ------------------------------------------------------------
class DialogInput2:
    def __init__(self, text_list, list_of_possible_responses, line_width=50):
        self.display_list = text_list
        self.choices = list_of_possible_responses
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(10,
                                     700,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

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
                    self.text = self.user_text.lower().strip()
                    if not self.text in self.choices:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.keep_looping = False
                    self.message = self.text
                else:
                    self.user_text += event.unicode

    def _position_input_text(self):
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
        # ----
        # surface = self.font.render(self.user_text, True, self.text_color)
        # user_response_width, user_response_height = self.font.size(self.user_text)
        # left = 14
        # top = 337
        # mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        # self.screen.blit(surface, mytext_rect)

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=20, line_length=60,
                          color=constants.BLACK)

        # -----------------------------------------
        self._position_input_text()
        # -----------------------------------------

        utils.talk_dialog(self.screen, self.user_text, self.font, width_offset=20,
                          height_offset=700, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = []
        # mylist.append("1 = Reload Player")
        # mylist.append("Q = Exit")
        # mylist.append("ESC = Exit")
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=200, line_length=60,
        #                   color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.player.debug_print()
        # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
        # self.save_data()
        return self.message
# ------------------------------------------------------------
#                    class DialogInput
# ------------------------------------------------------------

class DialogInput:
    def __init__(self, text_list, list_of_possible_responses, height=400, width=600, line_width=50):
        self.display_list = text_list
        self.choices = list_of_possible_responses
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(10,
                                     330,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

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
                    self.text = self.user_text.lower().strip()
                    if not self.text in self.choices:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.keep_looping = False
                    self.message = self.text
                else:
                    self.user_text += event.unicode

    def _position_input_text(self):
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = 14
        top = 337
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=50, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = []
        # mylist.append("1 = Reload Player")
        # mylist.append("Q = Exit")
        # mylist.append("ESC = Exit")
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=200, line_length=60,
        #                   color=constants.BLACK)
        # -----------------------------------------
        self._position_input_text()
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.player.debug_print()
        # print("akdf;aksjdf;kajsdfkjas;dfkja;sdlkfja;lsdkjf;lksdjflkdjf")
        # self.save_data()
        return self.message

# ------------------------------------------------------------
#                    class DialogZoneInfo
# ------------------------------------------------------------
class DialogZoneInfo:
    def __init__(self, player_name, player_zone, player_map, height=900, width=500, line_width=50):
        self.width = height
        self.height = height
        self.player_name = player_name
        self.player_zone = player_zone
        self.player_map = player_map
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.user_text = ""
        self.display_list = []
        self.text_color = constants.BLACK
        # --------------------------------------
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        a_constant = 4
        # self.player.resize(constants.TILESIZE * a_constant, 0, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def read_data(self, zone_name, map_name):
        mylist = []
        mylist.append("character_name (from player): {}".format(self.player_name))
        mylist.append("zone_name: {}".format(zone_name))
        mylist.append("map_name: {}".format(map_name))
        mylist.append("------------")
        mylist.append("From file:")
        mydict = utils.get_user_data()
        mylist.append("character_name: {}".format(mydict["character_name"]))
        mylist.append("zone_name: {}".format(mydict["zone_name"]))
        mylist.append("map_name: {}".format(mydict["map_name"]))
        mylist.append("------------")
        mylist.append("From Player:")
        mylist.append("zone_name: {}".format(self.player_zone))
        mylist.append("map_name: {}".format(self.player_map))
        self.display_list = mylist

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if not utils.is_int(self.user_text):
                        raise ValueError("Error!")
                    myint = int(self.user_text)
                    if not myint in self.number_range:
                        self.user_text = ""
                    else:
                        mytext = self.npc_goods[myint - 1][1]
                        consumable_name = mytext.split(": ")
                        consumable_name = consumable_name[0].lower().strip()
                        mydialog = DialogDisplayConsumable(self.player, consumable_name)
                        mydialog.main()
                        self.init_pygame()
                        self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top + 45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        # mylist = []
        # mylist.append("{} the {} | {}".format(self.player.name, self.player.kind, self.player.profession))
        # # self.player.debug_print()
        # mylist.append(" ")
        # # mylist.append("{}".format(self.merchant.inventory.display_string()))
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20, height_offset=275,
                          line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = self.player.inventory.display_string()
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # # [print(i) for i in mylist]
        # # print("&&&&&&&&&&&&&&&&&&&&&&")
        # mylist.append("gold: {}".format(self.player.gold))
        # utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=300, line_length=60,
        #                   color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

        # def save_data(self):
        #     # self.player.debug_print()
        #     self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        # return self.return_value

# ------------------------------------------------------------
#                    class DialogReset
# ------------------------------------------------------------

class DialogSpashScreen:
    def __init__(self, height=400, line_width=50):
        # self.height = height
        # self.width = height
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # ----
        self.init_pygame()
        # ----
        self.keep_looping = True
        # ----
        self.all_sprites = pygame.sprite.Group()
        filepath = utils.get_filepath("splash_screen_square.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.image = pygame.transform.scale(self.image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.my_picture = MySprite("splash_screen_square.png", 0, 0)
        # self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.GREEN
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.user_text_rect_background_color = constants.WHITE
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites.add(self.my_picture)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        loop_counter = 0
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
            # self.keep_looping = False
            # ----
            loop_counter += 1
            if loop_counter > 50:
                self.keep_looping = False

# ------------------------------------------------------------
#                    class DialogGoodbye
# ------------------------------------------------------------

class DialogGoodbye:
    def __init__(self, height=400, line_width=50):
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.line_width = line_width
        # ----
        self.init_pygame()
        # ----
        self.keep_looping = True
        # ----
        self.all_sprites = pygame.sprite.Group()
        filepath = utils.get_filepath("goodbye_splash_screen.png")
        self.image = pygame.image.load(filepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (constants.TILESIZE, constants.TILESIZE))
        self.image = pygame.transform.scale(self.image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.my_picture = MySprite(image_filename="splash_screen_square.png", x=0, y=0)
        # self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.GREEN
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.user_text_rect_background_color = constants.WHITE
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.all_sprites.add(self.my_picture)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    def main(self):
        loop_counter = 0
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
            # self.keep_looping = False
            # ----
            loop_counter += 1
            if loop_counter > 50:
                self.keep_looping = False


# ------------------------------------------------------------
#                    class DialogSelectPlayer
# ------------------------------------------------------------

class DialogSelectPlayer:
    def __init__(self, height=400, line_width=50):
        self.height = height
        self.line_width = line_width
        # ---------------------------
        pygame.init()
        self.keep_looping = True
        # ---------------------------
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)
        text_width, _ = self.font.size("a")
        self.width = self.line_width * text_width
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ---------------------------
        self.user_text = ""
        self.window_text_list = []
        self.keep_looping = True
        self.mouse_pos = None
        self.mouse_pressed = None
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # ---------------------------
        self._initialize_rectangles()
        # ---------------------------
        self.chosen_name = ""

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.user_text_rect_background_color = constants.WHITE
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.chosen_name = self.user_text.lower().strip()
                    self.user_text = ""
                    if not utils.validate_name(self.chosen_name) == True:
                        self.user_text_rect_background_color = constants.RED
                    else:
                        self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.window_text_list, self.font, width_offset=14, height_offset=0)

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        filepath = os.path.join("data", "playing_characters")
        self.window_text_list = utils.get_subdirectories(filepath)
        self.window_text_list.insert(0, " ")
        self.window_text_list.insert(0, "Which character would you like to select?")
        # ----
        self.user_text = ""
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.events()
            self.draw()
        return self.chosen_name

# ------------------------------------------------------------
#                    class DialogCreatePlayer
# ------------------------------------------------------------
class DialogCreatePlayer:
    def __init__(self):
        self.player_name = ""

    def main(self):
        mydialog = InputDialog(["What would you like the name of your character to be?"])
        player_name = mydialog.main().lower().strip()
        print("player_name: {}".format(player_name))
        destination = os.path.join("data", "playing_characters", player_name)
        os.mkdir(destination)
        # ----
        raise NotImplemented
        source = os.path.join("data", "master_files", "player_types", "warrior")
        utils.copy_directory(source, destination)

# ------------------------------------------------------------
#                    class DialogMerchant
# ------------------------------------------------------------

class DialogPlayerData:
    def __init__(self, player, height=900, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # --------------------------------------
        # <Player Name> the <Species>
        # --------------------------------------
        self.display_list = []
        self.display_list.append("{} the {}".format(self.player.name, self.player.kind))
        self.display_list.append(" ")
        self.display_list += self.player.display_list()
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        a_constant = 4
        self.player.resize(constants.TILESIZE * a_constant, 0, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20, height_offset=275, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()

# ------------------------------------------------------------
#               class DialogDisplayConsumable
# ------------------------------------------------------------

class DialogDisplayConsumable:
    def __init__(self, player, consumable_name, height=400, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.consumable_name = consumable_name
        self.consumable = self.player.inventory.get_item_by_name(consumable_name)
        # self.consumable.debug_print()
        # raise NotImplemented
        # --------------------------------------
        # title, length = utils.format_string("debugging in DialogPlayerInventory.__init__")
        # print(title)
        # self.player.inventory.debug_print()
        # print("-" * length)
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # self._initialize_rectangles()
        # --------------------------------------
        mylist = []
        mylist.append("{} the {}".format(self.player.name, self.player.kind))
        mylist.append(" ")
        # mylist = mylist + self.merchant.inventory.display_string()
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        # self.mouse_pos = None
        self.keep_looping = True
        # self.message = ""
        self.return_value = []
        # --------------------------------------
        a_constant = 4
        # self.player.resize(constants.TILESIZE * a_constant, 0, 0)
        # self.merchant.resize(constants.TILESIZE * a_constant, constants.NUMBER_OF_BLOCKS_WIDE - a_constant - 1, 0)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def process_text(self, myint):
        pass
        # print("this_good: {}".format(this_good))
        # raise NotImplemented

        # if not self.text in constants.COMMANDS:
        #     raise ValueError("Error")
        # if self.text == "rpi":
        #     pass
        # elif self.text == "rp":
        #     pass
        # else:
        #     raise ValueError("Error")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False
                    # if not utils.is_int(self.user_text):
                    #     raise ValueError("Error!")
                    # myint = int(self.user_text)
                    # if not myint in self.number_range:
                    #     self.user_text = ""
                    # else:
                    #     self.text = self.user_text
                    #     # self.process_text(myint)
                    #     self.return_value = self.npc_goods[myint - 1]
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top + 45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    # def update_classes(self):
    #     self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        # self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.consumable.get_list(), self.font, width_offset=20, height_offset=50,
                          line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.save_data()
        # return self.text
        return self.return_value

# ------------------------------------------------------------
#                    class DialogLobby
# ------------------------------------------------------------

class DialogLobby:
    """
    This dialog starts up at the very beginning.
    Will let the programmer reload the player from scratch, etc.
    Later I would like to have commands that allow the programmer to
    change practically any stat, change any inventory item, give the player
    more gold, and so on.
    """
    def __init__(self, choices, height=500, width=750, line_width=50):
        self.choices = choices
        self.line_width = line_width
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        # ---------------------------
        self.mytextlist = ["Welcome to {}!".format(constants.TITLE)]
        self.mytextlist.append(" ")
        self.mytextlist.append("To play the game, press 'g'.")
        self.mytextlist.append("(disabled) To debug the game, press 'b'.")
        self.mytextlist.append("(disabled) To select a character, press 's'.")
        self.mytextlist.append("To create a player, press 'p'.")
        self.mytextlist.append("(disabled) To alter your playing character, press 'c'.")
        self.mytextlist.append("To access utilities panel, press 'u'.")
        self.mytextlist.append("To quit, press 'q'.")
        # ---------------------------
        self.init_pygame()
        # ---------------------------
        self.user_text = ""
        self.keep_looping = True
        self.return_message = ""
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.LIGHTGREY
        self.text_color = constants.BLACK
        # ---------------------------
        self._initialize_rectangles()

    def init_pygame(self):
        pygame.init()
        # self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        # print("width: {}, height: {}".format(self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    def _set_new_player_name(self):
        def input_name():
            max_length = 10
            mylist = []
            mylist.append("Enter your character's name, below:")
            mylist.append(" ")
            mylist.append("Your character's name:")
            mylist.append(" ")
            mylist.append("- must not be more than 10 characters long")
            mylist.append("- must not have any sapces in it.")
            mylist.append("- must only contain letters (a, b, ..., z)")
            mydialog = DialogGetFreeformText(mylist, max_length)
            return mydialog.main()
        # ----
        user_info = utils.get_user_data()
        zone_name = user_info["zone_name"]
        map_name = user_info["map_name"]
        profession = user_info["profession_name"]
        # ----
        user_input = ""
        a_name = ""
        while not user_input in ["y", "yes"]:
            a_name = input_name()
            mychoices = ["yes", "no", "y", "n"]
            mytext = "Accept this name: {}?".format(a_name)
            ask_player = DialogInput2(mytext, mychoices)
            user_input = ask_player.main()
        # ----
        mypath = os.path.join("data", "playing_characters", a_name)
        os.mkdir(mypath)
        # ----
        if not profession in ["warrior"]:
            s = "Error! At the moment, only the warrior class has been implemented."
            raise ValueError(s)
        # ----
        utils.set_user_data(char_name=a_name,
                            zone_name=zone_name,
                            map_name=map_name,
                            profession_name=profession)
        basepath = os.path.join("data", "master_files", "player_types", "warrior")
        destination_directory = os.path.join("data", "playing_characters", a_name)
        utils.copy_directory(basepath, destination_directory)

    def _set_new_player_model(self):
        mydialog = DialogPlayerModels()
        model_chosen = mydialog.main()
        if model_chosen is None:
            raise ValueError("Error")
        print(model_chosen)
        # ----
        user_info = utils.get_user_data()
        filepath = os.path.join("data", "playing_characters", user_info["character_name"], "player_data_file.txt")
        if os.path.isfile(filepath) == False:
            raise ValueError("Error")
        mydict = utils.read_file(filepath)[0]
        mydict["image_model"] = model_chosen
        # filepath = os.path.join("data", "testing.txt")
        with open(filepath, "w") as f:
            for key, value in mydict.items():
                s = "{}: {}\n".format(key, value)
                f.write(s)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.user_text_rect_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.return_message = "q"
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    mytext = self.user_text.lower().strip()
                    if not mytext in self.choices:
                        self.user_text_rect_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.user_text = ""
                    if mytext == "g":
                        self.keep_looping = False
                        self.return_message = "g"
                    elif mytext == "b":
                        self.keep_looping = False
                        self.return_message = "b"
                    elif mytext == "p":
                        # ----
                        self._set_new_player_name()
                        self._set_new_player_model()
                        # self.init_pygame()
                        return False
                        # mydialog = DialogPlayerCommands()
                        # mydialog.main()
                        # self.keep_looping = False
                        # self.return_message = "c"
                    elif mytext == "c":
                        mytext = "This has been disabled."
                        mylist = ["quit", "q"]
                        # mydialog = DialogInput2(mytext, mylist)
                        return False
                    elif mytext == "u":
                        self.return_message = "u"
                        self.keep_looping = False
                        return False
                    elif mytext == "s":
                        mydialog = TextDialog("Player selection has been temporarily disabled.")
                        mydialog.main()
                        self.init_pygame()
                        self.return_message = "s"
                        return False
                        # mydialog = DialogSelectPlayer()
                        # user_choice = mydialog.main()
                        # # ----
                        # utils.set_user_data(user_choice)
                        # # ----
                        # self.return_message = "s"
                        # self.keep_looping = False
                    elif mytext == "q" or mytext == "quit":
                        self.keep_looping = False
                        self.return_message = "q"
                    else:
                        raise ValueError("Error!")
                else:
                    self.user_text += event.unicode

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.mytextlist, self.font, width_offset=12, height_offset=12, line_length=50)

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        utils.talk_dialog(self.screen, [self.user_text], self.font, width_offset=14, height_offset=670)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.events()
            self.draw()
        if not self.return_message in self.choices:
            raise ValueError("Error! This was entered: {}".format(self.return_message))
        return self.return_message

# ------------------------------------------------------------
#                    class DialogPlayerCommands
# ------------------------------------------------------------

class DialogPlayerCommands:
    """
    This is going to be useful mainly for debugging. It lets the player
    change practically any stat, change their inventory, gives themselves
    more gold, and so on.
    """
    def __init__(self, height=700, line_width=50):
        # self.possible_responses = possible_responses
        self.height = height
        self.width = 750
        self.line_width = line_width
        # ---------------------------
        self.init_pygame()
        # ---------------------------
        # pygame.init()
        self.keep_looping = True
        self.text_background_color = constants.LIGHTGREY
        # ---------------------------
        # self.clock = pygame.time.Clock()
        # self.font = pygame.font.SysFont('Comic Sans', 30)
        # myfont = pygame.font.SysFont('Comic Sans MS', 30)
        # text_width, _ = self.font.size("a")
        # self.width = self.line_width * text_width
        # self.screen = pygame.display.set_mode((self.width, self.height))
        # ---------------------------
        self.user_text = ""
        self.window_text_list = []
        self.keep_looping = True
        self.mouse_pos = None
        self.mouse_pressed = None
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # ---------------------------
        self.mytextlist = []
        filepath = os.path.join("data", constants.PLAYER_COMMANDS)
        with open(filepath, "r") as f:
            self.mytextlist = f.readlines()
            self.mytextlist = [i.strip() for i in self.mytextlist if len(i.strip()) > 0]
        # ---------------------------
        self._initialize_rectangles()

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    # def separate_text_into_lines(self, mytext, line_length):
    #     mylist = []
    #     while len(mytext) >= line_length:
    #         myint = mytext[0:line_length].rfind(" ")
    #         mylist.append(mytext[0:myint].strip())
    #         mytext = mytext[myint:].strip()
    #     mylist.append(mytext)
    #     return mylist

    def events(self):
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
                    mytext = self.user_text.lower().strip()
                    if mytext == "rp":
                        print("Resetting player")
                        user_data = utils.get_user_data()
                        utils.copy_original_player_files(user_data["profession"], user_data["character_name"])
                        self.keep_looping = False
                    elif mytext == "rpi":
                        print("Resetting player's inventory files")
                        utils.copy_original_player_inventory_files()
                        self.keep_looping = False
                    elif mytext == "rm": # reset monsters
                        print("Resetting monsters")
                        utils.copy_original_monster_files()
                        self.keep_looping = False
                    elif mytext == "ra":
                        print("Resetting all (player and monsters)")
                        utils.copy_original_player_files() # player
                        utils.copy_original_monster_files() # monsters
                        self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.mytextlist, self.font, width_offset=15, height_offset=12, line_length=40)
        # # -----------------------------
        # # ---- Draw text in big window
        # for count, elem in enumerate(self.window_text_list):
        #     text_width, text_height = self.font.size(elem)
        #     surface = self.font.render(elem, True, (0, 0, 0))
        #     # ----------------------
        #     left = 20
        #     top = (text_height * count) + 20
        #     self.screen.blit(surface, (left, top))

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        self.user_text = ""
        self.clock.tick(20)
        while self.keep_looping:
            self.events()
            self.draw()
        return self.user_text

# ------------------------------------------------------------
#                    class InputDialog
# ------------------------------------------------------------

class InputDialog:
    def __init__(self, list_of_text, height=400, line_width=50):
        if type(list_of_text) != type([]):
            raise ValueError("Error!")
        self.height = height
        self.line_width = line_width
        # ---------------------------
        pygame.init()
        self.keep_looping = True
        # ---------------------------
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)
        text_width, _ = self.font.size("a")
        self.width = self.line_width * text_width
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ---------------------------
        self.user_text = ""
        self.window_text_list = list_of_text
        self.keep_looping = True
        self.mouse_pos = None
        self.mouse_pressed = None
        # ---------------------------
        self.BG_COLOR = constants.BLACK
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        # ---------------------------
        self._initialize_rectangles()

    # def separate_text_into_lines(self, mytext, line_length):
    #     mylist = []
    #     while len(mytext) >= line_length:
    #         myint = mytext[0:line_length].rfind(" ")
    #         mylist.append(mytext[0:myint].strip())
    #         mytext = mytext[myint:].strip()
    #     mylist.append(mytext)
    #     return mylist

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.window_background_rect = pygame.Rect(top_rectangle_left,
                                                  top_rectangle_top,
                                                  top_rectangle_width,
                                                  top_rectangle_height)
        # ----------------------
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 100
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        # ----------------------

    def _draw_big_window(self):
        pygame.draw.rect(self.screen, self.big_window_background_color, self.window_background_rect)
        utils.talk_dialog(self.screen, self.window_text_list, self.font, width_offset=14, height_offset=0)
        # -----------------------------
        # ---- Draw text in big window
        # for count, elem in enumerate(self.window_text_list):
        #     text_width, text_height = self.font.size(elem)
        #     surface = self.font.render(elem, True, (0, 0, 0))
        #     # ----------------------
        #     left = 20
        #     top = (text_height * count) + 20
        #     self.screen.blit(surface, (left, top))

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        mytext_rect = pygame.Rect(left, top, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def main(self):
        self.user_text = ""
        while self.keep_looping:
            self.clock.tick(20)
            self.events()
            self.draw()
        return self.user_text

# ------------------------------------------------------------
#                    class TextDialog
# ------------------------------------------------------------

class TextDialog:
    def __init__(self, text, line_width=50):
        self.BG_COLOR = constants.LIGHTGREY
        self.text_list = []
        if type(text) == type("abc"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            for elem in text:
                temp = utils.separate_text_into_lines(elem, line_length=100)
                for line in temp:
                    self.text_list.append(line)
                # self.text_list.append(temp)
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        if len(self.text_list) > 12:
            s = "Error! Textbox should not contain more than 12 lines."
            raise ValueError(s)
        # -------------------------
        pygame.init()
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        text_width, text_height = self.font.size("a")
        self.width = 50 * text_width
        self.height = 400
        kind = ""
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ----
        self.line_height = -1
        for elem in self.text_list:
            try:
                text_width, text_height = self.font.size(elem)
            except:
                try:
                    text_width, text_height = self.font.size(elem[0])
                except:
                    raise ValueError("Error!")
            if text_height > self.line_height:
                self.line_height = text_height
        # -------------------------
        # ----- Text Window -------
        window_left = 10
        window_top = 10
        window_width = self.width - 20
        window_height = self.height - (20 * 3)
        self.window_rect = pygame.Rect(window_left, window_top, window_width, window_height)
        # --------------------------
        # -------- OK Button -------
        button_width = 60
        button_height = 35
        button_left = int(self.height / 2)
        top = 600 - button_height
        print("width: ", button_width)
        self.okay_rect = pygame.Rect(button_left, top, button_width, button_height)
        # else:
        #     raise ValueError("I don't recognize that: ", kind)
        # -------------------------
        self.mouse_pos = None
        self.keep_looping = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                if event.key == pygame.K_RETURN:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                elif mouse_pressed[2] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def _draw_lines(self):
        # karen
        for count, elem in enumerate(self.text_list):
            try:
                surface = self.font.render(elem, True, (0, 0, 0))
            except:
                try:
                    surface = self.font.render(elem[0], True, (0, 0, 0))
                except:
                    raise ValueError("Error!")
            # ----------------------
            left = 20
            top = (self.line_height * count) + 20
            # ----------------------
            self.screen.blit(surface, (left, top), area=None)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ----------------------
        pygame.draw.rect(self.screen, constants.WHITE, self.window_rect)
        # ----------------------
        pygame.draw.rect(self.screen, constants.PURPLE, self.okay_rect)
        # ----------------------
        self._draw_lines()
        # ---- Render the text used to label the button. ----
        surface = self.font.render("OK", True, constants.BLACK)
        self.screen.blit(surface, self.okay_rect)
        # --------------------------------------------------
        if not self.mouse_pos == None:
            okay_result = self.okay_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            self.mouse_pos = None
            if okay_result == 1:
                self.message = ""
                self.keep_looping = False
        # --------------------------------------------------
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()


# ------------------------------------------------------------
#                    class DialogFight
# ------------------------------------------------------------

class DialogFight:
    """Takes the player and a monster and lets them fight."""
    def __init__(self, player, npc, width=768, height=768):
        if player.is_dead() == True:
            s = "The player ({}) is dead.".format(player.name)
            raise ValueError(s)
        if npc.is_dead() == True:
            s = "The monster ({}) is dead.".format(npc.name)
            raise ValueError(s)
        # ----
        self.width = width
        self.height = height
        self.player = player
        self.npc = npc
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.init_pygame()
        # pygame.init()
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        # self.screen = pygame.display.set_mode((self.width, self.height))
        # pygame.display.set_caption("{}".format(constants.TITLE))
        # self.clock = pygame.time.Clock()
        # self.BG_COLOR = constants.WHITE
        # self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text = ""
        self.input_text_color = constants.ORANGE
        self.npc_damage = -1
        self.player_damage = -1
        # # last_attack is important for drawing and nothing else.
        # self.last_attack = "player"
        # --------------------------------------
        # self.mouse_pos = None
        self.keep_looping = True
        # self.message = ""
        # --------------------------------------
        # multiplier = 4
        # self.player.resize(constants.TILESIZE * multiplier, 0, 0)
        # self.monster.resize(constants.TILESIZE * multiplier, constants.NUMBER_OF_BLOCKS_WIDE-multiplier, 0)
        rpg_filepath = os.path.join("data", "images", "npc_models", npc.model_name, "down.png")
        player_filepath = os.path.join("data", "images", "player_images", player.model_name, player.image_down)
        temp_size = constants.TILESIZE * 3
        self.npc_display = MyImage(rpg_filepath, x=2.3, y=0,
                                   width=temp_size,
                                   height=temp_size)
        self.player_display = MyImage(player_filepath, x=0, y=0,
                                      width=temp_size,
                                      height=temp_size)

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_h:
                    myran = random.randint(0, 99)
                    if myran <= self.player.chance_to_hit:
                        # self.npc_damage = self.player.calculate_damage(self.npc)
                        # self.npc.hit_points -= self.player.calculate_damage(self.npc)
                        self.npc_damage = self.player.calculate_damage(self.npc)
                        self.npc.hit_points -= self.npc_damage
                    else:
                        self.npc_damage = 0
                        # self.npc.hit_points
                    myran = random.randint(0, 99)
                    if myran <= self.npc.chance_to_hit:
                        self.player_damage = self.npc.calculate_damage(self.player)
                        # self.player.hit_points -= self.npc.calculate_damage(self.player)
                        self.player.hit_points -= self.player_damage
                    else:
                        self.player_damage = 0
                    # if self.npc.hit_points <= 0:
                    #     # self.keep_looping = False
                    #     pass
                    # elif self.player.hit_points <= 0:
                    #     # self.keep_looping = False
                    #     pass
                else:
                    pass

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self.all_sprites.add(self.npc_display)
        self.all_sprites.add(self.player_display)
        # -----------------------------------------
        monster_list = []
        monster_list.append("{}:".format(self.npc.name.capitalize()))
        monster_list.append("hp: {}".format(self.npc.hit_points))
        utils.talk_dialog(self.screen, monster_list, self.font, width_offset=475, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        player_list = []
        player_list.append("{}:".format(self.player.player_name))
        player_list.append("hp: {}".format(self.player.hit_points))
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        s, t = "", ""
        damage_list = []
        if self.player_damage > -1:
            s = "The {} does {} points of damage.".format(self.npc.name, self.player_damage)
            damage_list.append(s)
        if self.npc_damage > -1:
            t = "{} does {} points of damage.".format(self.player.name, self.npc_damage)
            damage_list.append(t)
        if self.player.hit_points <= 0:
            damage_list.append("{} is dead!".format(self.player.name))
        if self.npc.hit_points <= 0:
            damage_list.append("{} is dead!".format(self.npc.name))
        utils.talk_dialog(self.screen, damage_list, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=constants.BLACK)
        # if self.npc_damage != -1 or self.player_damage != -1:
        #     raise NotImplemented
        # ----
        mylist = []
        mylist.append("What would you like to do?")
        mylist.append("H = Hit")
        # mylist.append("X = Exit (Exiting will cost 2 hitpoints)")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=650, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.add(self.npc_display)
        self.all_sprites.add(self.player_display)
        # s = "npc.xy: ({},{})".format(self.npc_display.x, self.npc_display.y)
        # t = "player.xy: ({},{})".format(self.player_display.x, self.player_display.y)
        # print(s)
        # print(t)
        # self.player_display.move(dx=0.05, dy=0)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def update(self):
        if self.npc.hit_points <= 0:
            self.keep_looping = False
        elif self.player.hit_points <= 0:
            self.keep_looping = False

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
            self.update()
        print("Data being saved.")
        # self.draw()
        # time.sleep(5)
        self.save_data()
        # self.init_pygame()

    def save_data(self):
        print("this is monster save_data in dialogs: {}".format(self.npc.get_fileline()))
        self.npc.save_data()
        self.player.save_data()

# ------------------------------------------------------------
#                    class DialogMerchant
# ------------------------------------------------------------

class DialogMerchant:
    def __init__(self, player, merchant_inventory, merchant_name, height=700, width=800, line_width=50):
        self.player = player
        # self.player.image = self.player.image_down_health_100
        self.merchant_name = merchant_name
        # ----
        if len(self.player.inventory) == 0:
            raise ValueError("Doh! The player has lost their inventory!")
        self.merchant_inventory = merchant_inventory
        # self.merchant_inventory.image = merchant_sprite
        # self.merchant_inventory.x = 500
        # self.merchant_inventory.y = 1000
        self.line_width = line_width
        self.pygame_init()
        # ----
        # self.respond_to_user_action = False
        # self.program_to_player_text = ""
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.width = width
        self.height = height
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text_color = constants.ORANGE
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        # mylist = []
        # mylist.append("{} the {}".format(self.merchant.name, self.merchant.profession))
        # mylist.append(" ")
        # mylist = mylist + self.merchant.inventory.display_string()
        # self.inventory = inventory
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        # self.merchant_sprite = MySprite("barkeep_female_down.png", 5, 0)
        filepath = utils.get_filepath("barkeep_female_down.png")
        # self.merchant.image = pygame.image.load(filepath).convert_alpha()
        # self.npc_display = MySprite(self.merchant.display_image, x=7.5, y=0)
        # self.npc_display.move(dx=2.4, dy=0)
        # self.player_display = MySprite(self.player.display_image, x=0, y=0)
        a_constant = 4
        # self.player.resize(constants.TILESIZE * a_constant, 0, 0)
        # ----

    def pygame_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def _initialize_rectangles(self):
        """This is the box the user uses to type things in."""
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = constants.SCREEN_HEIGHT - 60
        long_thin_rectangle_width = constants.SCREEN_WIDTH - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def process_order(self):
        raise NotImplemented
        print("This is what the user typed: {}".format(self.text))
        parsed_result = utils.parse_player_purchase(self.text)
        print("This is the parsed result: {}".format(parsed_result))
        # ----
        this_item = self.merchant.inventory.get_item_by_name(parsed_result[1])
        if this_item is None:
            raise ValueError("This shoudln't be happening!")
        if parsed_result[0] == "buy":
            print("parsed_result[2]: {}".format(parsed_result[2]))
            gold_required = this_item.cost * int(parsed_result[2])
            print("This is the gold_required: {}".format(gold_required))
            if type(gold_required) != type(123):
                raise ValueError("Error! This needs to be int: {}, it is of type {}.".format(gold_required, type(gold_required)))
            if (self.player.gold - gold_required) < 0:
                mydialog = TextDialog("Doh! You don't have eough money to buy that!")
                mydialog.main()
            else:
                self.player.gold -= gold_required
                # s = "bought {} items of {} ({}|{}) for {} gold.".format(parsed_result[2], this_item.name, this_item.item_kind, this_item.species, gold_required)
                # print(s)
                for _ in range(parsed_result[2]):
                    print("parsed_result: {}".format(parsed_result))
                    print("Adding {} ...".format(parsed_result[1]))
                    print("This is what is being passed off to inventory.add_item:")
                    print("first argument: {}; second argument: {}; third argument: {}".format(parsed_result[2], parsed_result[1], parsed_result[2]))
                    self.player.inventory.add_item(parsed_result[1])
                    print("Item ({}) added.".format(parsed_result[1]))
                    #karen
                # raise NotImplemented
        elif parsed_result[0] == "sell":
            self.player.gold += this_item.cost * parsed_result[2]
            print("sold {} items of {} for {} gold.".format(parsed_result[2], this_item.name,
                                                            (this_item.cost * parsed_result[2])))
            if self.player.inventory.remove_item_by_name(this_item.name, parsed_result[2]) == False:
                self.text_background_color = constants.RED
        else:
            raise ValueError("Error! Could not understand this: {}".format(parsed_result[0]))
        # ----

    def _examine_item(self, item_name):
        this_item = self.merchant_inventory.get_item_by_name(item_name)
        if this_item is None:
            self.text_background_color = constants.RED
            return False
        mydialog = DialogDisplayItem(self.merchant_inventory, item_name)
        mydialog.main()

    def _buy_item(self, item_name):
        def show_text(mylist):
            mylist.append(" ")
            mylist.append("Press <ESC>")
            mydialog = DialogInput2(text_list=mylist,
                                   list_of_possible_responses=["quit", "exit", "okay"])
            return mydialog.main()
        # ----
        this_item = self.merchant_inventory.get_item_by_name(item_name)
        if this_item is None:
            self.text_background_color = constants.RED
            return False
        # ----
        # does the player have enough money?
        # self.player.gold = 1
        if this_item.core_item == True:
            mylist = ["Sorry! This {} cannot be bought.".format(item_name.upper())]
            show_text(mylist)
        elif self.player.gold < this_item.cost:
            mylist = ["Sorry! You don't have enough gold to buy that item."]
            mylist.append("The item costs {} gold.".format(this_item.cost))
            mylist.append("You have {} gold.".format(self.player.gold))
            show_text(mylist)
        elif self.player.gold >= this_item.cost:
            old_gold = self.player.gold
            self.player.gold -= this_item.cost
            mylist = ["You have bought one {} for {} gold.".format(item_name.upper(), this_item.cost)]
            mylist.append("You had {} gold, now you have {} gold.".format(old_gold, self.player.gold))
            show_text(mylist)
            self.player.inventory.add_item_by_name(item_name, 1)
        else:
            raise ValueError("Error")

    def _sell_item(self, item_name):
        def show_text(mylist):
            mylist.append(" ")
            mylist.append("Press <ESC>")
            mydialog = DialogInput2(text_list=mylist,
                                   list_of_possible_responses=["quit", "exit", "okay"])
            return mydialog.main()
        # ----
        this_item = self.merchant_inventory.get_item_by_name(item_name)
        if this_item is None:
            self.text_background_color = constants.RED
            return False
        # ----
        if this_item.core_item == True:
            mylist = ["Sorry! This {} cannot be sold.".format(item_name.upper())]
            show_text(mylist)
            return True
        player_item = self.player.inventory.get_item_by_name(item_name)
        if player_item is None:
            mylist = ["It looks as though you do not have that item ({}) in your backpack.".format(item_name)]
            show_text(mylist)
        elif player_item.units <= 0:
            mylist = ["It looks as though you DO have that item ({}) in your backpack,".format(item_name)]
            mylist.append("but that you have 0 units of it.")
            show_text(mylist)
        elif player_item.units > 0:
            old_gold = self.player.gold
            mylist = ["You sell one unit of this item: {}".format(item_name.upper())]
            self.player.gold += this_item.cost
            mylist.append("You had {} gold. Now you have {} gold.".format(old_gold, self.player.gold))
            self.player.inventory.remove_item_by_name(item_name, 1)
            show_text(mylist)
        else:
            raise ValueError("Error")

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
                    self.text = self.user_text
                    mylist = self.text.split(' ')
                    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
                    if len(mylist) != 3:
                        self.text_background_color = constants.RED
                        return False
                    # ----
                    command = mylist[0]
                    item_name = "{} {}".format(mylist[1], mylist[2])
                    if not item_name in constants.WEAPON_NAMES + constants.CONSUMABLE_NAMES:
                        self.text_background_color = constants.RED
                        return False
                    # ----
                    if command == "examine":
                        self._examine_item(item_name)
                        self.user_text = ""
                    elif command == "buy":
                        self._buy_item(item_name)
                        self.user_text = ""
                        # if utils.order_valid(self.text):
                        #     self.process_order()
                        #     self.user_text = ""
                    elif command == "sell":
                        self._sell_item(item_name)
                        self.user_text = ""
                    else:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)

    def _display_items(self):
        people_name_height = 10
        my_height = 80
        mylist = self.player.inventory.display_string()
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=my_height, line_length=60,
                          color=constants.BLACK)
        utils.talk_dialog(self.screen, self.merchant_name.upper(), self.font,
                          width_offset=450, height_offset=people_name_height, line_length=60,
                          color=constants.BLACK)
        mylist = self.merchant_inventory.display_string()
        if mylist is None:
            raise ValueError("Error")
        utils.talk_dialog(self.screen, mylist, self.font,
                          width_offset=450, height_offset=my_height, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.user_text, self.font, width_offset=20, height_offset=710, line_length=60,
                          color=constants.BLACK)
        # ----
        player_list = []
        player_list.append("{} the {}".format(self.player.name.upper(), self.player.profession.upper()))
        player_list.append("gold: {}".format(self.player.gold))
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=people_name_height, line_length=60,
                          color=constants.BLACK)

    def draw(self):
        # self.update_classes()
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        self._display_items()
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def save_data(self):
        # self.merchant.save_temp_data()
        self.player.save_data()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        # self.player.debug_print()
        # self.save_data()
        # return self.text

# ------------------------------------------------------------
#                    class DialogPlayerInventory
# ------------------------------------------------------------

class DialogPlayerInventory:
    def __init__(self, player, height=900, width=500, line_width=50):
        self.width = width
        self.height = height
        # --------------------------------------
        self.init_pygame()
        # --------------------------------------
        self.player = player
        self.line_width = line_width
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.user_text = ""
        self.text_color = constants.BLACK
        self.background_colour_of_text_box = constants.LIGHTGREY
        # --------------------------------------
        # mylist = []
        # self.npc_goods = self.player.inventory.display_string()
        # self.npc_goods_display = mylist + utils.format_npc_goods(self.npc_goods)
        # self.number_range = utils.get_number_range(self.npc_goods)
        self.display_player_goods = []
        # --------------------------------------
        self._initialize_rectangles()
        # --------------------------------------
        self.keep_looping = True
        # --------------------------------------
        gold_item = player.inventory.get_item_by_name("gold coin")
        # --------------------------------------

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.WHITE
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 40)
        # self.font = pygame.font.SysFont(constants.FONT_NAME, constants.FONT_SIZE)

    def display_text(self):
        # ----
        mylist = []
        mylist.append("{} the {}".format(self.player.name, self.player.profession))
        mylist.append("index | name | (cost) | hps | #")
        mylist.append("HPs: {}, Map: {}".format(self.player.hit_points, self.player.map_name))
        mylist.append(" ")
        return mylist

    def _initialize_rectangles(self):
        long_thin_rectangle_left = 10
        long_thin_rectangle_top = self.height - 60
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        self.user_rect = pygame.Rect(long_thin_rectangle_left,
                                     long_thin_rectangle_top,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def _display_accepted_quests(self):
        from NEW_inventory import SearchMasterQuests
        myobject = SearchMasterQuests()
        return myobject.get_all_accepted_quests_by_name()

    def handle_events(self):
        def is_wrong(text=""):
            self.background_colour_of_text_box = constants.RED
            if len(text) == 0:
                self.user_text = ""
            else:
                self.user_text = text
            return False
        # ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.background_colour_of_text_box = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.user_text is None: raise ValueError("Error")
                    if len(self.user_text) == 0:
                        # Changed Sept 26, 2021
                        # raise ValueError("Error")
                        self.keep_looping = False
                        # self.background_colour_of_text_box = constants.LIGHTGREY
                        return ""
                    if utils.is_int(self.user_text): raise ValueError("Error!")
                    # ----
                    mylist = self.user_text.split((" "))
                    mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
                    if not len(mylist) in [3, 4]:
                        return is_wrong()
                    if not mylist[0] in ["drink", "eat", "add", "remove", "load", "read", "sell"]:
                        # 'add' and 'remove' are for debugging ONLY!!!!
                        return is_wrong()
                    # ----
                    try:
                        number_of_items = int(mylist[3])
                    except:
                        number_of_items = 1
                    # ----
                    command = mylist[0]
                    item_name = "{} {}".format(mylist[1], mylist[2])
                    # ---- ---- ---- ----
                    if command in ["eat", "drink"]:
                        an_item = self.player.inventory.get_item_by_name(item_name)
                        if an_item is None:
                            raise ValueError("Error")
                        self.player.hit_points += an_item.hp * number_of_items
                        if self.player.hit_points > self.player.max_hit_points:
                            self.player.hit_points = self.player.max_hit_points
                        if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                            return is_wrong()
                        # ----
                        npc_goods = self.player.inventory.display_string()
                        self.npc_goods_display = utils.format_npc_goods(npc_goods)
                    elif command in ["sell"]:
                        an_item = self.player.inventory.get_item_by_name(item_name)
                        if an_item is None: raise ValueError("Error")
                        gold_coin = self.player.inventory.get_item_by_name("gold coin")
                        if gold_coin is None: raise ValueError("Error")
                        gold_gained = an_item.cost * number_of_items
                        gold_coin.units += gold_gained
                        # ----
                        if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                            return is_wrong()
                    elif command in ["add"]:
                        # temp = "{} {}".format(mylist[0], mylist[1])
                        # if temp == "add gold":
                        #     if utils.is_int(mylist[2]) == False:
                        #         raise ValueError("Error")
                        #     self.gold += int(mylist[2])
                        #     self.user_text = ""
                        #     return True
                        # ----
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        if item_name is None:
                            raise ValueError("Error")
                        else:
                            self.player.inventory.add_item_by_name_for_dialog(item_name, number_of_items)
                            npc_goods = self.player.inventory.display_string()
                            self.npc_goods_display = utils.format_npc_goods(npc_goods)
                    elif command in ["remove"]:
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        if item_name is None:
                            raise ValueError("Error")
                        if self.player.inventory.remove_item_by_name_for_dialog(item_name, number_of_items) == False:
                            return is_wrong()
                        npc_goods = self.player.inventory.display_string()
                        self.npc_goods_display = utils.format_npc_goods(npc_goods)
                    elif command in ["read"]:
                        item_name = "{} {}".format(mylist[1], mylist[2])
                        if not item_name in constants.READABLE_INVENTORY_ITEMS:
                            s = "This does not seem to be a READABLE_INVENTORY_ITEM: {}".format(item_name)
                            return is_wrong(s)
                        this_item = self.player.inventory.get_item_by_name(item_name)
                        if this_item is None:
                            s = "I can't find this item: {}".format(item_name)
                            return is_wrong(s)
                        mydialog = DialogDisplayImage(this_item.filename)
                        mydialog.main()
                        self.init_pygame()
                    elif command in ["load"]:
                        self.npc_goods_display = self._display_accepted_quests()
                    else:
                        return is_wrong()
                    self.user_text = ""
                else:
                    self.user_text += event.unicode

    def _draw_user_input_window(self):
        left = self.width - int(self.width / 1.05)
        top = self.height - 90
        # pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        # pygame.draw.rect(self.screen, constants.LIGHTGREY, self.user_rect)
        pygame.draw.rect(self.screen, self.background_colour_of_text_box, self.user_rect)
        # ----
        surface = self.font.render(self.user_text, True, self.text_color)
        user_response_width, user_response_height = self.font.size(self.user_text)
        mytext_rect = pygame.Rect(left, top+45, user_response_width, user_response_height)
        self.screen.blit(surface, mytext_rect)

    def update_classes(self):
        self.all_sprites.add(self.player)
        # -----------------------------------------

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self._draw_user_input_window()
        # -----------------------------------------
        utils.talk_dialog(self.screen, self.display_text(), self.font, width_offset=20, height_offset=275, line_length=60,
                          color=constants.BLACK)

        self.display_player_goods = self.player.inventory.display_string()
        utils.talk_dialog(self.screen, self.display_player_goods, self.font, width_offset=20, height_offset=400, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("Return = Exit")
        mylist.append("ESC = Exit")
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=750, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        # self.window_text_list = self.separate_text_into_lines(
        #     text, self.line_width)
        while self.keep_looping:
            self.handle_events()
            self.draw()
        self.player.inventory.save_data()
        # self.save_data()
        # return self.text
        # return self.return_value

# ------------------------------------------------------------
#                    class DialogSpeech
# ------------------------------------------------------------

class DialogSpeech:
    def __init__(self, npc_name, line_width=50):
        if type(npc_name) != type("abc"):
            raise ValueError("Error!")
        # ----
        user_data = utils.get_user_data()
        self.zone_name = user_data["zone_name"]
        self.map_name = user_data["map_name"]
        # ----
        self.text_list = []
        self.npc_name = npc_name
        self.line_width = line_width
        # ----
        self.init_pygame()
        # ----
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        # ----
        self.text = ""
        self.window_rect = None
        self.window_speech = None
        self.window_replies = None
        self.keep_looping = True
        self.length_of_conversation = -1
        # ----
        self.conversation = None
        self.index = 1
        self.response_text = ""
        self.draw_response = False
        # ----
        self.message = ""

    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.DARKGREY
        # self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.npc_name)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def read_data(self):
        self.conversation = Speech(self.npc_name)
        self.conversation.read_data()
        # -------------------------
        # ---- Containing Window ----
        window_left = 10
        window_top = 10
        window_width = self.width - 20
        window_height = self.height - (20 * 3)
        self.window_rect = pygame.Rect(window_left, window_top, window_width, window_height)
        # --------------------------
        # ---- Window Speech ----
        # Upper part of the window
        self.window_speech = pygame.Rect(window_left, window_top, window_width, window_height / 2)
        # -----------------------
        # ---- Window Replies ----
        # Player gets to choose a reply
        self.window_replies = pygame.Rect(window_left, window_height / 2 + (window_top * 2), window_width, window_height / 2)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    self.message = "end game"
                elif event.key == pygame.K_RETURN:
                    if self.response_list[1] == "end game":
                        self.message = self.response_list[1]
                        self.keep_looping = False
                    elif self.response_list[1] == "end conversation":
                        self.message = self.response_list[1]
                        self.keep_looping = False
                    elif self.response_list[1] == "continue":
                        self.message = self.response_list[1]
                        pass
                    else:
                        raise ValueError("Error!")
                    self.index += 1
                    if self.index >= self.length_of_conversation:
                        self.message = "continue"
                        self.keep_looping = False
                    self.draw_response = False
                elif event.key == pygame.K_1:
                    self.draw_response = True
                    self.response_list = self.conversation.get_response(self.index, 1)
                elif event.key == pygame.K_2:
                    self.draw_response = True
                    self.response_list = self.conversation.get_response(self.index, 2)
                elif event.key == pygame.K_3:
                    self.draw_response = True
                    self.response_list = self.conversation.get_response(self.index, 3)

    def draw_response_text(self):
        mylist = utils.separate_text_into_lines(self.response_list[0], 50)
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=14, height_offset=10, line_length=55)

    def draw_text(self):
        if self.keep_looping == False: return ""
        self.text_list = utils.separate_text_into_lines(self.conversation.get_prompt(self.index), self.line_width)
        if len(self.text_list) > 12:
            s = "Error! Textbox should not contain more than 12 lines."
            raise ValueError(s)
        # -------------------------
        # self.window_speech = pygame.Rect(window_left, window_top, window_width, window_height / 2)
        utils.talk_dialog(self.screen, self.text_list, self.font, width_offset=14, height_offset=10, line_length=55)
        choices_list = self.conversation.get_choices(self.index)
        top1 = utils.talk_dialog(self.screen, choices_list, self.font, width_offset=14, height_offset=400, line_length=55)
        # print("top1: {}".format(top1))
        # top2 = utils.talk_dialog(self.screen, self.npc.choice2(), self.font, width_offset=14, height_offset=top1+40, line_length=55)
        # print("top2: {}".format(top2))
        # top3 = utils.talk_dialog(self.screen, self.npc.choice3(), self.font, width_offset=14, height_offset=top2+40, line_length=55)
        # print("top3: {}".format(top3))

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # window_rect is the main window
        pygame.draw.rect(self.screen, self.BG_COLOR, self.window_rect)
        # window_speech contains what is said by the npc
        pygame.draw.rect(self.screen, constants.WHITE, self.window_speech)
        # window_replies contains the choices of the player
        pygame.draw.rect(self.screen, constants.WHITE, self.window_replies)
        if self.draw_response == False:
            self.draw_text()
        else:
            self.draw_response_text()
        pygame.display.flip()

    def main(self):
        self.length_of_conversation = len(self.conversation)
        while self.keep_looping:
            self.events()
            self.draw()
        if self.message is None:
            raise ValueError("Error!")
        if len(self.message) == 0:
            raise ValueError("Error")
        return self.message

# ============================================================

def init_pygame():
    pygame.init()
    pygame.display.set_caption("Enter {}".format(constants.TITLE))

def debug_DialogFight():
    player_name = ""
    zone_name = ""
    map_name = ""
    from graphics_fauna import Player
    from child_classes import PredatorNPC
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    mymonsters = Monsters()
    mymonsters.read_data()
    mymonster = mymonsters.get_monster_by_name("Nether")
    # ----
    myplayer.read_data_first()
    mydialog = DialogFight(myplayer, mymonster)
    mydialog.main()

# ************************************************

def test_dialog_player_data():
    from graphics_fauna import Player, Npc
    myplayer = Player()
    myplayer.read_data_first()
    # ----
    name = "alvin"
    x = 4
    y = 4
    mylist = [name, x, y]
    mynpc = Npc(mylist)
    mynpc.read_data()
    # ----
    mydialog = DialogPlayerData(myplayer)
    mydialog.main()
    # mydialog = DialogDisplayConsumable(myplayer, "dry bread")
    # mydialog.main()
    # mydialog.main()
    # ----
    # mydialog = DialogPlayerInventory(myplayer)
    # mydialog.main()

def test_dialog_lobby():
    choices = ["g", "c", "q", "p", "s"]
    mydialog = DialogLobby(choices)
    mydialog.main()

def test_dialog_speech(player_name, zone_name, map_name):
    from graphics_fauna import Player
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    npc_name = "Old Ben"
    mydialog = DialogSpeech(npc_name=npc_name)
    mydialog.read_data()
    result = mydialog.main()
    print("Result: {}".format(result))

def test_dialog_fight_loader():
    player_name = "henry"
    # npc_name = "skeleton_plain"
    # npc_name = "loriintr"
    npc_name = "daith"
    # zone_name = "swindon_pub"
    # zone_name = "green_lawn"
    zone_name = "bridge"
    map_name = "map02"
    profession = "warrior"
    mylist = ["Loading a fight between:"]
    mylist.append("{} the {}. Zone: {}, map: {}".format(player_name, profession, zone_name, map_name))
    mylist.append("and")
    mylist.append("npc_name: {}".format(npc_name))
    mydialog = DialogText(mylist)
    mydialog.main()
    # ----
    _test_dialog_fight(player_name, npc_name, zone_name, map_name, profession="warrior")

def _test_dialog_fight(player_name, npc_name, zone_name, map_name, profession="warrior"):
    from graphics_fauna import Player, Npcs
    utils.copy_original_player_files(profession, player_name)
    # ----
    myplayer = Player(player_name, zone_name, map_name)
    if myplayer is None: raise ValueError("Error")
    myplayer.read_data()
    mynpcs = Npcs(zone_name, map_name)
    mynpcs.read_data()
    mynpc = mynpcs.get_npc_by_name(npc_name)
    if mynpc is None:
        s = "I could not find the npc with the name: {}".format(npc_name)
        raise ValueError(s)
    if mynpc.hit_points <= 0:
        mynpc.hit_points = mynpc.max_hit_points
    # ---- **** ----
    mydialog = DialogFight(myplayer, mynpc)
    mydialog.main()
    # ---- **** ----
    if myplayer.is_dead():
        print("The monster won.")
    elif mynpc.is_dead():
        print("The player won!")
    elif mynpc.is_dead() == False and myplayer.is_dead() == False:
        print("Someone called the fight off.")
    else:
        raise ValueError("Error!")

def test_dialog_input():
    ud = utils.get_user_data()
    name = ud["character_name"]
    prof = ud["profession_name"]
    text_list = ["{} the {} is dead.".format(name.upper(), prof.upper())]
    text_list.append("Reload player?")
    text_list.append(" ")
    text_list.append("(y = Yes; n = No)")
    choices = ["y", "n"]
    mydialog = DialogInput(text_list, choices)
    myresult = mydialog.main()
    print("myresult: {}".format(myresult))

def debug_dialog_player_info():
    player_name = "henry"
    zone_name = "the_orchard"
    map_name = "map01"
    # ----
    from graphics_fauna import Player
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    if myplayer is None:
        raise ValueError("Error")
    mylist = myplayer.display_list()
    print(mylist)
    # ----
    mydialog = DialogPlayerInfo(myplayer)
    mydialog.main()

def test_dialog_player_inventory():
    player_name = "henry"
    zone_name = "green_lawn"
    map_name = "map00"
    # ----
    from graphics_fauna import Player
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    # myplayer.inventory.add_item_by_name("westley note", 1)
    # myitem = myplayer.inventory.get_item_by_name("westley note")
    # if myitem is None: raise ValueError("Error")
    mydialog = DialogPlayerInventory(myplayer)
    mydialog.main()

def test_dialog_display_item():
    from inventory import Inventory
    player_name = "henry"
    npc_name = "matilda"
    char_type = "npc"
    myinventory = Inventory(player_name=player_name,
                            npc_name=npc_name, character_type=char_type)
    myinventory.read_data()
    mydialog = DialogDisplayItem(merchant_inventory=myinventory, item_name="tough jerky")
    mydialog.main()

def test_dialog_merchant():
    player_name = "henry"
    zone_name = "swindon_pub"
    map_name = "map00"
    npc_name = "matilda"
    # ----
    from graphics_fauna import Npcs, Player
    from inventory import Inventory
    mynpcs = Npcs(zone_name, map_name)
    mymerchant = mynpcs.debug_load_NPC(player_name, npc_name, 2, 3)
    # mymerchant.debug_print()
    myplayer = Player(player_name, zone_name, map_name)
    myplayer.read_data()
    # ----
    merchant_inventory = Inventory(player_name, npc_name, character_type="npc")
    merchant_inventory.read_data()
    # ----
    mydialog = DialogMerchant(myplayer, merchant_inventory, merchant_name=npc_name)
    mydialog.main()
    myplayer.save_data()

def test_dialog_use_item_in_inventory():
    from graphics_fauna import Player
    myplayer = Player(player_name="henry",
                      zone_name="swindon_pub",
                      map_name="map00")
    myplayer.read_data()
    mydialog = DialogUseItemInInventory(myplayer)
    # mydialog.read_data()
    mydialog.main()

def test_dialog_list_quests():
    mydialog = DialogShowQuests()
    mydialog.read_data()
    mydialog.main()

if __name__ == "__main__":
    # test_dialog_use_item_in_inventory()
    test_dialog_player_inventory()
    # test_dialog_fight_loader()
    # test_dialog_list_quests()