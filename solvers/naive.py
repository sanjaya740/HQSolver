import requests

from config import negationWords, whichWords

from shutil import get_terminal_size


class Naive(object):
    """ Naive solver

    Asks google, loads the search results page, and checks how many times the answers appear on the results page. The
    answer which is the most popular is returned. However, if the question contains the word "NOT", the answer is the
    least popular one.

    Additionally, if the question contains words in quotes, it is additionally searched, and subjected to the same
    analysis (see above).

    If the question contains word "Which", additionally, looks for answers in google.
    """

    def __init__(self, google_api_key, google_cse_id, debug=False):
        self.debug = debug
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id
        self.negation = False
        self.which = False

    def solve(self, question, answers):
        """ question = 'Which ballroom dance is typically performed in 3/4 time?'
            answers = [{'text': 'Rumba'}, {'text': 'Waltz'}, {'text': 'Tango'}] """

        self.question = question
        self.answers = answers

        try:
            answers = self.getAnswer()
        except:
            answers = [0, 0, 0]
            print("\33[33mNaive: Warning! It seems that we have problem getting info from Google API.\n"
                  "Most common issue is that your daily limit for this API has been exceeded!\33[0m")

        if self.debug:
            print("Naive:", answers)

        mostPropably = max(answers)
        ifNOTmostPropably = min(answers)

        if (mostPropably != 0 or ifNOTmostPropably != 0) and (answers.count(mostPropably) == 1 or answers.count(ifNOTmostPropably) == 1):

            if not self.negation:
                correct = answers.index(mostPropably)
                print((" Naive solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + "\33["
                                                                                                                "0m").center(get_terminal_size()[0], "*"))
                return correct
            else:
                correct = answers.index(ifNOTmostPropably)
                print((" Naive solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + "\33["
                                                                                                                "0m").center(get_terminal_size()[0], "*"))
                return correct

        print(" Naive solver couldn't guess the answer! ".center(get_terminal_size()[0], "*"))

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
                        print("Naive: Negation word found!")
                    self.negation = True
            for whichWord in range(len(whichWords)):
                if whichWords[whichWord] == questionWords[questionWord]:
                    if self.debug:
                        print("Naive: Which word found!")
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
        payload = {
            "q": self.question,
            "cx": self.google_cse_id,
            "filter": "1",  # Turns off duplicate filter
            "lr": "lang_en",  # Returns search results in English
            "key": self.google_api_key
        }

        request = requests.get("https://www.googleapis.com/customsearch/v1", params=payload)
        response = request.json()

        items = response["items"]

        words = ""
        for item in range(len(items)):
            words += items[item]['title'] + "\n"
            words += items[item]['snippet'] + "\n"

        self.words = words.lower().split()

    def additionalSearch(self):
        """ It will run twice, firstly it will search for question (just like first search)
            BUT with specified exactTerms (words in quotes).

            Second run will just search words in quotes """

        for runNum in range(1):
            if runNum == 0:
                payload = {
                    "q": self.question,
                    "cx": self.google_cse_id,
                    "exactTerms": self.searchExactlyFor,
                    "filter": "1",  # Turns off duplicate filter
                    "lr": "lang_en",  # Returns search results in English
                    "key": self.google_api_key
                }
            else:
                payload = {
                    "q": self.searchExactlyFor,
                    "cx": self.google_cse_id,
                    "filter": "1",  # Turns off duplicate filter
                    "lr": "lang_en",  # Returns search results in English
                    "key": self.google_api_key
                }

            request = requests.get("https://www.googleapis.com/customsearch/v1", params=payload)
            response = request.json()

            items = response["items"]

            words = ""
            for item in range(len(items)):
                words += items[item]['title'] + "\n"
                words += items[item]['snippet'] + "\n"

            self.words.append(words.lower().split())

    def searchAnswers(self):
        answerSearchWords = []
        for runNum in range(len(self.answers)):
            if self.enableAddSearch:
                payload = {
                    "q": self.answers[runNum]['text'],
                    "cx": self.google_cse_id,
                    "exactTerms": self.searchExactlyFor,
                    "filter": "1",  # Turns off duplicate filter
                    "lr": "lang_en",  # Returns search results in English
                    "key": self.google_api_key
                }
            else:
                payload = {
                    "q": self.answers[runNum]['text'],
                    "cx": self.google_cse_id,
                    "filter": "1",  # Turns off duplicate filter
                    "lr": "lang_en",  # Returns search results in English
                    "key": self.google_api_key
                }

            request = requests.get("https://www.googleapis.com/customsearch/v1", params=payload)
            response = request.json()

            items = response["items"]

            words = ""
            for item in range(len(items)):
                words += items[item]['title'] + "\n"
                words += items[item]['snippet'] + "\n"

            answerSearchWords.append(words.lower())

        return answerSearchWords
