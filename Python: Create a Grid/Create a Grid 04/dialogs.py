import pygame
import constants
import utils
import sys, os
import random
# ------------------------------------------------------------
#                         class TextDialog
# ------------------------------------------------------------

class TextDialog:
    """This is a dialog that just displays a text message."""
    def __init__(self, text, line_width=50):
        self.BG_COLOR = constants.LIGHTGREY
        self.text_list = []
        if type(text) == type("bla"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            for elem in text:
                temp = utils.separate_text_into_lines(elem, line_length=50)
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
        # print("width: ", button_width)
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
#                    class DialogChoices
# ------------------------------------------------------------

class DialogChoices:
    """Dialog displays a number of choices. The users choice is returned as a strong."""
    def __init__(self, choices):
        self.choices = choices
        # --------------------------------------
        pygame.init()
        self.width = 350
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        s = "{}".format(constants.TITLE)
        pygame.display.set_caption(s)
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.LIGHTGREY
        self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.background_window_rect = pygame.Rect(10, 10, self.width - 20, self.height - 70)
        mylist = ["{}) {}".format(count + 1, i) for count, i in enumerate(self.choices)]
        self.background_window_text = mylist
        self.background_window_color = constants.WHITE
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text = ""
        self.input_text_color = constants.ORANGE
        # # --------------------------------------
        # self.quit_rect = pygame.Rect(10, 150, self.width - 20, 55)
        # self.quit_text = "Quit"
        # self.quit_color = con.LIGHT_PURBLE
        # --------------------------------------
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""

    def process_choice(self):
        if len(self.user_choice) == 0: return False
        if not utils.is_int(self.user_choice): return False
        user_choice = int(self.user_choice)
        if not user_choice in list(range(1, len(self.choices) + 1)): return False
        self.message = self.choices[int(self.user_choice)-1]
        self.user_choice = ""
        self.keep_looping = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.user_choice = self.input_text.lower().strip()
                    self.input_text = ""
                    self.process_choice()
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                print("mouse pressed:", mouse_pressed)
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        pygame.draw.rect(self.screen, constants.WHITE, self.background_window_rect)
        utils.talk_dialog(self.screen, self.background_window_text, self.font, width_offset=20, height_offset=20,
                          line_length=60, color=constants.BLACK)
        # ----
        pygame.draw.rect(self.screen, self.input_text_color, self.input_rect)
        utils.talk_dialog(self.screen, self.input_text, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=con.BLACK)
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        self.clock.tick(20)
        while self.keep_looping:
            self.events()
            self.draw()
        # pygame.quit()
        return self.message

# ------------------------------------------------------------
#                    class InputDialog
# ------------------------------------------------------------

class InputDialog:
    """A users input is solicted and then returend."""
    def __init__(self, height=400, line_width=50):
        self.height = height
        self.line_width = line_width
        # ---------------------------
        pygame.init()
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
        self.BG_COLOR = con.BLACK
        self.big_window_background_color = con.WHITE
        self.user_text_rect_background_color = con.WHITE
        self.text_color = con.BLACK
        # ---------------------------
        self._initialize_rectangles()

    def separate_text_into_lines(self, mytext, line_length):
        mylist = []
        while len(mytext) >= line_length:
            myint = mytext[0:line_length].rfind(" ")
            mylist.append(mytext[0:myint].strip())
            mytext = mytext[myint:].strip()
        mylist.append(mytext)
        return mylist

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
        # -----------------------------
        # ---- Draw text in big window
        for count, elem in enumerate(self.window_text_list):
            text_width, text_height = self.font.size(elem)
            surface = self.font.render(elem, True, (0, 0, 0))
            # ----------------------
            left = 20
            top = (text_height * count) + 20
            self.screen.blit(surface, (left, top))

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

    def main(self, text):
        self.user_text = ""
        self.window_text_list = self.separate_text_into_lines(
            text, self.line_width)
        self.keep_looping = True
        while self.keep_looping:
            self.clock.tick(20)
            self.events()
            self.draw()
        return self.user_text

# ------------------------------------------------------------
#                    class DialogChoices
# ------------------------------------------------------------

class DialogFight:
    """Takes the player and a monster and lets them fight."""
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        # --------------------------------------
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        pygame.init()
        self.width = constants.SCREEN_WIDTH
        self.height = constants.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        s = "{}".format(constants.TITLE)
        pygame.display.set_caption(s)
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.background_window_rect = pygame.Rect(10, 10, self.width - 20, self.height - 70)
        # mylist = ["{}) {}".format(count + 1, i) for count, i in enumerate(self.choices)]
        # self.background_window_text = mylist
        self.background_window_color = constants.WHITE
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        self.input_text = ""
        self.input_text_color = constants.ORANGE
        # --------------------------------------
        # self.display_initial_images()
        # --------------------------------------
        # self.quit_rect = pygame.Rect(10, 150, self.width - 20, 55)
        # self.quit_text = "Quit"
        # self.quit_color = con.LIGHT_PURBLE
        # --------------------------------------
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""
        # --------------------------------------
        multiplier = 4
        self.player.resize(constants.TILESIZE * multiplier, 0, 0)
        self.monster.resize(constants.TILESIZE * multiplier, constants.NUMBER_OF_BLOCKS_WIDE-multiplier, 0)


    # def display_initial_images(self):
    #     # ---------------------------------------------
    #     filepath = os.path.join("data/images", constants.PLAYER_IMG)
    #     self.player_image = pygame.image.load(filepath).convert_alpha()
    #     self.player_image = pygame.transform.scale(self.player_image, (constants.TILESIZE, constants.TILESIZE))
    #     self.rect = self.player_image.get_rect()
    #     self.rect = self.rect.move(self.player.x * constants.TILESIZE, self.player.y * constants.TILESIZE)
    #     # ---------------------------------------------


    def process_choice(self):
        if len(self.user_choice) == 0: return False
        if not utils.is_int(self.user_choice): return False
        user_choice = int(self.user_choice)
        if not user_choice in list(range(1, len(self.choices) + 1)): return False
        self.message = self.choices[int(self.user_choice)-1]
        self.user_choice = ""
        self.keep_looping = False

    # def save_data(self):
    #     self.player.save_data()
    #     self.monster.save_data

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.user_choice = self.input_text.lower().strip()
                    self.input_text = ""
                    self.process_choice()
                elif event.key == pygame.K_h:
                    # print("You just hit h")
                    myran = random.randint(0, 99)
                    if myran <= self.player.chance_to_hit:
                        self.monster.hit_points -= 1
                    myran = random.randint(0, 99)
                    if myran <= self.monster.chance_to_hit:
                        self.player.hit_points -= 1
                    # print("monster hit points: {}".format(self.monster.hit_points))
                    if self.monster.hit_points <= 0:
                        # save player stats to file
                        # save monster stats to file
                        self.message = "monster is dead"
                        self.keep_looping = False
                    elif self.player.hit_points <= 0:
                        self.message = "player is dead"
                        self.keep_looping = False
                else:
                    pass
                    # self.input_text_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                print("mouse pressed:", mouse_pressed)
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    # def update_classes(self):
    #     # for elem in self.grasses:
    #     #     self.all_sprites.add(elem)
    #     # for elem in self.walls:
    #     #     self.all_sprites.add(elem)
    #     # for elem in self.monsters:
    #     #     self.all_sprites.add(elem)
    #     self.all_sprites.add(self.player)
    #     self.all_sprites.add(self.monster)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # -----------------------------------------
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monster)
        # pygame.draw.rect(self.screen, constants.WHITE, self.background_window_rect)
        # utils.talk_dialog(self.screen, self.background_window_text, self.font, width_offset=20, height_offset=20,
        #                   line_length=60, color=con.BLACK)
        # ----
        # pygame.draw.rect(self.screen, self.input_text_color, self.input_rect)
        # -----------------------------------------
        # mylist = []
        monster_list = []
        monster_list.append("{} hit points:".format(self.monster.kind.capitalize()))
        monster_list.append("hp: {}".format(self.monster.hit_points))
        # mylist.append("H = Hit")
        # mylist.append("X = Exit (Exiting will cost 2 hitpoints)")
        # self.input_text = mylist
        utils.talk_dialog(self.screen, monster_list, self.font, width_offset=475, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        # mylist = []
        player_list = []
        player_list.append("Player hit points:")
        player_list.append("hp: {}".format(self.player.hit_points))
        # mylist.append("H = Hit")
        # mylist.append("X = Exit (Exiting will cost 2 hitpoints)")
        # self.input_text = mylist
        utils.talk_dialog(self.screen, player_list, self.font, width_offset=20, height_offset=250, line_length=60,
                          color=constants.BLACK)
        # ----
        mylist = []
        mylist.append("What would you like to do?")
        mylist.append("H = Hit")
        mylist.append("X = Exit (Exiting will cost 2 hitpoints)")
        # self.input_text = mylist
        utils.talk_dialog(self.screen, mylist, self.font, width_offset=20, height_offset=350, line_length=60,
                          color=constants.BLACK)
        # -----------------------------------------
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # -----------------------------------------
        pygame.display.flip()

    def save_data(self):
        self.monster.save_to_temp_file()
        self.player.save_data()

    def main(self):
        self.clock.tick(20)
        while self.keep_looping:
            self.events()
            self.draw()
        # pygame.quit()
        self.save_data()
        return self.message

# ====================================================
# def is_valid(myname):
#     for mychar in myname:
#         if not mychar in con.ALPHABET:
#             return False
#     return True

if __name__ == "__main__":
    from myclasses import Game
    mygame = Game()
    mygame.read_data()
    # mygame.monsters[0].debug_print()
    # raise NotImplemented
    # ----
    text = "Hi!"
    message = ""
    display_dialog = 4
    if display_dialog == 1:
        choices_dialog = DialogChoices([text])
        message = choices_dialog.main().lower().strip()
    elif display_dialog == 2:
        input_dialog = InputDialog()
        message = input_dialog.main(text)
    elif display_dialog == 3:
        text_dialog = TextDialog(text)
        text_dialog.main()
    elif display_dialog == 4:
        fight_dialog = DialogFight(mygame.player, mygame.monsters[0])
        message = fight_dialog.main()
    else:
        raise ValueError("I don't recognize this: {}".format(display_dialog))
    print(message)
