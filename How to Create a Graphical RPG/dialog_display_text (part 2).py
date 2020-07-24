import pygame
import utils
import constants as con
# ------------------------------------------------------------
#                         class TextDialog
# ------------------------------------------------------------

class TextDialog:
    def __init__(self, text, height=400, line_width=50):
        self.text_list = []
        if type(text) == type("bla"):
            self.text_list = utils.separate_text_into_lines(text, line_width)
        elif type(text) == type([]):
            self.text_list.append(text)
        else:
            s = "Doh! That type of data shouldn't be here!"
            raise ValueError(s)
        # -------------------------
        pygame.init()
        self.font = pygame.font.Font(None, 35)
        # -------------------------
        # Calculate the width and hight of the window we're using
        # for the back of the dialog box.
        text_width, text_height = self.font.size("a")
        self.width = 50 * text_width
        if len(self.text_list) > 12:
            self.height = 600
        else:
            self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        # ----
        # Calulate the desired height of each line, given the
        # text we want to display.
        self.line_height = -1
        for elem in self.text_list:
            text_width, text_height = self.font.size(elem)
            if text_height > self.line_height:
                self.line_height = text_height
        # -------------------------
        self.button_color = con.BLACK
        self.BG_COLOR = con.LIGHTGREY
        self.window_background_color = con.WHITE
        # -------------------------
        self.mouse_pos = None
        self.okay_rect = None
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
        left = 10
        top = 10
        width = self.width - 20
        height = self.height - (20 * 3)
        window_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, self.window_background_color, window_rect)
        # ----------------------
        button_width = 60
        left = int(self.width / 2) - int(button_width / 2)
        top = int(self.height / 1.12)
        width = button_width
        height = 35
        self.okay_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.screen, self.button_color, self.okay_rect)
        # ----------------------
        self._draw_lines()
        # ---- Draw the button rectangle ----
        left = int(self.width / 2) - int(button_width / 2) + 10
        top = int(self.height / 1.12) + 8
        width = button_width
        height = 35
        mytext_rect = pygame.Rect(left, top, width, height)
        # ---- Render the text used to label the button. ----
        surface = self.font.render("OK", True, con.BLACK)
        self.screen.blit(surface, mytext_rect)
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

if __name__ == "__main__":
    mytext = "The Fourth Test of the 1948 Ashes series was one of five "
    mytext += "Tests in a cricket series between Australia and England. "
    mytext += "Played at Headingley Stadium at Leeds from 22 to 27 July, "
    mytext += "for the third time in a row the match set a new record "
    mytext += "for the highest attendance at a Test in England. On the "
    mytext += "last day, Australia, captained by Don Bradman (pictured), "
    mytext += "had a target of 404 to make up, and England had used a heavy "
    mytext += "roller to break up the pitch to make batting harder."
    mydialog = TextDialog(mytext)
    mydialog.main()
