import pygame
import utils

class Window:
    def __init__(self):
        self.init_pygame()
        self.x, self.y = 3, 3
        self.body = pygame.Rect(self.x * self.TILEWIDTH,
                                self.y * self.TILEWIDTH,
                                self.TILEWIDTH, self.TILEWIDTH)
        self.BG_COLOR = (200, 200, 200)
        self.keep_looping = True
        # self.g = utils.get_moves(100)
        self.g = None
        self.class_counter = 0
        self.local_counter = 0

    def init_pygame(self):
        pygame.init()
        self.TILEWIDTH = 100
        self.TILES_WIDE = 6
        self.TILES_HEIGH = 5
        self.WINDOW_WIDTH = self.TILEWIDTH * self.TILES_WIDE
        self.WINDOW_HEIGHT = self.TILEWIDTH * self.TILES_HEIGH
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Example")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 40)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_LEFT:
                    self.x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.x += 1
                elif event.key == pygame.K_UP:
                    self.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.y += 1
                # else:
                #     self.text += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        # ----------------------
        self.body = pygame.Rect(self.x * self.TILEWIDTH,
                                self.y * self.TILEWIDTH,
                                self.TILEWIDTH, self.TILEWIDTH)
        pygame.draw.rect(self.screen, (100, 100, 100), self.body)
        pygame.display.set_caption("Example: {}".format(self.class_counter))
        self.class_counter += 1
        # ----------------------
        pygame.display.update()

    def move(self):
        next_move = ""
        try:
            next_move = next(self.g)
        except:
            self.g = utils.get_moves(100)
            next_move = next(self.g)
        if next_move == "up":
            self.y -= 1
        elif next_move == "down":
            self.y += 1
        elif next_move == "right":
            self.x += 1
        elif next_move == "left":
            self.x -= 1
        else:
            raise ValueError("Not found: {}".format(next_move))
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x > self.TILES_WIDE: self.x = self.TILES_WIDE
        if self.y > self.TILES_HEIGH: self.y = self.TILES_HEIGH

    def update(self):
        self.local_counter += 1
        if self.local_counter > 5:
            self.local_counter = 0
            self.move()

    def main(self):
        self.update()
        self.draw()
        while self.keep_looping:
            self.clock.tick(10)
            self.events()
            self.update()
            self.draw()


if __name__ == "__main__":
    mywin = Window()
    mywin.main()
