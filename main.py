import json
import requests
import sys

from config import login_header, readFromConfig
from shutil import get_terminal_size

from dhooks import Webhook, Embed

from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor, ssl

from game import GameFactory

webhook_url = "https://discordapp.com/api/webhooks/584715861890433025/9AIxErMi3ijsNHWkOhqMDcJZSGHnq8m8MIsLz75Z-BYvC1L11Pc0X-WHptdhMkGQHMaF"

#############################
try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")

class Launcher(object):
    def __init__(self):
        self.api_shows = readFromConfig("API", "shows_now")
        self.debug = readFromConfig("General", "debug_mode")
        self.server_ip = readFromConfig("General", "server_ip")

    def launchSolver(self):

        print(" HQ Solver ".center(get_terminal_size()[0], "="))
        hook.send('HQ Solver')

        if self.showAlive():
            socketURL = self.getSocketURL()

            proto = socketURL.split('://')[0]
            server = socketURL.split('://')[1].split("/")[0]
            server_dir = socketURL.replace(proto + '://' + server, "")

            if proto == "http":
                self.socketURL = "ws://" + server + ":80" + server_dir
            elif proto == "https":
                self.socketURL = "wss://" + server + ":443" + server_dir
            else:
                self.socketURL = socketURL

            factory = GameFactory(self.socketURL, headers=login_header)
            factory.setProtocolOptions(autoPingInterval=5, autoPingTimeout=5, autoPingSize=20)

            if factory.isSecure:
                contextFactory = ssl.ClientContextFactory()
            else:
                contextFactory = None

            connectWS(factory, contextFactory)
            reactor.run()
        else:
            print(''.center(get_terminal_size()[0], '='))
            sys.exit(0)

    def showAlive(self):
        """ Checks if show is live """

        request = requests.get(self.server_ip + self.api_shows, headers=login_header)
        response = request.content.decode()

        try:
            responseJSON = json.loads(response)

            if responseJSON["active"]:
                hook.send('Show is now live!')
                print("Show is now live!".center(get_terminal_size()[0]))
                return True
            else:
                hook.send('Show aren\'t live!')
                print("Show aren't live!".center(get_terminal_size()[0]))
                return False
        except:
            hook.send('Server returned unknown response!')
            print("Server returned unknown response!".center(get_terminal_size()[0]))
            return False

    def getSocketURL(self):

        request = requests.get(self.server_ip + self.api_shows, headers=login_header)
        response = request.content.decode()

        try:
            broadcastJSON = json.loads(response)["broadcast"]

            socketURL = broadcastJSON["socketUrl"]
            return socketURL
        except:
            return False


if __name__ == "__main__":
    Launcher().launchSolver()
