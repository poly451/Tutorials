import utils
import pygame
import constants
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "1000, 400"

# -------------------------------------------------------------
#                class SimpleSprite
# -------------------------------------------------------------

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, imagepath, width=600, height=600):
        super().__init__()
        self.width = width
        self.height = height
        if os.path.isfile(imagepath) == False:
            a_path = utils.get_filepath02(imagepath)
            if a_path is None:
                s = "I can't find the path for this: {}".format(imagepath)
                raise ValueError(s)
            imagepath = a_path
        # self.tilesize = constants.TILESIZE
        self.image = pygame.image.load(imagepath).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (self.tilesize, self.tilesize))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect = self.rect.move(x * self.width, y * self.height)

# ------------------------------------------------------------
#                    class DialogInput
# ------------------------------------------------------------
class DialogInput:
    def __init__(self, text_list, list_of_possible_responses,
                 show_possible_responses=True,
                 width = 600, height=600, line_width=50):
        self.show_possible_responses = show_possible_responses
        self.display_list = utils.string_to_list(text_list, line_width)
        # ----
        list_of_possible_responses = [str(i) for i in list_of_possible_responses]
        self.choices = list_of_possible_responses
        s = "Choices: {}".format(", ".join(list_of_possible_responses))
        self.display_choices = []
        self.display_choices.append(s)
        # --------------------------------------
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        # self.input_text_color = constants.ORANGE
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
            pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            # pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            if self.show_possible_responses == True:
                utils.talk_dialog(self.screen, self.display_choices, self.font,
                                  width_offset=self.x, height_offset=self.y-40,
                                  line_length=60,
                                  color=constants.BLACK)
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
        # ---- ----
        if len(self.message) == 0:
            # window closed without making a choice
            return None
        if utils.is_int(self.message) == False:
            if self.message == "n":
                # The user wishes to exit the window
                return None
            elif self.message == "y":
                raise ValueError("fix this")
            s = "This is not of type int: {}\n".format(self.message)
            s += "It is of type: {}".format(type(self.message))
            raise ValueError(s)
        return self.message


# ------------------------------------------------------------
#                    class QuizDialogInput
# ------------------------------------------------------------
class QuizDialogInput:
    def __init__(self, text_list, list_of_possible_responses,
                 show_possible_responses=True,
                 width=600, height=600, line_width=50):
        self.show_possible_responses = show_possible_responses
        self.display_list = utils.string_to_list(text_list, line_width)
        # ----
        list_of_possible_responses = [str(i) for i in list_of_possible_responses]
        self.choices = list_of_possible_responses
        s = "Choices: {}".format(", ".join(list_of_possible_responses))
        self.display_choices = []
        self.display_choices.append(s)
        # --------------------------------------
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_rect = pygame.Rect(10, self.height - 50, self.width - 20, 40)
        # self.input_text_color = constants.ORANGE
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
            pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            # pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            if self.show_possible_responses == True:
                utils.talk_dialog(self.screen, self.display_choices, self.font,
                                  width_offset=self.x, height_offset=self.y - 40,
                                  line_length=60,
                                  color=constants.BLACK)
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
        # ---- ----
        if len(self.message) == 0:
            # window closed without making a choice
            return None
        if utils.is_int(self.message) == False:
            if self.message in ["y", "n"]:
                return self.message
            s = "This is not of type int: {}\n".format(self.message)
            s += "It is of type: {}".format(type(self.message))
            raise ValueError(s)
        return self.message

# ------------------------------------------------------------
#                    class TransitionScreen
# ------------------------------------------------------------

class TransitionScreen:
    def __init__(self, image_to_display="splashscreen01.png",
                 screen_width=600, screen_height=600):
        self.width = screen_width
        self.height = screen_height
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.big_window_background_color = constants.WHITE
        # --------------------------------------
        # filepath = utils.get_filepath02(image_to_display, constants.IMAGES)
        self.mysprite = SimpleSprite(image_to_display)
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        # self.font = pygame.font.Font(None, 35)

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
                    pass
                    # self.user_text += event.unicode

    def draw(self):
        self.screen.fill(constants.UGLY_PINK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main(self):
        counter = 0
        self.all_sprites.add(self.mysprite)
        while self.keep_looping:
            counter += 1
            self.clock.tick(10)
            self.handle_events()
            self.draw()
            if counter > 15:
                self.keep_looping = False
        return

if __name__ == "__main__":
    mydialog = QuizDialogInput(["text list"], [1, 2, 3])
    message = mydialog.main()
    print(message)
    # mydialog = TransitionScreen()
    # mydialog.main()