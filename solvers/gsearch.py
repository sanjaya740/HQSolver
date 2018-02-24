from config import negationWords, whichWords

from google import google
from shutil import get_terminal_size


class Google(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.negation = False

    def solve(self, question, answers):
        self.question = question
        self.answers = answers

        try:
            answers = self.getAnswer()
        except Exception as e:
            print(e)
            answers = [0, 0, 0]
            print("\33[33mGoogle: Warning! It seems that we have problem getting info from Google!\33[0m")

        if self.debug:
            print("Google:", answers)

        mostPropably = max(answers)
        ifNOTmostPropably = min(answers)

        if (mostPropably != 0 or ifNOTmostPropably != 0) and (answers.count(mostPropably) == 1 or answers.count(ifNOTmostPropably) == 1):

            if not self.negation:
                correct = answers.index(mostPropably)
                print((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33["
                                                                                                                "0m").center(get_terminal_size()[0], "*"))
                return correct
            else:
                correct = answers.index(ifNOTmostPropably)
                print((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33["
                                                                                                                "0m").center(get_terminal_size()[0], "*"))
                return correct

        print(" Google solver couldn't guess the answer! ".center(get_terminal_size()[0], "*"))

        return False

    def getAnswer(self):
        question = self.question.lower()
        questionWords = question.replace("?", "").split()

        answers = []
        for answer in range(len(self.answers)):
            answers.append(self.answers[answer]['text'].lower())

        for questionWord in range(len(questionWords)):
            for negWord in range(len(negationWords)):
                if negationWords[negWord] == questionWords[questionWord]:
                    if self.debug:
                        print("Google: Negation word found!")
                    self.negation = True
            for whichWord in range(len(whichWords)):
                if whichWords[whichWord] == questionWords[questionWord]:
                    if self.debug:
                        print("Google: Which word found!")
                    self.which = True

        focusOnWords = []
        for questionWord in range(len(questionWords)):
            if questionWords[questionWord].istitle():
                focusOnWords.append(questionWords[questionWord])
            if questionWords[questionWord] == "in":
                focusOnWords.append(questionWords[questionWord + 1])

        self.loadSearchPage()
        self.enableAddSearch = False

        if self.question.find("“") != -1 and self.question.find("”") != -1:
            self.enableAddSearch = True
            self.searchExactlyFor = self.question.split("“")[1].split("”")[0]
            self.additionalSearch()

        whichPred = []
        if self.which:
            whichSearch = self.searchAnswers()

            for search in range(len(whichSearch)):
                count = 0

                answerWords = whichSearch[search].split()

                for word in range(len(focusOnWords)):
                    count += answerWords.count(focusOnWords[word])

                whichPred.append(count)

        prediction = []
        for answer in range(len(answers)):
            answerWords = answers[answer].split()

            count = 0
            for word in range(len(self.words)):
                for answerWord in range(len(answerWords)):
                    if answerWords[answerWord] in self.words[word]:
                        count += 1
            prediction.append(count)

        answerPredictions = []
        if self.which:
            for answer in range(len(answers)):
                answerPredictions.append(prediction[answer] + whichPred[answer])
        else:
            for answer in range(len(answers)):
                answerPredictions.append(prediction[answer])

        return answerPredictions

    def loadSearchPage(self):
        search_results = google.search(self.question, 1, 'en')

        words = ""
        for result in search_results:
            words += result.name + "\n"
            words += result.description + "\n"

        self.words = words.lower().split()


    def additionalSearch(self):
        """ It will run twice, firstly it will search for question (just like first search)
            BUT with specified exactTerms (words in quotes).

            Second run will just search words in quotes """

        exact = ""
        for i in self.searchExactlyFor:
            exact += ' "' + i + '"'

        for runNum in range(1):
            if runNum == 0:
                search_results = google.search(self.question + exact, 1, 'en')
            else:
                search_results = google.search(exact, 1, 'en')

            words = ""
            for result in search_results:
                words += result.name + "\n"
                words += result.description + "\n"

            self.words.append(words.lower().split())

    def searchAnswers(self):
        answerSearchWords = []
        for runNum in range(len(self.answers)):
            if self.enableAddSearch:
                exact = ""
                for i in self.searchExactlyFor:
                    exact += ' "' + i + '"'

                search_results = google.search(self.answers[runNum]['text'] + exact, 1, 'en')
            else:
                search_results = google.search(self.answers[runNum]['text'], 1, 'en')

            words = ""
            for result in search_results:
                words += result.name + "\n"
                words += result.description + "\n"

            answerSearchWords.append(words.lower())

        return answerSearchWords
