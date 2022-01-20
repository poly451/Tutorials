import sys, os
import utils
from dialogs import DialogInput
# ------------------------------------------------------------
#                    class UserScore
# ------------------------------------------------------------
class UserScore:
    def __init__(self, mydict):
        # print("mydict: {}".format(mydict))
        self.question_index = int(mydict["question_index"])
        self.times_question_correct = int(mydict["times_question_correct"])
        self.times_question_presented = int(mydict["times_question_presented"])

    def get_score(self):
        if self.times_question_presented == 0: return 0.0
        percent = (self.times_question_correct * 100) / self.times_question_presented
        return round(percent, 1)

    def update_score(self, question_record):
        if question_record.user_response is None: return False
        if utils.is_int(question_record.user_response) == False:
            s = "This is wrong: {} | {}".format(question_record.user_response, type(question_record.user_response))
            raise ValueError(s)
        if utils.is_int(question_record.answer) == False: raise ValueError("Error")
        user_response = int(question_record.user_response)
        answer = int(question_record.answer)
        if user_response == answer:
            self.times_question_correct += 1
        self.times_question_presented += 1

    def fileline(self, user_name, quiz_name):
        s = "user_name: {}\n".format(user_name)
        s += "quiz_name: {}\n".format(quiz_name)
        s += "question_index: {}\n".format(self.question_index)
        s += "times_question_correct: {}\n".format(self.times_question_correct)
        s += "times_question_presented: {}\n\n".format(self.times_question_presented)
        return s

    def debug_print(self, user_name, quiz_name):
        s = "user_name: {}, ".format(user_name)
        s += "quiz_name: {}, ".format(quiz_name)
        s += "question_index: {}, ".format(self.question_index)
        s += "times_question_correct: {}, ".format(self.times_question_correct)
        s += "times_question_presented: {}".format(self.times_question_correct)
        print(s)

# ------------------------------------------------------------
#                    class UserScores
# ------------------------------------------------------------
class UserScores:
    def __init__(self, user_name, quiz_name):
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.inner = []

    def get_element(self, index):
        return self.inner[index]

    def get_score(self, index):
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        for elem in self.inner:
            # s = "{} ({}) | {} ({})".format(elem.question_index, type(elem.question_index), index, type(index))
            # print(s)
            if elem.question_index == index:
                the_score = elem.get_score()
                # print("entered!!! {} -- {} ({})".format(elem.question_index, index, the_score))
                # print("*******************")
                return the_score
        print("index {} not found!".format(index))
        return None

    def read_data(self):
        filename = "{}.txt".format(self.quiz_name)
        filepath = os.path.join("data", "users", self.user_name, "scores", filename)
        if os.path.isfile(filepath) == False:
            s = "I don't recognize this: {}".format(filepath)
            raise ValueError(s)
        # ---- ----
        mylist = utils.read_data_file(filepath, 5)
        if mylist is None: raise ValueError("Error")
        if len(mylist) == 0: raise ValueError("Error")
        for mydict in mylist:
            newobject = UserScore(mydict)
            self.inner.append(newobject)

    def save_data(self):
        filename = "{}.txt".format(self.quiz_name)
        filepath = os.path.join("data", "users", self.user_name, "scores", filename)
        if os.path.isfile(filepath) == False:
            s = "I don't recognize this: {}".format(filepath)
            raise ValueError(s)
        # ---- ----
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        # DEBUGGING !!!!!!
        # filepath = os.path.join("data", "testing.txt")
        with open(filepath, "w") as f:
            for elem in self.inner:
                s = elem.fileline(self.user_name, self.quiz_name)
                if len(s) == 0: raise ValueError("Error!")
                f.write("{}".format(s))

    def update_score(self, question):
        for elem in self.inner:
            if elem.question_index == question.index:
                try:
                    elem.update_score(question)
                except Exception as e:
                    t = "question.index: {}\n".format(question.index)
                    t += "elem.question_index: {}\n".format(elem.question_index)
                    t += "elem (type): {}\n".format(type(elem))
                    t += "--> fileline: {}<--\n".format(elem.fileline(self.user_name, self.quiz_name))
                    s = "{}\n{}\n".format(e, t)
                    raise ValueError(s)
                return True
        return False

    def get_score_across_questions(self):
        mylist = ["All scores for quiz:"]
        mylist.append("{}".format(self.quiz_name.upper()))
        mylist.append(" ")
        for elem in self.inner:
            if elem.times_question_presented == 0:
                s = "index: {} -- 0 / 0 || --%".format(elem.question_index,
                                                         elem.times_question_correct,
                                                         elem.times_question_presented)
            else:
                percent = round((elem.times_question_correct) * 100 / elem.times_question_presented, 1)
                s = "index: {} -- {} / {} || {}%".format(elem.question_index,
                                      elem.times_question_correct,
                                      elem.times_question_presented,
                                      percent)
            mylist.append(s)
        mylist.append(" ")
        mylist.append("Press <Return> to continue...")
        return mylist

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print(self.user_name, self.quiz_name)

