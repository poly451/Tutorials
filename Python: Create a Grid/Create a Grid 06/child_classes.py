import random
import utils
from parent_classes import Npc
from mysprites import HandleMovingSprite
from dialogs import DialogFight
from NEW_inventory import Conversation

# -----------------------------------------------------------
#                      class GrekinNPC
# -----------------------------------------------------------

class GerekinNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)
        self.resource = "blue feather"
        self.number_of_resources = 1
        self.gold = 0

    def default_action(self, obstacles, player):
        this_item = player.inventory.get_item_by_name("wild blueberries")
        if this_item is None:
            self.move_random(obstacles)
        else:
            distance = utils.distance_between_two_points((player.x, player.y), (self.x, self.y))
            if distance >= 1.5:
                self.move_random(obstacles)
        return None, None

# -----------------------------------------------------------
#                      class QuestGiverNPC
# -----------------------------------------------------------

class QuestGiverNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)

    def default_action(self, obstacles, player):
        return None, None

# -----------------------------------------------------------
#                      class SellNPC
# -----------------------------------------------------------

class SellNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)

    def default_action(self, obstacles, player):
        return None, None

# -----------------------------------------------------------
#                      class BuyNPC
# -----------------------------------------------------------

class BuyNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)

    def default_action(self, obstacles, player):
        return None, None

# -----------------------------------------------------------
#                      class BystanderNPC
# -----------------------------------------------------------

class BystanderNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)

    def default_action(self, obstacles, player):
        return None, None

# -----------------------------------------------------------
#                      class NuisanceNPC
# -----------------------------------------------------------

class NuisanceNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)
        # self.mysprite = MySpriteNew(1, 10, 4, 10, "apple.png")
        self.move_sprite = True
        self.mysprite = HandleMovingSprite("apple.png")
        self.mysprite.read_data(begin_x=1, begin_y=8, end_x=1, end_y=1)

    def attack(self, player, obstacles):
        # move char up to the same square as the player.
        if self.move_toward_alternate(player.x, player.y, obstacles) == True:
            myint = random.randint(1, 1000)
            # print("----------------------------------")
            # print("This is myint: {}".format(myint))
            # print("this is change to hit: {}".format(self.chance_to_hit))
            # print("----------------------------------")
            if myint < self.chance_to_hit:
                player.hit_points -= 1

    def default_action(self, obstacles, player):
        A = (self.x, self.y)
        B = (player.x, player.y)
        distance_between = utils.distance_between_two_points(A, B)
        if distance_between < 5:
            self.attack(player, obstacles)
        return None, None

# -----------------------------------------------------------
#                      class PredatorNPC
# -----------------------------------------------------------

class PredatorNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)
        self.alternate_increment = 1.0
        # self.alternate_increment = 0.25
        self.hit_points = self.max_hit_points
        # self.mysprite = MySpriteNew(1, 10, 4, 10, "apple.png")
        # self.move_sprite = True
        # self.mysprite = HandleMovingSprite("apple.png")
        # self.mysprite.read_data(begin_x=1, begin_y=8, end_x=1, end_y=1)

    def attack(self, player, obstacles):
        # move char up to the same square as the player.
        if self.move_toward_alternate(player.x, player.y, obstacles) == True:
            mydialog = DialogFight(player, self)
            mydialog.main()
            # myint = random.randint(1, 100)
            # if myint < self.chance_to_hit:
            #     player.hit_points -= 1

    def default_action(self, obstacles, player):
        A = (self.x, self.y)
        B = (player.x, player.y)
        distance_between = utils.distance_between_two_points(A, B)
        if distance_between <= self.attack_distance:
            self.attack(player, obstacles)
        return None, None

# -----------------------------------------------------------
#                      class AssassinNPC
# -----------------------------------------------------------

class AssassinNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)
        self.alternate_increment = 1.0
        self.hit_points = self.max_hit_points
        # self.mysprite = MySpriteNew(1, 10, 4, 10, "apple.png")
        # self.move_sprite = True
        # self.mysprite = HandleMovingSprite("apple.png")
        # self.mysprite.read_data(begin_x=1, begin_y=8, end_x=1, end_y=1)

    def attack(self, player, obstacles):
        # move char up to the same square as the player.
        if self.move_toward_alternate(player.x, player.y, obstacles) == True:
            mydialog = DialogFight(player, self)
            mydialog.main()
            if self.is_dead() == True:
                self.image = self.image_dead
            # myint = random.randint(1, 100)
            # if myint < self.chance_to_hit:
            #     player.hit_points -= 1

    def default_action(self, obstacles, player):
        A = (self.x, self.y)
        B = (player.x, player.y)
        distance_between = utils.distance_between_two_points(A, B)
        if distance_between <= self.attack_distance:
            self.attack(player, obstacles)
        return None, None

# -----------------------------------------------------------
#                      class MercenaryNPC
# -----------------------------------------------------------

class MercenaryNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)
        # self.conversation_finished = False
        self.quest_finished = False
        self.npc_met_player = False
        self.npc_at_destination = False
        # We need to make sure that mydict contains values for the destination point.
        if utils.is_int(self.destination_point_x) == False:
            s = "This destination point should be an integer, but it is not: {}"
            s = s.format(self.destination_point_x)
            raise ValueError(s)
        if utils.is_int(self.destination_point_y) == False:
            s = "This destination point should be an integer, but it is not: {}"
            s = s.format(self.destination_point_y)
            raise ValueError(s)
        if self.destination_point_x < 0: raise ValueError("Error")
        if self.destination_point_y < 0: raise ValueError("Error")
        # ----

    def _have_conversation(self, obstacles, player):
        A = (self.x, self.y)
        B = (player.x, player.y)
        distance_between = utils.distance_between_two_points(A, B)
        if distance_between <= self.attack_distance:
            if self.move_toward(player.x, player.y, obstacles) == True:
                mydialog = Conversation(player_name=player.name,
                                        npc_name=self.name,
                                        zone_name=player.zone_name,
                                        map_name=player.map_name)
                mydialog.read_data()
                return mydialog.main()

    def default_action(self, obstacles, player):
        def npc_with_player():
            if utils.points_are_close(player.x, self.x) and utils.points_are_close(player.y, self.y):
                return True
            return False
        def npc_at_destination():
            if utils.points_are_close(self.x, self.destination_point_x) and utils.points_are_close(self.y, self.destination_point_y):
                return True
            return False
        # ---- ----
        if self.npc_met_player == False and self.npc_at_destination == False:
            if self.move_toward(x=player.x, y=player.y, obstacles=obstacles) == True:
                self.npc_met_player = True
                return self._have_conversation(obstacles=obstacles, player=player)
        elif self.npc_met_player == True and npc_at_destination() == False:
            if self.move_toward(x=self.destination_point_x,
                                y=self.destination_point_y,
                                obstacles=obstacles) == True:
                self.npc_at_destination = True
        return None, None

# -----------------------------------------------------------
#                      class TalkAndFightNPC
# -----------------------------------------------------------

class TalkAndFightNPC(Npc):
    def __init__(self, mydict):
        super().__init__(mydict)

    def default_action(self, obstacles, player):
        return None, None

