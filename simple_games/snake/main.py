import pygame
import constants
import time
import random
import sys, os

keep_looping = True
index_counter = 0
mydict = {}
mydict["index"] = 0
mydict["x"] = constants.SCREEN_WIDTH / 2
mydict["y"] = constants.SCREEN_HEIGHT / 2
mydict["head"] = True
snake_x, snake_y = 0, 0
snake = [mydict]
food_x, food_y = -1, -1
movement_inc = constants.MOVEMENT_INC
direction = None

pygame.init()
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption(constants.TITLE)
clock = pygame.time.Clock()

def get_high_score():
    filepath = os.path.join("high_score.txt")
    with open(filepath, "r") as f:
        lines = f.readlines()
        lines = [i.strip() for i in lines if len(i.strip()) > 0]
    return int(lines[0])

def continue_playing(a_reason):
    screen.fill(constants.WHITE)
    line0_text = "Congratulations! You've set a new HIGH SCORE!"
    line1_text = "Game over"
    line2_text = "(Reason: {})".format(a_reason)
    line3_text = "Would you like to play again? (y/n)"
    # ---- ----
    line1 = font.render(line1_text, True, constants.BLACK)
    line2 = font.render(line2_text, True, constants.BLACK)
    line3 = font.render(line3_text, True, constants.BLACK)
    if len(snake)-1 > high_score:
        line0 = font.render(line0_text, True, constants.BLACK)
        i0 = (constants.SCREEN_WIDTH / 2) - line0.get_width() + (line0.get_width() / 2)
        j0 = (constants.SCREEN_HEIGHT / 2) - line0.get_height()
    i = (constants.SCREEN_WIDTH / 2) - line1.get_width() + (line1.get_width() / 2)
    j = (constants.SCREEN_HEIGHT / 2) - line1.get_height()
    i2 = (constants.SCREEN_WIDTH / 2) - line2.get_width() + (line2.get_width() / 2)
    j2 = (constants.SCREEN_HEIGHT / 2) - line2.get_height()
    i3 = (constants.SCREEN_WIDTH / 2) - line3.get_width() + (line3.get_width() / 2)
    j3 = (constants.SCREEN_HEIGHT / 2) - line3.get_height()
    while True:
        clock.tick(40)
        if len(snake) - 1 > high_score:
            screen.blit(line0, [i0, j0-(line0.get_height()*4)])
        screen.blit(line1, [i, j-(line1.get_height()*2)])
        screen.blit(line2, [i2, j2])
        screen.blit(line3, [i3, j3+(line3.get_height()*2)])
        pygame.display.update()
        # ---- ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False

def end_condition_met():
    # Has the snake gone out-of-bounds?
    continue_loop = True
    a_reason = ""
    if snake_x < 0 or snake_x > constants.SCREEN_WIDTH:
        print("snake_x: {}, snake_y: {}".format(snake_x, snake_y))
        continue_loop = False
        a_reason = "Travelled off screen."
    if snake_y < 0 or snake_y > constants.SCREEN_HEIGHT:
        print("snake_x: {}, snake_y: {}".format(snake_x, snake_y))
        continue_loop = False
        a_reason = "Travelled off screen."
    # ---- ----
    # Has the snake traveled through itself?
    if snake_overlap() == True:
        continue_loop = False
        a_reason = "Head touched body"
        # ---- ----
    return continue_loop, a_reason

def text_message(message, colour):
    the_message = font.render(message, True, colour)
    i = (constants.SCREEN_WIDTH / 2) - the_message.get_width() + (the_message.get_width() / 2)
    j = (constants.SCREEN_HEIGHT/ 2) - the_message.get_height()
    screen.blit(the_message, [i, j])

def record_high_score():
    filepath = os.path.join("high_score.txt")
    with open(filepath, "w") as f:
        s = "{}".format(len(snake)-1)
        f.write(s)

def goodbye():
    screen.fill(constants.WHITE)
    text_message("Thanks for playing!", constants.GREEN)
    pygame.display.update()
    time.sleep(0.5)
    # ---- ----
    if len(snake)-1 > high_score:
        record_high_score()
    # ---- ----
    pygame.quit()
    sys.exit()

