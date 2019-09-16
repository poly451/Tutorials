import pygame
import sys

TILESIZE = 64
WIDTH = TILESIZE * 16
HEIGHT = TILESIZE * 16
RED = (255, 0, 0)

# ----------------------------------------------------------------
#                           class Game
# ----------------------------------------------------------------

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My World')
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_surface.fill(RED)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.myquit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.myquit()
                    return True

    def myquit(self):
        pygame.quit()
        sys.exit()

# ==================================================================
# ==================================================================

def setup():
    mygame = Game()

    while True:
        mygame.handle_events()
        # ----------------------------------
        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    setup()

