import sys, os
import pygame
import utils
import constants
from myclasses import FlashCards
from dialogs import DialogInput, TransitionScreen, QuizDialogInput
# ------------------------------------------------------------
#                    class DialogQuiz
# ------------------------------------------------------------
class DialogQuiz:
    def __init__(self, user_name, quiz_name, percent_threshold=None, width=600, height=600, line_width=40):
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.percent_threshold = percent_threshold
        # ---- ---- ---- ----
        self.flashcards = None
        self.current_index = 1
        # --------------------------------------
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_text_color = constants.UGLY_PINK
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True
        self.x = self.user_rect.x + 10
        self.y = self.user_rect.y

    def read_data(self):
        self.flashcards = FlashCards(self.user_name, self.quiz_name, self.percent_threshold)
        was_successful = self.flashcards.read_data()
        if was_successful not in [True, False]: raise ValueError("Error")
        if was_successful == False:
            return False
        # ---- ----
        self.current_index = 1
        self.display_list = self.flashcards.display_question()
        # ----
        self.choices = ["1", "2", "3", "<SPACE>"]
        s = ", ".join(self.choices)
        self.display_choices = "Choices: {}".format(s)
        return True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def reload(self):
        self.flashcards = FlashCards(self.user_name, self.quiz_name, self.percent_threshold)
        self.flashcards.read_data()
        self.current_index = 1
        self.display_list = self.flashcards.display_question()
        # ----
        self.choices = ["1", "2", "3", "<SPACE>"]
        s = ", ".join(self.choices)
        self.display_choices = "Choices: {}".format(s)

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.user_rect = pygame.Rect(10,
                                     self.height - offset,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        self.user_rect2 = pygame.Rect(10,
                                     self.height - offset - 540,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height + 30)
        self.user_rect3 = pygame.Rect(10,
                                     self.height - offset - 465,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.text = self.user_text.lower().strip()
                    if not self.text in self.choices:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.display_list, is_correct = self.flashcards.calculate_result(self.text)
                    if is_correct == True:
                        self.BG_COLOR = constants.GREEN1
                    else:
                        self.BG_COLOR = constants.RED1
                    self.text = ""
                    self.user_text = ""
                elif event.key == pygame.K_SPACE:
                    if event.key == pygame.K_n:
                        self.user_text += event.unicode
                    # ----
                    if self.flashcards.answer_was_given() == False:
                        mytext = ["No answer has been given!"]
                        mytext.append(" ")
                        mytext.append("Press <Return> to continue...")
                        mydialog = DialogInput(mytext, [], show_possible_responses=False)
                        mydialog.main()
                        return False
                    # ---- ----
                    self.BG_COLOR = constants.WHITE
                    question_set = self.flashcards.load_next_question()
                    if question_set == False:
                        mytext = []
                        mytext.append(self.flashcards.get_score())
                        mytext.append(" ")
                        mytext.append("Would you like to take the quiz again?")
                        mydialogs = QuizDialogInput(mytext, ["y", "n"])
                        message = mydialogs.main()
                        if message == "y":
                            self.flashcards.save_data()
                            self.reload()
                        elif message == "n":
                            self.flashcards.save_data()
                            self.keep_looping = False
                        else:
                            raise ValueError("Error")
                    elif question_set == True:
                        self.display_list = self.flashcards.display_question()
                    else:
                        raise ValueError("Error")
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        if self.keep_looping == True:
            # -----------------------------------------
            pygame.draw.rect(self.screen, constants.GREY5, self.user_rect2)
            pygame.draw.rect(self.screen, constants.GREY6, self.user_rect3)
            # -----------------------------------------
            utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                              height_offset=20, line_length=60,
                              color=constants.BLACK)
            # -----------------------------------------
            pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            if len(self.choices) != 0:
                utils.talk_dialog(self.screen, self.display_choices, self.font,
                                  width_offset=self.x, height_offset=self.y-40,
                                  line_length=60,
                                  color=constants.BLACK)
            utils.talk_dialog(self.screen, self.user_text, self.font,
                              width_offset=self.x, height_offset=self.y,
                              line_length=60,
                              color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()

# *********************************************
# *********************************************

def main(user_name, quiz_name):
    percent_threshold = 90
    mydialog = DialogQuiz(user_name, quiz_name, percent_threshold)
    was_successful = mydialog.read_data()
    if was_successful == False:
        pass
    else:
        mydialog.main()

if __name__ == "__main__":
    user_name = "chris"
    # quiz_name = "testing01"
    quiz_name = "countries_and_capitals"
    main(user_name, quiz_name)