def snake_ate_food():
    if food_x - constants.TILESIZE <= snake_x <= food_x + constants.TILESIZE:
        if food_y - constants.TILESIZE <= snake_y <= food_y + constants.TILESIZE:
            return True
    return False

def move():
    global index_counter, snake_x, snake_y
    if direction is None: return False
    # ---- ----
    if direction == "down":
        snake_y += movement_inc
    elif direction == "up":
        snake_y -= movement_inc
    elif direction == "left":
        snake_x -= movement_inc
    elif direction == "right":
        snake_x += movement_inc
    else:
        raise ValueError("Error")
    index_counter += 1
    mydict = {}
    mydict["index"] = index_counter
    mydict["x"] = snake_x
    mydict["y"] = snake_y
    mydict["head"] = True
    return mydict

def spawn_food():
    global food_x, food_y
    food_x = random.randint(0, constants.SCREEN_WIDTH-constants.TILESIZE)
    food_y = random.randint(0, constants.SCREEN_HEIGHT-constants.TILESIZE)

def handle_events():
    global keep_looping, snake_x, snake_y, direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_looping = False
            goodbye()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keep_looping = False
                goodbye()
            elif event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"

def  get_head():
    for section in snake:
        if section["head"] == True:
            return section
    return None

def snake_overlap():
    # Has the snake traveled through itself?
    for section in snake:
        head = get_head()
        if head is None:
            s = "Snake: {}".format(snake)
            raise ValueError(s)
        for section in snake:
            if section["head"] == False:
                if section["x"] == head["x"]:
                    if section["y"] == head["y"]:
                        return True
    return False

def think():
    global snake
    def remove_tail():
        lowest = 100000
        for section in snake:
            if section["index"] < lowest:
                lowest = section["index"]
        mytemp = []
        for section in snake:
            if section["index"] != lowest:
                mytemp.append(section)
        return mytemp
    # ---- ---- ---- ----
    if len(snake) > 1:
        for mydict in snake:
            mydict["head"] = False
    # ---- ----
    new_section = move()
    if new_section == False: return False
    # ---- ----
    snake.insert(0, new_section)
    # Has the snake eaten the food?
    if snake_ate_food() == True:
        spawn_food()
    else:
        snake = remove_tail()
        if len(snake) == 0:
            raise ValueError("Error")

def draw():
    global screen, starting_colour
    screen.fill(constants.WHITE)
    pygame.display.set_caption("Snake: {} | High Score: {}".format(len(snake)-1, high_score))
    pygame.draw.rect(screen, constants.BLUE, [food_x, food_y, 10, 10])
    for mydict in snake:
        if mydict["head"] == True:
            pygame.draw.rect(screen, constants.RED, [mydict["x"], mydict["y"], 10, 10])
        else:
            pygame.draw.rect(screen, constants.BLACK, [mydict["x"], mydict["y"], 10, 10])
    pygame.display.update()

# ------------------------------------------------

def main():
    global keep_looping, snake
    keep_looping = True
    a_reason = ""
    spawn_food()
    while keep_looping == True:
        clock.tick(10)
        handle_events()
        think()
        draw()
        # ---- ----
        keep_looping, a_reason = end_condition_met()
    # ---- ---- ---- ----
    return continue_playing(a_reason)

# ************************************************
# ************************************************

high_score = -1
keep_playing = True
while keep_playing == True:
    high_score = get_high_score()
    snake_x = constants.SCREEN_WIDTH / 2
    snake_y = constants.SCREEN_HEIGHT / 2
    direction = None
    keep_playing = main()
    if keep_playing == True:
        if len(snake)-1 > high_score:
            record_high_score()
        # ---- ----
        mydict = {}
        mydict["index"] = 0
        mydict["x"] = constants.SCREEN_WIDTH / 2
        mydict["y"] = constants.SCREEN_HEIGHT / 2
        mydict["head"] = True
        snake_x, snake_y = 0, 0
        snake = [mydict]

goodbye()
