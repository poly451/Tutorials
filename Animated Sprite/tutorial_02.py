import pygame
import constants
import os, sys

# ------------------------------------------------------
#                       class Player
# ------------------------------------------------------
class Player(pygame.sprite.Sprite):
    x, y = 0, 0
    def __init__(self, directory_path, movement_increment):
        super().__init__()
        if os.path.isdir(directory_path) == False:
            s = "This isn't a directory: {}".format(directory_path)
            raise ValueError(s)
        # ----
        self.image_list = self.load_images(directory_path)
        # ----
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.movement_increment = movement_increment

    def load_images(self, directory_path):
        images = []
        for file_name in os.listdir(directory_path):
            path = os.path.join(directory_path, file_name)
            try:
                image = pygame.image.load(path)
            except Exception as e:
                s = "{}\nI couldn't load this path: {}".format(e, path)
                raise ValueError(s)
            image = pygame.transform.scale(image, (constants.TILESIZE, constants.TILESIZE))
            images.append(image)
        return images

    def next_frame(self, x, y):
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[self.index]
        self.rect = pygame.Rect(x, y, constants.TILESIZE, constants.TILESIZE)

    def move(self, advance_x, advance_y, x, y):
        dx = self.movement_increment * advance_x
        dy = self.movement_increment * advance_y
        self.rect = self.rect.move(dx, dy)
        # ----
        x += dx
        y += dy
        return x, y

    def debug_print(self):
        print("rect: {}".format(self.image.get_rect()))

# ------------------------------------------------------
#                       class ControllingMySprite
# ------------------------------------------------------
class Game:
    def __init__(self, directory_name, movement_increment):
        if os.path.isdir(directory_name) == False:
            raise ValueError("Error")
        self.init_graphics()
        # ----
        self.x, self.y = 0, 0
        self.player = Player(directory_name, movement_increment)
        # ----
        self.direction = "idle"
        self.counter = 0
        self.keep_looping = True

    def init_graphics(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
        self.all_sprites = pygame.sprite.Group()

    # #####################################################

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                    return True
                # ----
                if event.key == pygame.K_RIGHT:
                    self.direction = "right"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_UP:
                    self.direction = "up"
            elif event.type == pygame.KEYUP:
                self.direction = "idle"

    def update(self):
        if self.direction == "right":
            print("Moving right")
            self.x, self.y = self.player.move(1, 0, self.x, self.y)
            self.player.next_frame(self.x, self.y)
        elif self.direction == "left":
            self.x, self.y = self.player.move(-1, 0, self.x, self.y)
            self.player.next_frame(self.x, self.y)
        elif self.direction == "up":
            self.x, self.y = self.player.move(0, -1, self.x, self.y)
            self.player.next_frame(self.x, self.y)
        elif self.direction == "down":
            self.x, self.y = self.player.move(0, 1, self.x, self.y)
            self.player.next_frame(self.x, self.y)
        elif self.direction == "idle":
            self.player.next_frame(self.x, self.y)
        else:
            s = "self.direction: {}".format(self.direction)
            raise ValueError(s)
        # ----
        self.counter += 1

    def draw(self):
        self.screen.fill(constants.BG_COLOR)
        self.all_sprites = pygame.sprite.Group()
        # ----
        self.all_sprites.add(self.player)
        # ----
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()

    # #####################################################

    def goodbye(self):
        pygame.quit()
        sys.exit()

    def main(self):
        while self.keep_looping == True:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.update()
            self.draw()
        self.goodbye()

# *****************************************************
def main():
    # directory_path = "/Users/BigBlue/Documents/Programming/game_resources/programmerArt/animations/player_pumpkin/walk"
    directory_path = os.path.join("data", "images", "characters", "baldric", "walk", "front")
    movement_inc = 5
    control_sprite_strip = Game(directory_path,
                                movement_increment=movement_inc)
    control_sprite_strip.main()

if __name__ == "__main__":
    main()