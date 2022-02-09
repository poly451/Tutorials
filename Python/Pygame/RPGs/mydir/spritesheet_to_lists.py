import utils
import pygame
import constants
import sys, os
from dialogs import DialogInput_New, DialogText
# -------------------------------------------------------------
#                class SpriteSheet_to_Lists
# -------------------------------------------------------------
class SpriteSheet_to_Lists:
    def __init__(self, image_model, sheet_kind, list_or_spritesheet):
        models = utils.get_all_possible_model_names()
        if image_model not in models:
            s = "I don't recognize this model name: {}\n".format(image_model)
            s += "Here are the available models: {}".format(models)
            raise ValueError(s)
        self.image_model = image_model
        if sheet_kind not in constants.SHEET_KINDS:
            s = "I don't recognize this sheet_kind: {}".format(sheet_kind)
            raise ValueError(s)
        self.sheet_kind = sheet_kind
        if list_or_spritesheet not in constants.LIST_OR_SPRITESHEET:
            s = "This is the value of list_or_spritesheet: {}".format(list_or_spritesheet)
            raise ValueError(s)
        self.list_or_spritesheet = list_or_spritesheet
        # ----
        self.init_pygame()
        # ----
        self.player_character = PlayerCharacter_SpriteSheet(self.image_model, self.sheet_kind)
        self.health_meter = HealthMeter(self.player_character.x, self.player_character.y, 100)
        self.keep_looping = True
        self.image_counter = 0
        self.user_text = ""
        self.display_text = ""
        self.all_models = ", ".join(utils.get_all_possible_model_names())
        # ----
        self.images = None

    def read_data(self):
        self.player_character.read_data()

    def init_pygame(self):
        pygame.init()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Spritesheets')
        self.clock = pygame.time.Clock()

    # def create_character(self, model_name, sheet_kind):
    #     if model_name not in utils.get_all_possible_model_names(): raise ValueError("Error")
    #     if sheet_kind not in constants.SHEET_KINDS:
    #         s = "I don't understand this:\n".format(sheet_kind)
    #         s += "model_name: {}\n".format(model_name)
    #         s += "sheet_kind: {}\n".format(sheet_kind)
    #         s += "--------------\n"
    #         s += "{}\n".format(", ".join(utils.get_all_possible_model_names()))
    #         s += "{}\n".format(", ".join(constants.SHEET_KINDS))
    #         raise ValueError(s)
    #     # ---- -----
    #     sprite_sheet = SpriteSheetMaster(model_name, sheet_kind)
    #     sprite_sheet.read_data()
    #     print("model ({}) has been loaded.".format(model_name))
    #     sprite_sheet.save_images_to_file()

    # def reload(self, model_name):
    #     self.image_model = model_name
    #     self.player_character = PlayerCharacter(self.image_model, self.sheet_kind, self.list_or_spritesheet)
    #     self.player_character.read_data()
    #     print("model ({}) has been loaded.".format(model_name))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_UP:
                    self.player_character.change_direction("back")
                elif event.key == pygame.K_DOWN:
                    self.player_character.change_direction("front")
                elif event.key == pygame.K_RIGHT:
                    self.player_character.change_direction("right")
                elif event.key == pygame.K_LEFT:
                    self.player_character.change_direction("left")
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                # =======================================
                elif event.key == pygame.K_RETURN:
                    self.display_text = self.user_text
                    self.user_text = ""
                    # ----
                    self._process_choice(self.display_text)
                elif event.key == pygame.KMOD_SHIFT:
                    print("KMOD_SHIFT")
                else:
                    self.user_text += event.unicode

    def _process_choice(self, choice):
        # processing the input: choice
        mylist = choice.split(" ")
        mylist = [i.strip() for i in mylist if len(i.strip()) > 0]
        if len(mylist) != 2:
            if mylist[0] == "save":
                raise ValueError("I need to know which MODEL needs to be saved.")
            else:
                s = "There needs to be at least two terms: a command and a value."
                raise ValueError(s)
        command, data = mylist[0], mylist[1]
        if command not in constants.COMMANDS:
            s = "I do not recognize this: {}".format(command)
            raise ValueError(s)
        if data not in constants.DATA_VALUES:
            if data not in utils.get_all_possible_model_names():
                s = "I don't understand this: {}\n".format(data)
                s += "Possible values (I won't print out all the model names.):\n"
                s += ", ".join(constants.DATA_VALUES)
                raise ValueError(s)
        # ---- ----
        if command == "monster":
            print("Checking to see if {} is a proper monster name.".format(choice))
            if data in utils.get_all_possible_model_names():
                print("{} is a proper player name".format(self.display_text))
                self.reload(data)
                self.display_text = ""
                return True
            else: return False
        # ---- ----
        elif command == "health":
            if utils.is_int(data) == True:
                if int(data) > self.player_character.max_health: raise ValueError("Error")
                self.player_character.current_health = int(data)
                print("The monsters health has been reduced by {}".format(data))
                return True
        # ---- ----
        elif command == "sheet":
            # choices = ["walk", "thrust", "spell", "slash", "bow", "fall", "idle", "save"]
            if data not in constants.SHEET_KINDS: raise ValueError("Error")
            if data == "walk":
                self.player_character.change_movement("walk")
            elif data == "thrust":
                self.player_character.change_movement("thrust")
            elif data == "spell":
                self.player_character.change_movement("spell")
            elif data == "slash":
                self.player_character.change_movement("slash")
            elif data == "bow":
                self.player_character.change_movement("bow")
            elif data == "fall":
                self.player_character.change_movement("fall")
            elif data == "idle":
                self.player_character.change_movement("idle")
            elif data == "save":
                self.player_character.save_images_to_file()
            else:
                s = "I don't recognize this: {}".format(choice)
                raise ValueError(s)
        elif command == "load":
            model_name_to_load = data
            self.create_character(model_name_to_load, self.sheet_kind)
            # self.reload(model_name_to_load)
        elif command == "save":
            self.player_character.save_images_to_file()
        else:
            s = "I don't recognize this: {}".format(command)
            raise ValueError(s)

    def draw(self):
        self.all_sprites = pygame.sprite.Group()
        self.screen.fill(constants.BG_COLOR)
        # ---- ----
        mylists = [self.all_models]
        mylists.append("walk, thrust, spell, slash, bow, fall, idle, save")
        utils.talk_dialog(self.screen, mylists, self.font, width_offset=20, height_offset=20, line_length=60,
                          color=constants.BLACK)
        # ----
        mylists = ["COMMANDS: {}".format(constants.COMMANDS)]
        mylists.append("SHEET_KINDS: {}".format(constants.SHEET_KINDS))
        utils.talk_dialog(self.screen, mylists, self.font, width_offset=600, height_offset=20, line_length=60,
                          color=constants.BLACK)
        # ----
        example_command = "EXAMPLE COMMANND: save base"
        utils.talk_dialog(self.screen, [example_command], self.font,
                          width_offset=20,
                          height_offset=200,
                          line_length=60,
                          color=constants.BLACK)
        # ----
        # print("display text: {}".format(self.display_text))
        myheight = constants.SCREEN_HEIGHT - constants.TILESIZE
        utils.talk_dialog(self.screen, [self.user_text], self.font, width_offset=20, height_offset=myheight , line_length=60,
                          color=constants.BLACK)
        # ----
        self.health_meter.update_classes(self.player_character.x, self.player_character.y,
                                         self.player_character.current_health)
        self.all_sprites.add(self.health_meter)
        # ---- ----
        self.player_character.update_class()
        self.all_sprites.add(self.player_character)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        # ---- ----

    def goodbye(self):
        pygame.quit()
        sys.exit()

    def main(self):
        while self.keep_looping == True:
            self.clock.tick(10)
            self.handle_events()
            self.draw()
        self.goodbye()

