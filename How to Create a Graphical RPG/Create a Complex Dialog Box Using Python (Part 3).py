import pygame
import constants as con
import utils
from dialog_text import TextDialog

# ------------------------------------------------------------
#                    class DialogTextInput
# ------------------------------------------------------------

class DialogTextInput:
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

    def main_loop(self, text):
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
#                    class DialogGetText
# ------------------------------------------------------------

class DialogGetText:
    def __init__(self, height=400, line_width=50):
        self.height = height
        self.line_width = line_width

    def main(self):
        char_name, char_kind = "", ""
        keep_looping = True
        while keep_looping:
            s = "What would you like to name your character?"
            mydialog = DialogTextInput(self.height, self.line_width)
            char_name = mydialog.main_loop(s).strip()
            if len(char_name) == 0:
                mydialog = TextDialog("Doh! Your character needs a name. Let's try that again.")
                mydialog.main()
            else:
                keep_looping = False
        # -----------------------
        keep_looping = True
        while keep_looping:
            mydialog = DialogTextInput(self.height, self.line_width)
            s = "What class would you like your character to be? "
            s += "Choose one of the following: "
            s += ', '.join(con.CHAR_KINDS).upper()
            char_kind = mydialog.main_loop(s).strip()
            if not char_kind in con.CHAR_KINDS:
                s = "Doh! That is not a class I recognize. Please "
                s += "choose one of the following: "
                s += ', '.join(con.CHAR_KINDS).upper()
                mydialog = TextDialog(s)
                mydialog.main()
            else:
                keep_looping = False
        return char_name, char_kind

if __name__ == "__main__":
    mydialog = DialogGetText()
    char_name, char_kind = mydialog.main()
    print("char name: {}, char kind: {}".format(char_name, char_kind))
