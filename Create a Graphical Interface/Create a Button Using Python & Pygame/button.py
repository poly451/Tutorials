# How to Create a Button in Pygame [CODE IN DESCRIPTION]
# Most of this code came from:
# https://www.youtube.com/watch?time_continue=310&v=4_9twnEduFA&feature=emb_logo
import pygame
import random
import utils
import constants as con

class Button():
    def __init__(self, name, fcolor, x, y, width, height, text, message, font):
        self.name = name
        self.font = font
        self.message = message
        self.color = fcolor
        self.face_color = fcolor
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.text = text
        # -------------------
        self.list_of_circles = []

    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, con.BLACK, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # --------------------------------
        if len(self.text) > 0:
            text_surface = self.font.render(self.text, True, con.BLACK)
            temp_x = (self.width / 2 - text_surface.get_width() / 2)
            temp_y = (self.height / 2 - text_surface.get_height() / 2)
            screen.blit(text_surface, (self.x + temp_x, self.y + temp_y))

    def draw_random(self, screen):
        if self.message == "paint random":
            temp_x = random.randint(10, self.width)
            temp_y = random.randint(75, self.height + 65)
            pos = (temp_x, temp_y)
            radius = random.randint(2, 10)
            self.list_of_circles.append([pos, utils.get_color(), radius])
        elif self.message == "stop adding":
            pass
        self.paint(screen)

    def paint(self, screen):
        # print(len(self.list_of_circles))
        for a_point in self.list_of_circles:
            pygame.draw.circle(surface=screen, color=a_point[1], center=a_point[0], radius=a_point[2])

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
