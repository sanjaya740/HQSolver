import wikipedia

from config import negationWords

from shutil import get_terminal_size


class Wikipedia(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.negation = False

        wikipedia.set_lang("en")

    def solve(self, question, answers, category, queue=None):
        self.question = question
        self.answers = answers
        self.category = category

        self.correctPageNames = self.searchForPotencialPages()

        try:
            answers = self.getAnswer()
        except:
            answers = [0, 0, 0]
            print("\33[33mWiki: Warning! It seems that we have problem getting info from Wikipedia.\33[0m")

        if self.debug:
            print("Wiki:", answers)

        mostPropably = max(answers)
        ifNOTmostPropably = min(answers)

        if (mostPropably != 0 or ifNOTmostPropably != 0) and (
                answers.count(mostPropably) == 1 or answers.count(ifNOTmostPropably) == 1):

            if not self.negation:
                correct = answers.index(mostPropably)
                print((" Wikipedia solver thinks that correct answer is: \33[33m" + self.answers[correct][
                    'text'] + " \33[0m").center(get_terminal_size()[0], "*"))
            else:
                correct = answers.index(ifNOTmostPropably)
                print((" Wikipedia solver thinks that correct answer is: \33[33m" + self.answers[correct][
                    'text'] + " \33[0m").center(get_terminal_size()[0], "*"))

        if answers == [0, 0, 0]:
            print(" Wikipedia solver couldn't guess the answer! ".center(get_terminal_size()[0], "*"))

        if queue is not None:
            queue.put(answers)
        return answers

    def searchForPotencialPages(self):
        """ Try to search correct answer pages in wikipedia """

        potencialPages = []

        for answer in range(len(self.answers)):
            searchResults = wikipedia.search(self.answers[answer]["text"])

            found = False
            for result in range(len(searchResults)):
                if self.category.lower() in searchResults[result].lower():
                    potencialPages.append(searchResults[result])
                    found = True
                    break

            if not found:
                if len(searchResults) == 0:
                    potencialPages.append('')
                else:
                    potencialPages.append(searchResults[0])  # If not found try first page

        return potencialPages

    def getAnswer(self):
        question = self.question.lower()
        questionWords = question.replace("?", "").split()

        for questionWord in range(len(questionWords)):
            for negWord in range(len(negationWords)):
                if negationWords[negWord] == questionWords[questionWord]:
                    if self.debug:
                        print("Wiki: Negation word found!")
                    self.negation = True

        focusOnWords = []
        for questionWord in range(len(questionWords)):
            if questionWords[questionWord].istitle():
                focusOnWords.append(questionWords[questionWord])
            if questionWords[questionWord] == "in":
                focusOnWords.append(questionWords[questionWord + 1])

        loadedPages = self.loadPages()

        if self.question.find("“") != -1 and self.question.find("”") != -1:
            focusOnWords.append(question.split("“")[1].split("”")[0])

        answers = []

        for page in range(len(loadedPages)):
            count = 0
            words = loadedPages[page].split()

            for focusWord in range(len(focusOnWords)):
                count += words.count(focusOnWords[focusWord])

            answers.append(count)

        return answers

    def loadPages(self):
        pages = []
        for page in range(len(self.correctPageNames)):
            if self.correctPageNames[page] == '':
                pages.append('')
            else:
                pages.append(wikipedia.page(self.correctPageNames[page]).content.lower())

        return pages