# -------------------------------------------------------------
#                        class PlayerCharacter_SpriteSheet
# -------------------------------------------------------------

class PlayerCharacter_SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, model_name, sheet_kind):
        super().__init__()
        if model_name not in utils.get_all_possible_model_names():
            s = "I don't recognize this model name: {}".format(model_name)
            raise ValueError(s)
        if sheet_kind not in constants.SHEET_KINDS:
            raise ValueError("Error")
        # ----
        self.x, self.y = 5, 4
        # ----
        self.init_pygame()
        self.image_lists_the = SpriteSheetMaster(model_name, sheet_kind)
        # ----
        self.max_health = 100
        self.current_health = self.max_health
        # ----
        self.image_counter = 0
        self.image = None
        self.rect = None
        self.movement = "spell"
        self.direction = "front"
        # ----
        self.image_list = []

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Spritesheets')
        self.clock = pygame.time.Clock()

    def read_data(self):
        self.image_lists_the.read_data()
        # the line below sets the first animation to play
        self.image_list = self.image_lists_the.spellcast_front

    def change_direction(self, new_direction):
        self.image_counter = 0
        self.direction = new_direction
        self.image_list = self.image_lists_the.get_list(self.movement, self.direction)

    def change_movement(self, movement):
        self.image_counter = 0
        self.movement = movement
        self.image_list = self.image_lists_the.get_list(movement, self.direction)

    def update_class(self):
        try:
            self.image = self.image_list[self.image_counter]
        except Exception as e:
            t = "image_counter: {}".format(self.image_counter)
            s = "{}\n{}".format(e, t)
        self.image = pygame.transform.scale(self.image, (constants.TILESIZE * 2, constants.TILESIZE * 2))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
        self.image_counter += 1
        if self.image_counter >= len(self.image_list):
            if self.movement == "fall":
                self.image_list = self.image_lists_the.unconscious
            self.image_counter = 0
        # ----

    def save_images_to_file(self):
        self.image_lists_the.save_images_to_file()

