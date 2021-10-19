import random

def _random_change(x, y):
    def one_axis(foo):
        myint = random.randint(0, 1)
        if myint == 0:
            foo += 1
        else:
            foo -= 1
        return foo
    # ----
    new_x, new_y = -1, -1
    myint_xy = random.randint(0, 1)
    if myint_xy == 0:
        new_x = one_axis(x)
    elif myint_xy == 1:
        new_y = one_axis(y)
    else:
        pass
    return new_x, new_y

def obstacle_in_the_way(x, y, obstacles):
    for elem in obstacles:
        if elem.x == x and elem.y == y:
            return True
    return False

def _move_toward_helper(x1, y1, x2, y2):
    if x1 == x2 and y1 != y2:
        if abs((y1-1)-y2) < abs((y1+1)-y2):
            y1 = y1 - 1
        else:
            y1 = y1 + 1
    elif x1 != x2 and y1 == y2:
        if abs((x1-1)-x2) < abs((x1+1)-x2):
            x1 = x1 - 1
        else:
            x1 = x1 + 1
    elif x1 != x2 and y1 != y2:
        myrand = random.randint(0, 1)
        if myrand == 0:
            if abs((y1 - 1) - y2) < abs((y1 + 1) - y2):
                y1 = y1 - 1
            else:
                y1 = y1 + 1
        elif myrand == 1:
            if abs((x1 - 1) - x2) < abs((x1 + 1) - x2):
                x1 = x1 - 1
            else:
                x1 = x1 + 1
    else:
        s = "x1: {}; x2: {}; y1: {}, y2: {}".format(x1, x2, y1, y2)
        raise ValueError(s)
    return (x1, y1)

def move_toward(x1, y1, x2, y2, obstacles):
    # self.rect = self.rect.move(dx * constants.TILESIZE, dy * constants.TILESIZE)
    old_x = x1
    old_y = y1
    if x1 == x2 and y1 == y2:
        raise ValueError("They are already on the same tile!")
    # ----
    x1, y1 = _move_toward_helper(x1, y1, x2, y2)
    is_blocked = obstacle_in_the_way(x1, y1, obstacles)
    if is_blocked == True:
        return old_x, old_y
    # this_obstacle = obstacles.get_obstcle(x1, y1)
    # if this_obstacle is None:
    return x1, y1

def walk_toward(myobstacles):
    # ----
    x1, y1 = 1, 1
    x2, y2 = 4, 4
    besafe = 0
    arrived = False
    while arrived == False:
        x1, y1 = move_toward(x1, y1, x2, y2, myobstacles)
        # ----
        if x1 == x2 and y1 == y2:
            arrived = True
        else:
            arrived = False
        print("new_x, new_y: {},{}; destination_x, destiation_y: {},{}".format(x1, y1, x2, y2))
        besafe += 1
        if besafe > 1000:
            raise ValueError("Error")
    print("new_x, new_y: {},{}; destination_x, destiation_y: {},{}".format(x1, y1, x2, y2))
    return arrived


if __name__ == "__main__":
    from graphics_environment import Obstacles
    myobstacles = Obstacles("swindon", "map00")
    myobstacles.read_data()
    # ----
    x1, y1 = 1, 1
    x2, y2 = 3, 4
    new_x1, new_y1 = move_toward(x1, y1, x2, y2, myobstacles)
    print("x,y: {},{}".format(new_x1, new_y1))
    # if walk_toward(myobstacles) == True:
    #     print("Success!!!!!! :-)")
    # else:
    #     print("Try again.")
