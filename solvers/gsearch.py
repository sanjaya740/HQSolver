from shutil import get_terminal_size

import nltk
from google import google

from config import negationWords
from dhooks import Webhook, Embed

webhook_url = "https://discordapp.com/api/webhooks/584715861890433025/9AIxErMi3ijsNHWkOhqMDcJZSGHnq8m8MIsLz75Z-BYvC1L11Pc0X-WHptdhMkGQHMaF"

hook = Webhook(webhook_url)


class Google(object):
    def __init__(self, debug=False):
        self.debug = debug
        try:
            self.stopwords = nltk.corpus.stopwords.words("english")
        except:
            nltk.download('stopwords')
            self.stopwords = nltk.corpus.stopwords.words("english")

        self.negation = False
        self.which = False

    def solve(self, question, answers, queue=None):
        self.question = question
        self.answers = answers

        try:
            answers = self.getAnswer()
        except Exception as e:
            print(e)
            answers = [0, 0, 0]
            print("\33[33mGoogle: Warning! It seems that we have problem getting info from Google!\33[0m")
            hook.send("\33[33mGoogle: Warning! It seems that we have problem getting info from Google!\33[0m")


        if self.debug:
            print("Google:", answers)

        mostPropably = max(answers)
        ifNOTmostPropably = min(answers)

        if (mostPropably != 0 or ifNOTmostPropably != 0) and (
                answers.count(mostPropably) == 1 or answers.count(ifNOTmostPropably) == 1):

            if not self.negation:
                correct = answers.index(mostPropably)
                hook.send((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33[""0m"))
                print((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33[""0m").center(get_terminal_size()[0], "*"))
            else:
                correct = answers.index(ifNOTmostPropably)
                hook.send((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33[""0m"))
                print((" Google solver thinks that correct answer is: \33[33m" + self.answers[correct]['text'] + " \33[""0m").center(get_terminal_size()[0], "*"))

        if answers == [0, 0, 0]:
            hook.send("Google solver couldn't guess the answer! ")
            print(" Google solver couldn't guess the answer! ".center(get_terminal_size()[0], "*"))

        if queue is not None:
            queue.put(answers)
        return answers

    def getAnswer(self):
        question = self.question.lower()
        questionWords = question.replace("?", "").split()
        self.filtered_words = [word for word in questionWords if word not in self.stopwords]

        answers = []
        for answer in range(len(self.answers)):
            answers.append(self.answers[answer]['text'].lower())

        for questionWord in range(len(questionWords)):
            for negWord in range(len(negationWords)):
                if negationWords[negWord] == questionWords[questionWord]:
                    if self.debug:
                        print("Google: Negation word found!")
                    self.negation = True

        focusOnWords = []
        for questionWord in range(len(questionWords)):
            if questionWords[questionWord].istitle():
                focusOnWords.append(questionWords[questionWord])
            if questionWords[questionWord] == "in":
                focusOnWords.append(questionWords[questionWord + 1])

        predictions = self.method1()
        self.enableAddSearch = False

        if self.question.find("“") != -1 and self.question.find("”") != -1:
            self.enableAddSearch = True
            self.searchExactlyFor = self.question.split("“")[1].split("”")[0]
            method2Pred = self.method2()
            for prediction in range(len(method2Pred)):
                predictions[prediction] = predictions[prediction] + method2Pred[prediction]

        method3Pred = self.method3()
        for prediction in range(len(method3Pred)):
            predictions[prediction] = predictions[prediction] + method3Pred[prediction]

        return predictions

    def method1(self):
        question = self.filtered_words

        questionStr = ""
        for word in question:
            questionStr += word + " "

        search_results = google.search(questionStr, 1, 'en')

        words = ""
        for result in search_results:
            words += result.name + "\n"
            words += result.description + "\n"

        words = words.lower().split()

        prediction = []
        for answer in self.answers:
            answerWords = answer['text'].lower().split()

            count = 0
            for word in words:
                for answerWord in answerWords:
                    if answerWord in word:
                        count += 1
            prediction.append(count)

        return prediction

    def method2(self):
        search_results = google.search(self.searchExactlyFor, 1, 'en')

        words = ""
        for result in search_results:
            words += result.name + "\n"
            words += result.description + "\n"

        words = words.lower().split()

        prediction = []
        for answer in self.answers:
            answerWords = answer['text'].lower().split()

            count = 0
            for word in words:
                for answerWord in answerWords:
                    if answerWord in word:
                        count += 1
            prediction.append(count)

        return prediction

    def method3(self):
        question = self.filtered_words

        questionStr = ""
        for word in question:
            questionStr += ' "' + word + '"'

        prediction = []
        for answer in self.answers:
            current = answer['text']

            search_results = google.search(current + questionStr, 1, 'en')

            words = ""
            for result in search_results:
                words += result.name + "\n"
                words += result.description + "\n"

            words = words.lower().split()

            answerWords = answer['text'].lower().split()

            count = 0
            for word in words:
                for answerWord in answerWords:
                    if answerWord in word:
                        count += 1
            prediction.append(count)

        return prediction