# -------------------------------------------------------------
#                        class SpriteSheetMaster
# -------------------------------------------------------------
class SpriteSheetMaster:
    def __init__(self, model_name, sheet_kind):
        if model_name not in utils.get_all_possible_model_names():
            s = "I don't recognize this model name: {}".format(model_name)
            raise ValueError(s)
        self.model_name = model_name
        if sheet_kind not in constants.SHEET_KINDS:
            raise ValueError("Error")
        self.sheet_kind = sheet_kind
        # --
        filename = "{}_{}.png".format(self.model_name, sheet_kind)
        filepath = os.path.join(constants.IMAGES, "animations", "lpc", self.model_name, "spritesheets", filename)
        # --
        if os.path.isfile(filepath) == False:
            s = "I don't recognize this DIRECTORY path: --{}--".format(filepath)
            raise ValueError(s)
        # ----
        self.sheet = pygame.image.load(filepath).convert_alpha()
        self.myinc = 64
        self.width, self.height = 64, 64
        self.spellcast_back = []
        self.spellcast_left = []
        self.spellcast_front = []
        self.spellcast_right = []
        # ----
        self.thrust_back = []
        self.thrust_left = []
        self.thrust_front = []
        self.thrust_right = []
        # ----
        self.walk_back = []
        self.walk_left = []
        self.walk_front = []
        self.walk_right = []
        # ----
        self.slash_back = []
        self.slash_left = []
        self.slash_front = []
        self.slash_right = []
        # ----
        self.bow_back = []
        self.bow_left = []
        self.bow_front = []
        self.bow_right = []
        # ----
        self.fall = []
        self.unconscious = []
        # ---- ----
        self.idle_back = []
        self.idle_left = []
        self.idle_front = []
        self.idle_right = []

    def get_image(self):
        width, height = 64, 64
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (-192, 0))
        return image

    def get_list(self, kind, direction):
        if kind == "spell":
            if direction == "back": return self.spellcast_back
            elif direction == "left": return self.spellcast_left
            elif direction == "front": return self.spellcast_front
            elif direction == "right": return self.spellcast_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        elif kind == "thrust":
            if direction == "back": return self.thrust_back
            elif direction == "left": return self.thrust_left
            elif direction == "front": return self.thrust_front
            elif direction == "right": return self.thrust_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        elif kind == "walk":
            if direction == "back": return self.walk_back
            elif direction == "left": return self.walk_left
            elif direction == "front": return self.walk_front
            elif direction == "right": return self.walk_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        elif kind == "slash":
            if direction == "back": return self.slash_back
            elif direction == "left": return self.slash_left
            elif direction == "front": return self.slash_front
            elif direction == "right": return self.slash_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        elif kind == "bow":
            if direction == "back": return self.bow_back
            elif direction == "left": return self.bow_left
            elif direction == "front": return self.bow_front
            elif direction == "right": return self.bow_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        elif kind == "fall":
            return self.fall
        elif kind == "idle":
            if direction == "back": return self.idle_back
            elif direction == "left": return self.idle_left
            elif direction == "front": return self.idle_front
            elif direction == "right": return self.idle_right
            else:
                s = "I don't recognize this direction: {}".format(direction)
                raise ValueError(s)
        else:
            raise ValueError("Error")

    def read_data(self):
        self.spellcast_back = self.cast_motion(7, "back")
        self.spellcast_left = self.cast_motion(7, "left")
        self.spellcast_front = self.cast_motion(7, "front")
        self.spellcast_right = self.cast_motion(7, "right")
        # ----
        self.thrust_back = self.thrust_motion(8, "back")
        self.thrust_left = self.thrust_motion(8, "left")
        self.thrust_front = self.thrust_motion(8, "front")
        self.thrust_right = self.thrust_motion(8, "right")
        # ----
        self.walk_back = self.walk_motion(9, "back")
        self.walk_left = self.walk_motion(9, "left")
        self.walk_front = self.walk_motion(9, "front")
        self.walk_right = self.walk_motion(9, "right")
        # ----
        self.slash_back = self.slash_motion(6, "back")
        self.slash_left = self.slash_motion(6, "left")
        self.slash_front = self.slash_motion(6, "front")
        self.slash_right = self.slash_motion(6, "right")
        # ----
        self.bow_back = self.bow_motion(13, "back")
        self.bow_left = self.bow_motion(13, "left")
        self.bow_front = self.bow_motion(13, "front")
        self.bow_right = self.bow_motion(13, "right")
        # ----
        self.fall = self.fall_motion(6)
        self.unconscious = self.unconscious_motion()
        # ---- ----
        self.idle_back = self.idle_motion("back")
        self.idle_left = self.idle_motion("left")
        self.idle_front = self.idle_motion("front")
        self.idle_right = self.idle_motion("right")

    def cast_motion(self, images_in_sequence, direction):
        myimages = []
        # ----
        if direction == "back":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 0 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "left":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 1 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "front":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 2 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "right":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 3 * self.myinc * -1))
                myimages.append(image)
            return myimages
        else:
            s = "I don't recognize this: {}".format(direction)
            raise ValueError(s)

    def thrust_motion(self, images_in_sequence, direction):
        myimages = []
        # ----
        if direction == "back":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 4 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "left":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 5 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "front":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 6 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "right":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 7 * self.myinc * -1))
                myimages.append(image)
            return myimages
        else:
            s = "I don't recognize this: {}".format(direction)
            raise ValueError(s)

    def walk_motion(self, images_in_sequence, direction):
        myimages = []
        # ----
        if direction == "back":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 8 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "left":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 9 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "front":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 10 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "right":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 11 * self.myinc * -1))
                myimages.append(image)
            return myimages
        else:
            s = "I don't recognize this: {}".format(direction)
            raise ValueError(s)

    def slash_motion(self, images_in_sequence, direction):
        myimages = []
        # ----
        if direction == "back":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 12 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "left":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 13 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "front":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 14 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "right":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 15 * self.myinc * -1))
                myimages.append(image)
            return myimages
        else:
            s = "I don't recognize this: {}".format(direction)
            raise ValueError(s)

    def bow_motion(self, images_in_sequence, direction):
        myimages = []
        # ----
        if direction == "back":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 16 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "left":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 17 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "front":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 18 * self.myinc * -1))
                myimages.append(image)
            return myimages
        elif direction == "right":
            x = 64 * 1
            for i in range(images_in_sequence):
                image = pygame.Surface((self.width, self.height)).convert_alpha()
                image.blit(self.sheet, (x * i * -1, 19 * self.myinc * -1))
                myimages.append(image)
            return myimages
        else:
            s = "I don't recognize this: {}".format(direction)
            raise ValueError(s)

    def fall_motion(self, images_in_sequence):
        myimages = []
        x = 64 * 1
        for i in range(images_in_sequence):
            image = pygame.Surface((self.width, self.height)).convert_alpha()
            image.blit(self.sheet, (x * i * -1, 20 * self.myinc * -1))
            myimages.append(image)
        return myimages

    def unconscious_motion(self):
        myimage = self.fall[5]
        return [myimage, myimage, myimage, myimage, myimage, myimage]

    def idle_motion(self, direction):
        if direction not in constants.DIRECTION_VALUES: raise ValueError("Error")
        # ---- ----
        idle01, idle02 = None, None
        if direction == "back":
            idle01, idle02 = self.walk_back[0], self.walk_back[1]
        elif direction == "front":
            idle01, idle02 = self.walk_front[0], self.walk_front[1]
        elif direction == "left":
            idle01, idle02 = self.walk_left[0], self.walk_left[8]
        elif direction == "right":
            idle01, idle02 = self.walk_right[0], self.walk_right[8]
        else:
            raise ValueError("Error")
        myimages = [idle01, idle01, idle01, idle01, idle01, idle01, idle01, idle01]
        myimages += [idle02, idle02, idle02, idle02, idle02, idle02, idle02, idle02, idle02, idle02]
        return myimages

    # ----------------------------------------------------------

    def _save_images(self, image_list, root_directory, kind, direction):
        filepath = os.path.join(root_directory, kind, direction)
        for count, elem in enumerate(image_list):
            filename = "{}_{}_{}.png".format(kind, direction, count)
            temp = os.path.join(filepath, filename)
            pygame.image.save(elem, temp)

    def _save_image_list(self, image_list, root_directory, kind):
        if kind not in constants.MOVEMENT_VALUES: raise ValueError("Error")
        filepath = os.path.join(root_directory, kind)
        for count, elem in enumerate(image_list):
            filename = "{}_{}.png".format(kind, count)
            temp = os.path.join(filepath, filename)
            pygame.image.save(elem, temp)

    def _check_for_existence_of_directories(self, model_name):
        def helper(the_directory, kind):
            for a_dir in constants.DIRECTION_VALUES:
                os.mkdir(os.path.join(the_directory, kind, a_dir))
        # ---- ---- ---- ----
        root_directory = os.path.join("data", "images", "characters", model_name, "lists")
        if os.path.isdir(root_directory) == True: return True
        # ---- ----
        os.mkdir(root_directory)
        the_directory = os.path.join(root_directory, model_name)
        # ----
        os.mkdir(os.path.join(the_directory, "spell"))
        os.mkdir(os.path.join(the_directory, "thrust"))
        os.mkdir(os.path.join(the_directory, "walk"))
        os.mkdir(os.path.join(the_directory, "slash"))
        os.mkdir(os.path.join(the_directory, "bow"))
        os.mkdir(os.path.join(the_directory, "fall"))
        # ---- ----
        helper(the_directory, "spell")
        helper(the_directory, "thrust")
        helper(the_directory, "walk")
        helper(the_directory, "slash")
        helper(the_directory, "bow")
        # Since FALL doesn't have bac, left, front, right we
        # don't need to do anything else.
        return True

    def _save_files(self, path):
        os.mkdir(os.path.join(path, "spell"))
        os.mkdir(os.path.join(path, "spell", "back"))
        os.mkdir(os.path.join(path, "spell", "left"))
        os.mkdir(os.path.join(path, "spell", "front"))
        os.mkdir(os.path.join(path, "spell", "right"))
        # ----
        os.mkdir(os.path.join(path, "thrust"))
        os.mkdir(os.path.join(path, "thrust", "back"))
        os.mkdir(os.path.join(path, "thrust", "left"))
        os.mkdir(os.path.join(path, "thrust", "front"))
        os.mkdir(os.path.join(path, "thrust", "right"))
        # ----
        os.mkdir(os.path.join(path, "walk"))
        os.mkdir(os.path.join(path, "walk", "back"))
        os.mkdir(os.path.join(path, "walk", "left"))
        os.mkdir(os.path.join(path, "walk", "front"))
        os.mkdir(os.path.join(path, "walk", "right"))
        # ----
        os.mkdir(os.path.join(path, "slash"))
        os.mkdir(os.path.join(path, "slash", "back"))
        os.mkdir(os.path.join(path, "slash", "left"))
        os.mkdir(os.path.join(path, "slash", "front"))
        os.mkdir(os.path.join(path, "slash", "right"))
        # ----
        os.mkdir(os.path.join(path, "bow"))
        os.mkdir(os.path.join(path, "bow", "back"))
        os.mkdir(os.path.join(path, "bow", "left"))
        os.mkdir(os.path.join(path, "bow", "front"))
        os.mkdir(os.path.join(path, "bow", "right"))
        # ----
        os.mkdir(os.path.join(path, "idle"))
        os.mkdir(os.path.join(path, "idle", "back"))
        os.mkdir(os.path.join(path, "idle", "left"))
        os.mkdir(os.path.join(path, "idle", "front"))
        os.mkdir(os.path.join(path, "idle", "right"))
        # ----
        os.mkdir(os.path.join(path, "fall"))
        os.mkdir(os.path.join(path, "unconscious"))
        # ---- ----
        self._save_images(self.spellcast_back, path, "spell", "back")
        self._save_images(self.spellcast_left, path, "spell", "left")
        self._save_images(self.spellcast_front, path, "spell", "front")
        self._save_images(self.spellcast_right, path, "spell", "right")
        # ----
        self._save_images(self.thrust_back, path, "thrust", "back")
        self._save_images(self.thrust_left, path, "thrust", "left")
        self._save_images(self.thrust_front, path, "thrust", "front")
        self._save_images(self.thrust_right, path, "thrust", "right")
        # ----
        self._save_images(self.walk_back, path, "walk", "back")
        self._save_images(self.walk_left, path, "walk", "left")
        self._save_images(self.walk_front, path, "walk", "front")
        self._save_images(self.walk_right, path, "walk", "right")
        # ----
        self._save_images(self.slash_back, path, "slash", "back")
        self._save_images(self.slash_left, path, "slash", "left")
        self._save_images(self.slash_front, path, "slash", "front")
        self._save_images(self.slash_right, path, "slash", "right")
        # ----
        self._save_images(self.bow_back, path, "bow", "back")
        self._save_images(self.bow_left, path, "bow", "left")
        self._save_images(self.bow_front, path, "bow", "front")
        self._save_images(self.bow_right, path, "bow", "right")
        # ----
        self._save_images(self.idle_back, path, "idle", "back")
        self._save_images(self.idle_left, path, "idle", "left")
        self._save_images(self.idle_front, path, "idle", "front")
        self._save_images(self.idle_right, path, "idle", "right")
        # ----
        self._save_image_list(self.fall, path, "fall")
        self._save_image_list(self.unconscious, path, "unconscious")

    def save_images_to_file(self):
        base_path = os.path.join(constants.IMAGES, "animations", "lpc", self.model_name, "lists")
        if os.path.isdir(base_path) == False:
            os.mkdir(base_path)
        # ----
        base_path = os.path.join("data", "images", "characters", self.model_name, "lists", self.sheet_kind)
        if os.path.isdir(base_path) == True:
            s = "Doh! I can't delete a directory that isn't empty. This directory is NOT empty:\n"
            s += "{}\n".format(base_path)
            s += "You might want to delete it and try again.\n"
            raise ValueError(s)
        # ----
        # create directories
        base_path = os.path.join(constants.IMAGES, "animations", "lpc", self.model_name, "lists", self.sheet_kind)
        if os.path.isdir(base_path) == True:
            dialog_list = ["That path already exists:"]
            dialog_list.append(" ")
            dialog_list.append(os.path.join(self.model_name, "lists", self.sheet_kind))
            dialog_list.append(" ")
            dialog_list.append("Save operation cancelled.")
            mydialog = DialogText(dialog_list)
            mydialog.main()
        elif os.path.isdir(base_path) == False:
            os.mkdir(base_path)
            self._save_files(base_path)
        # ---- ----
        # root_directory = os.path.join("data", "images", "characters", self.model_name, "lists")
        # if self.sheet_kind == "base":
        # 	base_directory = os.path.join(root_directory, "base")
        # 	self._save_files(base_directory)
        # elif self.sheet_kind == "sword":
        # 	sword_directory = os.path.join(root_directory, "sword")
        # 	self._save_files(sword_directory)
        # else:
        # 	raise ValueError("Error")

