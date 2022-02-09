import pygame
import constants
import utils
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
# ------------------------------------------------------------
#                    class SplashScreen
# ------------------------------------------------------------

class SplashScreen:
    def __init__(self, display_text="", loop_length=10, screen_width=600, screen_height=600):
        # self.width = constants.SCREEN_WIDTH
        # self.height = constants.SCREEN_HEIGHT
        self.width = screen_width
        self.height = screen_height
        self.display_text = display_text
        self.loop_length = loop_length
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.big_window_background_color = constants.WHITE
        # --------------------------------------
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
        offset = int((long_thin_rectangle_height * 1.25))
        self.user_rect = pygame.Rect(10,
                                     self.height - offset,
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
                    self.keep_looping = False
                else:
                    self.user_text += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        utils.talk_dialog(self.screen, self.display_text, self.font, width_offset=10, height_offset=10)
        pygame.display.flip()

    def main(self):
        counter = 0
        while self.keep_looping:
            counter += 1
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
            if counter > self.loop_length:
                self.keep_looping = False
        return

# ------------------------------------------------------------
#                    class DialogInput
# ------------------------------------------------------------
class DialogInput:
    def __init__(self, text_list, list_of_possible_responses,
                 numbered_list=False,
                 show_possible_answers=True,
                 width = 600, height=600, line_width=50):
        if type(text_list) == type("abc"):
            s = "Text as passed in, but this must be a list."
            raise ValueError(s)
        # ----
        if type(list_of_possible_responses) != type([]):
            raise ValueError("Error")
        # ---- ----
        if numbered_list == True:
            self.display_list = text_list
            self.display_list = [i.strip() for i in self.display_list if len(i.strip())>0]
            self.display_list = ["{}) {}".format(count+1, i) for count, i in enumerate(self.display_list)]
        elif numbered_list == False:
            self.display_list = text_list
        self.show_possible_answers = show_possible_answers
        # ----
        if len(list_of_possible_responses) != 0:
            mylist = []
            if numbered_list == False:
                if self.show_possible_answers == True:
                    s = "({})".format(", ".join(list_of_possible_responses))
                    self.display_list.append("")
                    self.display_list.append(s)
                elif self.show_possible_answers == False:
                    pass
                else: raise ValueError("Error")
            elif numbered_list == True:
                for elem in list_of_possible_responses:
                    if utils.is_int(elem) == False:
                        s = "elem: {}".format(elem)
                        raise ValueError(s)
                    mylist.append(str(elem))
                list_of_possible_responses = mylist
            else:
                raise ValueError("Error")
        # ----
        list_of_possible_responses = [str(i) for i in list_of_possible_responses]
        # possible_answers = [str(i) for i in possible_answers]
        # --------------------------------------
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
        self.x = self.user_rect.x + 10
        self.y = self.user_rect.y

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
        offset = int((long_thin_rectangle_height * 1.25))
        self.user_rect = pygame.Rect(10,
                                     self.height - offset,
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
                    if len(self.choices) == 0:
                        self.keep_looping = False
                        return False
                    if not self.text in self.choices:
                        # print("choices:", self.choices)
                        # raise NotImplemented
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.keep_looping = False
                    self.message = self.text
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        if self.keep_looping == True:
            # -----------------------------------------
            utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=20, line_length=60,
                          color=constants.BLACK)
            # -----------------------------------------
            # pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            if len(self.choices) != 0:
                pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
                utils.talk_dialog(self.screen, self.user_text, self.font,
                              width_offset=self.x, height_offset=self.y,
                              line_length=60,
                              color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
        return self.message

# ------------------------------------------------------------
#                    class DialogInput_New
# ------------------------------------------------------------
class DialogInput_New:
    def __init__(self, text_list, list_of_possible_responses,
                 show_possible_answers=True,
                 width = 600, height=600, line_width=50):
        if type(text_list) == type("abc"):
            s = "text_list is of type string, but it neesd to be of type list."
            raise ValueError(s)
        self.display_list = text_list
        # ----
        if type(list_of_possible_responses) != type([]):
            raise ValueError("Error")
        # ---- ----
        if len(list_of_possible_responses) != 0:
            mylist = []
        # ----
        list_of_possible_responses = [str(i) for i in list_of_possible_responses]
        # possible_answers = [str(i) for i in possible_answers]
        # --------------------------------------
        self.choices = list_of_possible_responses
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
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
        self.x = self.user_rect.x + 10
        self.y = self.user_rect.y

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
        offset = int((long_thin_rectangle_height * 1.25))
        self.user_rect = pygame.Rect(10,
                                     self.height - offset,
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
                    if len(self.choices) == 0:
                        self.keep_looping = False
                        return False
                    if not self.text in self.choices:
                        # print("choices:", self.choices)
                        # raise NotImplemented
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.keep_looping = False
                    self.message = self.text
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        if self.keep_looping == True:
            # -----------------------------------------
            utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                          height_offset=20, line_length=60,
                          color=constants.BLACK)
            # -----------------------------------------
            # pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            if len(self.choices) != 0:
                pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
                utils.talk_dialog(self.screen, self.user_text, self.font,
                              width_offset=self.x, height_offset=self.y,
                              line_length=60,
                              color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
        return self.message

# ------------------------------------------------------------
#                    class DialogText
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

if __name__ == "__main__":
    value_list = ["first", "second"]
    text_list = ["{}) {}".format(count+1, i) for count, i in enumerate(value_list)]
    possible_responses = [1, 2]
    mydialog = DialogInput_New(text_list, possible_responses, show_possible_answers=False)
    message = mydialog.main()
    print(message)
    print(value_list[int(message)-1])
    # mydialog = SplashScreen(display_text="Goodbye! :-)", loop_length=40)
    # mydialog.main()
    # text_list = ["How many columns"]
    # text_list.append("are there in this")
    # text_list.append("sprite sheet?")
    # text_list.append(" ")
    # response_list = [str(i) for i in list(range(1, 10+1))]
    # mydialog = DialogInput(text_list=text_list,
    #                        numbered_list=True,
    #                         list_of_possible_responses=response_list,
    #                         screen_width=1000, screen_height=500)
    # message = mydialog.main()
    # print(message)