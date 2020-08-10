import button
import constants as con
import pygame

class OuterWindow:
    def __init__(self):
        self.pygame_init()
        self.keep_looping = True
        self.event_var = None
        # -----------------------
        self.pos = None
        self.current_action = None
        # -----------------------
        self.clear_button = button.Button("clear", con.ORANGE, x=10, y=10,
                                         width=235, height=50, text="Clear",
                                         message="clear", font=self.font)
        self.randomButton = button.Button("random", con.ORANGE, x=255, y=10,
                                          width=235, height=50, text="Random",
                                          message="random", font=self.font)
        self.primary_color_btn = button.Button("primary", con.BLUE, x=500, y=10,
                                               width=90, height=235, text="P",
                                               message="primary", font=self.font)
        self.background_color_btn = button.Button("background", con.WHITE, x=500, y=255,
                                               width=90, height=235, text="B",
                                               message="background", font=self.font)
        self.main_window = button.Button("main", con.WHITE, x = 10, y=70,
                                         width = 480, height=420, text="main window",
                                         message="main window", font=self.font)
        self.buttons = []
        self.buttons.append(self.clear_button)
        self.buttons.append(self.randomButton)
        self.buttons.append(self.main_window)
        self.buttons.append(self.primary_color_btn)
        self.buttons.append(self.background_color_btn)
        self.main_window.message = "none"

    def pygame_init(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Simple Interface")
        self.font = pygame.font.Font(None, 35)
        self.clock = pygame.time.Clock()

    def events(self):
        for event in pygame.event.get():
            self.pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for a_button in self.buttons:
                    if a_button.isOver(self.pos):
                        if not a_button.name == "main":
                            a_button.color = con.RED
                        if a_button.name == "random":
                            if self.main_window.message == "paint random":
                                self.main_window.message = "stop adding"
                            else:
                                self.main_window.message = "paint random"
                        elif a_button.name == "primary":
                            self.main_window.color = self.primary_color_btn.face_color
                        elif a_button.name == "background":
                            self.main_window.color = self.background_color_btn.face_color
                        elif a_button.name == "clear":
                            self.main_window.list_of_circles = []
                        elif a_button.name == "main":
                            pass
                        else:
                            raise ValueError("Error! I couldn't find this: {}".format(a_button.name))
            elif event.type == pygame.MOUSEBUTTONUP:
                for a_button in self.buttons:
                    if not a_button.name == "main":
                        a_button.color = a_button.face_color

    def draw(self):
        self.surface.fill(con.LIGHTGREY)
        for a_button in self.buttons:
            a_button.draw(self.surface, True)
        self.main_window.draw_random(self.surface)
        pygame.display.update()

    def main(self):
        while self.keep_looping:
            self.clock.tick(40)
            self.events()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    mywindow = OuterWindow()
    mywindow.main()
