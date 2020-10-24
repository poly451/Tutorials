import pygame
import constants as con
import utils
import os, sys
# ------------------------------------------------------------
#                    class MainDialog
# ------------------------------------------------------------

class GetFilepathDialog:
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
        self.text = ""
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
        self.message = ""
        self.file_name = ""
        self.window_text_list = []
        self.assemble_initial_menu()

    def assemble_initial_menu(self):
        filepath = os.path.join("data", "scripts")
        menu_items = utils.get_directories(filepath)
        self.window_text_list = ["{}. {}".format(count+1, i.replace(".txt", "")) for count, i in enumerate(menu_items)]

    def draw_menu(self):
        utils.talk_dialog(self.screen, self.window_text_list, self.font, width_offset=0, height_offset=0, line_length=30, color=(255,255,255))

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
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.user_text = self.text
                    self.text = ""
                    self.process_directory_input()
                    if self.file_name.find(".txt") > -1:
                        self.keep_looping = False
                else:
                    self.text += event.unicode

    def process_directory_input(self):
        def is_valid(mystring):
            if mystring == ".DS_Store": return False
            return True
        # -----------------------------------------------------
        if not utils.is_int(self.user_text): return False
        myint = int(self.user_text)
        if not myint in list(range(1, len(self.window_text_list)+1)):
            return False
        # -----------------------------------------------------
        dir = self.window_text_list[myint-1]
        myint = dir.find(" ")
        dir = dir[myint:].strip()
        dir = dir.replace(" ", "_")
        self.file_name = dir
        print(dir)
        filepath = os.path.join("data", "scripts")
        filepaths = os.listdir(filepath)
        self.window_text_list = [i for i in filepaths if is_valid(i)]
        self.window_text_list = ["{}. {}".format(count+1, i) for count, i in enumerate(self.window_text_list) if is_valid(i)]

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
        utils.talk_dialog(self.screen, self.window_text_list, self.font, width_offset=15, height_offset=5, line_length=50)

    def _draw_user_input_window(self):
        pygame.draw.rect(self.screen, self.user_text_rect_background_color, self.user_rect)
        utils.talk_dialog(self.screen, self.text, self.font, width_offset=15, height_offset=300, line_length=50)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self._draw_big_window()
        self._draw_user_input_window()
        pygame.display.flip()

    def update(self):
        pass

    # -------------------------------------------------------------

    def main(self):
        quiz_type = ""
        self.clock.tick(20)
        self.keep_looping = True
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()
        return os.path.join("data", "scripts", self.file_name)

# ------------------------------------------------------------
#                         class TextDialog
# ------------------------------------------------------------

class TextDialog:
    def __init__(self, text, line_width=40):
        self.window_width = 600
        self.window_height = 500
        # -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        # -------------------------
        if len(text) > 910:
            s = "That text is too long! "
            s += "It must be equal to or less than 910 characters."
            raise ValueError(s)
        # -------------------------
        large_height = 600
        # -------------------------
        self.BG_COLOR = con.LIGHTGREY
        self.text_list = []
        if type(text) == type("bla"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            self.text_list = text
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        self.okay_rect = pygame.Rect(300, 300, 100, 75)
        self.ok_image = pygame.image.load(os.path.join("data", "images", "buttons", "ok02.png")).convert_alpha()
        self.ok_image = pygame.transform.scale(self.ok_image, (self.okay_rect[0], self.okay_rect[1]))
        # -------------------------
        text_width, text_height = self.font.size("a")
        self.width = 50 * text_width
        kind = ""
        self.height = large_height
        kind = "large dialog"
        self.line_height = -1
        for elem in self.text_list:
            text_width, text_height = self.font.size(elem)
            if text_height > self.line_height:
                self.line_height = text_height
        window_left = 10
        window_top = 10
        window_width = self.width - 20
        window_height = self.height - (20 * 3)
        self.window_rect = pygame.Rect(window_left, window_top, window_width - 50, window_height - 100)
        # --------------------------
        # -------- OK Button -------
        button_width = 60
        button_height = 35
        button_left = int(self.height / 2)
        top = 600 - button_height
        print("width: ", button_width)
        self.okay_rect = pygame.Rect(button_left, top, button_width, button_height)
        self.ok_image = pygame.image.load(os.path.join("data", "images", "buttons", "ok02.png")).convert_alpha()
        self.ok_image = pygame.transform.scale(self.ok_image, (0, 0))
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
        for count, elem in enumerate(self.text_list):
            surface = self.font.render(elem, True, (0, 0, 0))
            # ----------------------
            left = 20
            top = (self.line_height * count) + 20
            # ----------------------
            self.screen.blit(surface, (left, top), area=None)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ----------------------
        pygame.draw.rect(self.screen, con.WHITE, self.window_rect)
        # ----------------------
        # pygame.draw.rect(self.screen, con.PURPLE, self.ok_image)
        myrect = self.ok_image.get_rect()
        self.screen.blit(self.screen, myrect)
        # ----------------------
        self._draw_lines()
        # --------------------------------------------------
        if not self.mouse_pos == None:
            okay_result = self.ok_image.collidepoint(self.mouse_pos)
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
#                         class TextDialog_YesNo
# ------------------------------------------------------------

class TextDialog_YesNo:
    def __init__(self, text, line_width=40):
        self.window_width = 600
        self.window_height = 300
        # -------------------------
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.BG_COLOR = con.LIGHTGREY
        self.text_list = []
        # -------------------------
        if type(text) == type("bla"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            self.text_list.append(text)
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        self.yes_rect = pygame.Rect(300, 300, 100, 75)
        self.yes_image = pygame.image.load(os.path.join("data", "images", "buttons", "yes_grey.png")).convert_alpha()
        self.yes_image = pygame.transform.scale(self.yes_image, (100, 50))
        # -------------------------
        self.no_rect = pygame.Rect(10, 230, 250, 75)
        self.no_image = pygame.image.load(os.path.join("data", "images", "buttons", "no_grey.png")).convert_alpha()
        self.no_image = pygame.transform.scale(self.no_image, (100, 50))
        # -------------------------
        self.text_window_rect = pygame.Rect(10, 10, 580, 220)
        # -------------------------
        self.message = ""
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
                if mouse_pressed[1] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                elif mouse_pressed[2] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ----------------------
        pygame.draw.rect(self.screen, con.WHITE, self.text_window_rect)
        yes_blit_rect = self.screen.blit(self.yes_image, (490, 240))
        no_blit_rect = self.screen.blit(self.no_image, (10, 240))
        # ----------------------
        utils.talk_dialog(self.screen, self.text_list, self.font, 20, 10)
        # --------------------------------------------------
        if not self.mouse_pos == None:
            yes_result = yes_blit_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            no_result = no_blit_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            self.mouse_pos = None
            if yes_result == 1:
                self.message = "yes"
                self.keep_looping = False
            if no_result == 1:
                self.message = "no"
                self.keep_looping = False
        # --------------------------------------------------
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.events()
            self.draw()
        return self.message

if __name__ == "__main__":
    mydialog = GetFilepathDialog()
    print("output:", mydialog.main())
