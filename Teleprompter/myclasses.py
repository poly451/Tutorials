import pygame
import utils
import constants as con

class StrangeTeleprompter:
    def __init__(self, filepath, height=400, line_width=50):
        self.filepath = filepath
        self.complete_text = self.get_text()
        self.height = height
        self.width = 1000
        self.line_width = line_width
        self.keep_looping = True
        self.temp_counter = 0
        # --------------------------
        self.BG_COLOR = con.WHITE
        # --------------------------
        self.scroll_up = True
        self.counter = 0
        self.gate_value = 1
        self.counter_increment = 1
        self.pygame_init()
        self._initialize_rectangles()

    def pygame_init(self):
        pygame.init()
        # ---------------------------
        self.clock = pygame.time.Clock()
        self.font_size = 80
        self.font = pygame.font.Font(None, self.font_size)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def get_text(self):
        with open(self.filepath, "r") as f:
            mylines = f.readlines()
            mylines = [i.strip() for i in mylines if len(i.strip()) > 0]
        mylines = utils.clean_text(mylines)
        mylines = " ".join(mylines)
        mylines = "{}{}".format(" " * 40, mylines)
        return mylines

    def _initialize_rectangles(self):
        top_rectangle_left = 10
        top_rectangle_top = 10
        top_rectangle_width = self.width - 20
        top_rectangle_height = self.height - (20 * 6)
        self.text_rect = pygame.Rect(top_rectangle_left,
                                     top_rectangle_top,
                                     top_rectangle_width,
                                     top_rectangle_height)

    # ---------------------------

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                print(pygame.KEYDOWN)
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_d:
                    print("Plus +++++++++")
                    # self.gate_value -= 1
                    self.counter_increment += 1
                elif event.key == pygame.K_a:
                    print("Minus ----------")
                    # self.gate_value += 1
                    self.counter_increment -= 1
                elif event.key == pygame.K_w:
                    self.scroll_up = True
                elif event.key == pygame.K_s:
                    self.scroll_up = False

    def update(self):
        if self.scroll_up == True:
            self.counter -= self.counter_increment
        else:
            self.counter += self.counter_increment


    def draw_text(self):
        pygame.draw.rect(self.screen, con.WHITE, self.text_rect)
        utils.talk_dialog(self.screen, self.complete_text, self.font, width_offset=20, height_offset=self.counter)

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_text()
        pygame.display.flip()

    def main(self):
        self.clock.tick(20)
        while self.keep_looping:
            self.events()
            self.update()
            self.draw()

if __name__ == "__main__":
    # Used for debugging
    filepath = "data/scripts/script_testing.txt"
    teleprompter = StrangeTeleprompter(filepath)
    teleprompter.main()