# ------------------------------------------------------------
#                    class FlashCard
# ------------------------------------------------------------
class FlashCard:
    def __init__(self, mydict):
        self.quiz_name = mydict["quiz_name"]
        self.index = int(mydict["index"])
        self.prompt = mydict["prompt"]
        self.option1 = mydict["option1"]
        self.option2 = mydict["option2"]
        self.option3 = mydict["option3"]
        self.answer = int(mydict["answer"])
        # ---- ----
        self.user_response = None

    def display_question(self):
        mylist = [self.quiz_name]
        mylist.append(" ")
        mylist.append(self.prompt)
        mylist.append("1) {}".format(self.option1))
        mylist.append("2) {}".format(self.option2))
        mylist.append("3) {}".format(self.option3))
        # mylist.append("(debugging: {})".format(str(self.answer)))
        return mylist

    def calculate_result(self, choice):
        def get_answer():
            if self.answer == 1: return self.option1
            if self.answer == 2: return self.option2
            if self.answer == 3: return self.option3
        # ---- ---- ---- ----
        self.user_response = int(choice)
        is_correct = False
        # ---- ----
        if choice in ["1", "2", "3"]:
            choice = int(choice)
            mylist = []
            if choice < 1 or choice > 3: raise ValueError("Error")
            if choice == 1:
                s = "{} (you chose) | {} (answer)".format(self.option1, get_answer())
                mylist.append(s)
            if choice == 2:
                s = "{} (you chose) | {} (answer)".format(self.option2, get_answer())
                mylist.append(s)
            if choice == 3:
                s = "{} (you chose) | {} (answer)".format(self.option3, get_answer())
                mylist.append(s)
            # ---- ----
            mylist.append(" ")
            if self.answer == choice:
                mylist.append("Correct! :-)")
                is_correct = True
            else:
                mylist.append("Incorrect")
                is_correct = False
            mylist.append("")
            mylist.append("Press <SPACE> to continue...")
            return mylist, is_correct
        else:
            raise ValueError("Error")

    def debug_print(self):
        s = "quiz_name: {}, ".format(self.quiz_name)
        s += "index: {}, ".format(self.index)
        s += "prompt: {}, ".format(self.prompt)
        s += "option1: {}, ".format(self.option1)
        s += "option2: {}, ".format(self.option2)
        s += "option3: {}, ".format(self.option3)
        s += "answer: {}, ".format(self.answer)
        s += "user_response: {}".format(self.user_response)
        print(s)

# ------------------------------------------------------------
#                    class FlashCards
# ------------------------------------------------------------

class FlashCards:
    def __init__(self, user_name, quiz_name, score_threshold):
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.score_threshold = score_threshold
        self.inner = []
        self.current_index = 0
        self.required_times_presented = 2

    def read_data(self):
        filename = "{}.txt".format(self.quiz_name)
        filepath = os.path.join("data", "quizzes", filename)
        if os.path.isfile(filepath) == False:
            s = "I can't find this file: {}".format(filepath)
            raise ValueError(s)
        mylist = utils.read_data_file(filepath, 7)
        # [print(i) for i in mylist]
        # ----
        for mydict in mylist:
            newobject = FlashCard(mydict)
            self.inner.append(newobject)
        # ----
        if not self.score_threshold is None:
            was_successful = self.filter_questions()
            if was_successful == False:
                mylist = ["There are no more questions!"]
                mylist.append(" ")
                mylist.append("You may want to change")
                mylist.append("self.score_threshold in the")
                mylist.append("flashcard class or remove it.")
                mylist.append(" ")
                mylist.append("Press <Return> to continue")
                mydialog = DialogInput(mylist, [], show_possible_responses=False)
                mydialog.main()
                return False
            else:
                return True
        return True

    def filter_questions(self):
        if self.score_threshold is None: raise ValueError("Error")
        user_scores = UserScores(self.user_name, self.quiz_name)
        user_scores.read_data()
        # ---- ----
        big_list = []
        for elem in self.inner:
            score = user_scores.get_score(elem.index)
            if score is None:
                s = "Something went wrong!"
                raise ValueError(s)
            user_score = user_scores.get_element(elem.index)
            if user_score.times_question_presented < self.required_times_presented:
                big_list.append(elem)
            elif score > self.score_threshold:
                pass
            else:
                big_list.append(elem)
        if len(big_list) == 0:
            return False
        self.inner = big_list
        return True

    def save_data(self):
        user_scores = UserScores(self.user_name, self.quiz_name)
        user_scores.read_data()
        mylist = []
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        for elem in self.inner:
            user_scores.update_score(elem)
        user_scores.save_data()

    def answer_was_given(self):
        current_question = self.inner[self.current_index]
        # current_question.debug_print()
        # raise NotImplemented
        if current_question.user_response is None: return False
        return True

    def get_current_question(self):
        if self.inner is None: raise ValueError("Error")
        if len(self.inner) == 0: raise ValueError("Error")
        return self.inner[self.current_index]

    def calculate_result(self, choice):
        current_question = self.inner[self.current_index]
        return current_question.calculate_result(choice)

    def get_score(self):
        questions_asked = 0
        correct = 0
        for a_question in self.inner:
            if a_question.user_response is None:
                pass
            else:
                questions_asked += 1
                if a_question.answer == a_question.user_response:
                    correct += 1
        if correct == 0:
            return "total: {}, correct: {}, percent: --".format(questions_asked, correct)
        else:
            percent = round((correct * 100)/questions_asked, 1)
            return "total: {}, correct: {}, percent: {}%".format(questions_asked, correct, percent)

    def display_question(self):
        this_question = self.inner[self.current_index]
        display_list = this_question.display_question()
        score = self.get_score()
        display_list.insert(0, " ")
        display_list.insert(0, score)
        return display_list

    def load_next_question(self):
        self.current_index += 1
        if self.current_index >= len(self.inner):
            return False
        return True

    def debug_print(self):
        for elem in self.inner:
            elem.debug_print()

if __name__ == "__main__":
    myclass = UserScores("chris", "testing01")
    myclass.read_data()
    myclass.s
    # myclass = FlashCards("karen", "testing01")
    # myclass.read_data()
    # myclass.debug_print()