# -----------------------------------------------------------
#                      class HealthMeter
# -----------------------------------------------------------
class HealthMeter(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health):
        super().__init__()
        self.empty_tile = "empty.png"
        self.keep_looping = True
        self.x, self.y = x, y
        self.max_health = max_health
        self.image_95 = None
        self.image_75 = None
        self.image_50 = None
        self.image_25 = None
        self.image_5 = None
        self.image_1 = None
        self.image_0 = None
        self.empty = None
        # ----
        self.image = None
        self.rect = None
        # ----
        self.read_data(x, y)

    def read_data(self, x, y):
        # filedir = os.path.join("data", "images", "health")
        filedir = os.path.join(constants.IMAGES, "health")
        self.image_95 = pygame.image.load(os.path.join(filedir, "health_95.png")).convert_alpha()
        self.image_75 = pygame.image.load(os.path.join(filedir, "health_75.png")).convert_alpha()
        self.image_50 = pygame.image.load(os.path.join(filedir, "health_50.png")).convert_alpha()
        self.image_25 = pygame.image.load(os.path.join(filedir, "health_25.png")).convert_alpha()
        self.image_5 = pygame.image.load(os.path.join(filedir, "health_5.png")).convert_alpha()
        self.image_1 = pygame.image.load(os.path.join(filedir, "health_1.png")).convert_alpha()
        self.image_0 = pygame.image.load(os.path.join(filedir, "health_0.png")).convert_alpha()
        # ----
        self.image_95 = pygame.transform.scale(self.image_95, (constants.TILESIZE, constants.TILESIZE))
        self.image_75 = pygame.transform.scale(self.image_75, (constants.TILESIZE, constants.TILESIZE))
        self.image_50 = pygame.transform.scale(self.image_50, (constants.TILESIZE, constants.TILESIZE))
        self.image_25 = pygame.transform.scale(self.image_25, (constants.TILESIZE, constants.TILESIZE))
        self.image_5 = pygame.transform.scale(self.image_5, (constants.TILESIZE, constants.TILESIZE))
        self.image_1 = pygame.transform.scale(self.image_1, (constants.TILESIZE, constants.TILESIZE))
        self.image_0 = pygame.transform.scale(self.image_0, (constants.TILESIZE, constants.TILESIZE))
        # ----
        filepath = os.path.join(constants.IMAGES, "empty.png")
        self.empty = pygame.image.load(filepath).convert_alpha()
        self.empty = pygame.transform.scale(self.empty, (constants.TILESIZE, constants.TILESIZE))
        # ----
        # set current image
        self.image = self.empty
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)


    # --------------------------------------------------------------

	# in class SpecialEffects
    def update_classes(self, x, y, current_health):
        if self.max_health == current_health:
            self.image = self.empty
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)
            return True
        # ----
        percent = utils.get_percent(current_health, self.max_health)
        if percent < 100 and percent >= 95:
            self.image = self.image_95
        elif percent < 95 and percent >= 75:
            self.image = self.image_75
        elif percent < 75 and percent >= 50:
            self.image = self.image_50
        elif percent < 50 and percent >= 25:
            self.image = self.image_25
        elif percent < 25 and percent >= 5:
            self.image = self.image_5
        elif percent < 5 and percent >= 1:
            self.image = self.image_1
        elif percent == 0:
            self.image = self.image_0
        else:
            raise ValueError("Error")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)

# *******************************************************
# *******************************************************

def main():
    choices = utils.get_all_possible_model_names()
    display_list = ["{}) {}".format(count+1, i) for count, i in enumerate(choices)]
    possible_choices = list(range(1, len(choices)+1))
    mydialog = DialogInput_New(display_list, possible_choices,
                               width=constants.SCREEN_WIDTH,
                               height=constants.SCREEN_HEIGHT)
    user_choice = mydialog.main()
    user_index = int(user_choice)-1
    character_model = choices[user_index]
    # ---- ----
    myclass = SpriteSheet_to_Lists(character_model, "base", "spritesheet")
    myclass.read_data()
    myclass.main()

if __name__ == "__main__":
    myclass = SpriteSheet_to_Lists("bandit", "base", "spritesheet")
    myclass.read_data()
    myclass.main()