import platform
import re

from config import readFromConfig


class Chat(object):
    def __init__(self):
        self.enable = readFromConfig("Chat", "enable")
        self.show_usernames = readFromConfig("Chat", "show_usernames")
        self.show_userids = readFromConfig("Chat", "show_userids")
        self.show_message = readFromConfig("Chat", "show_message")

    def showMessage(self, message):
        if not self.enable:
            return True

        self.message = message

        preparedMessage = self.prepareMessage()

        if platform.system() == "Windows":
            finalMessage = self.fixMessage(preparedMessage)
        else:
            finalMessage = preparedMessage

        print(finalMessage)

        return True

    def prepareMessage(self):
        toPrint = ""

        if self.show_usernames or self.show_userids:
            if self.show_usernames:
                toPrint += str(self.message["metadata"]["username"])
            if self.show_usernames and self.show_userids:
                toPrint += " (" + str(self.message["metadata"]["userId"]) + ")"
            elif self.show_userids:
                toPrint += str(self.message["metadata"]["userId"])

        if self.show_message and (self.show_usernames or self.show_userids):
            toPrint += ": " + str(self.message["metadata"]["message"])
        elif self.show_message:
            toPrint += str(self.message["metadata"]["message"])

        return toPrint

    def fixMessage(self, message):
        """ Microsoft Windows Command Line (CMD) are crashing because of incorrect characters.

        This will remove all characters that are not letters and / or numbers
        """

        return re.sub(r'\W+\(\)', '', message)
