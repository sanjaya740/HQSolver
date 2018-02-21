from config import readFromConfig

from shutil import get_terminal_size

class Solver(object):
    def __init__(self):
        self.google_api_key = readFromConfig("Solver", "google_api_key")
        self.google_cse_id = readFromConfig("Solver", "google_cse_id")
        self.show_answers = readFromConfig("Solver", "show_answers")
        self.show_answerids = readFromConfig("Solver", "show_answerids")
        self.show_category = readFromConfig("Solver", "show_category")
        self.show_question = readFromConfig("Solver", "show_question")
        self.show_questionid = readFromConfig("Solver", "show_questionid")
        self.show_question_count = readFromConfig("Solver", "show_question_count")
        self.show_question_number = readFromConfig("Solver", "show_question_number")
        self.use_naive = readFromConfig("Solver", 'use_naive')

    def solve(self, message):
        self.question = message

        self.showQuestion()

        return True

    def showQuestion(self):
        print(" Question ".center(get_terminal_size()[0], "="))
        print()

        if self.show_question_count or self.show_question_number:
            tempPrint = ""
            if self.show_question_count:
                tempPrint += "Question " + str(self.question["questionNumber"])
            if self.show_question_count and self.show_question_number:
                tempPrint += "/" + str(self.question["questionCount"])
            elif self.show_question_number:
                tempPrint += "Questions: " + str(self.question["questionCount"])

            print(tempPrint.center(get_terminal_size()[0]))

        if self.show_category:
            print(("Category: " + str(self.question["category"])).rjust(get_terminal_size()[0]))
            print()

        if self.show_question or self.show_questionid:
            tempPrint = ""
            if self.show_question:
                tempPrint += str(self.question["question"])
            if self.show_questionid:
                tempPrint += str(self.question["questionId"])

            print(tempPrint.center(get_terminal_size()[0]))

        if self.show_answers or self.show_answerids:
            answers = self.question["answers"]
            answersCount = len(answers)

            for answer in range(answersCount):
                tempPrint = ""

                if self.show_answers:
                    tempPrint += str(answers[answer]["text"])
                if self.show_answers and self.show_answerids:
                    tempPrint += " " + str(answers[answer]["answerId"])
                elif self.show_answerids:
                    tempPrint += str(answers[answer]["answerId"])

                print()
                print(tempPrint.center(get_terminal_size()[0]))

        return True
