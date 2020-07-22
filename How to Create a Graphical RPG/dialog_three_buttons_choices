import pygame
import constants as con
import utils
import sys
# Thanks to:
# https://stackoverflow.com/questions/53238491/python-pygame-mouse-position-and-which-button-is-pressed
# ------------------------------------------------------------
#                         class IntroPanel
# ------------------------------------------------------------

class IntroPanel:
    def __init__(self):
        pygame.init()
        self.width = 250
        self.height = 215
        self.screen = pygame.display.set_mode((self.width, self.height))
        s = "Welcome to the {}".format(con.TITLE)
        pygame.display.set_caption(s)
        self.clock = pygame.time.Clock()
        self.BG_COLOR = con.LIGHTGREY
        self.font = pygame.font.Font(None, 35)
        # --------------------------------------
        self.new_game_rect = pygame.Rect(10, 10, self.width - 20, 55)
        self.new_game_text = "New Game"
        self.new_game_color = con.WHITE
        # --------------------------------------
        self.load_game_rect = pygame.Rect(10, 80, self.width - 20, 55)
        self.load_game_text = "Load Game"
        self.load_game_color = con.WHITE
        # --------------------------------------
        self.quit_rect = pygame.Rect(10, 150, self.width - 20, 55)
        self.quit_text = "Quit"
        self.quit_color = con.LIGHT_PURBLE
        # --------------------------------------
        self.mouse_pos = None
        self.keep_looping = True
        self.message = ""

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                print("mouse pressed:", mouse_pressed)
                if mouse_pressed[0] == 1:
                    self.mouse_pos = pygame.mouse.get_pos()

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ==== New Game =====================================
        utils.draw_text_button(self.screen, self.new_game_text, self.new_game_rect,
                               self.font, font_color=con.BLACK, background_color=con.WHITE, use_inner=True)
        # ==== Load Game =====================================
        utils.draw_text_button(self.screen, self.load_game_text, self.load_game_rect,
                               self.font, font_color=con.BLACK, background_color=con.WHITE, use_inner=True)
        # ==== Quit =====================================
        utils.draw_text_button(self.screen, self.quit_text, self.quit_rect,
                                self.font, font_color=con.BLACK, background_color=con.WHITE, use_inner=True)
        if not self.mouse_pos == None:
            new_game_result = self.new_game_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            load_game_result = self.load_game_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            quit_result = self.quit_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1])
            self.mouse_pos = None
            if new_game_result == 1:
                self.message = "new game"
            elif load_game_result == 1:
                self.message = "load game"
            elif quit_result == 1:
                self.message = "quit"
            if len(self.message) > 0:
                self.keep_looping = False
        # -----------------------------------------
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(40)
            self.events()
            self.draw()
        return self.message

if __name__ == "__main__":
    mydialog = IntroPanel()
    message = mydialog.main()
    print("message: ", message)

