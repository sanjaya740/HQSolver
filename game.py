import json
import sys

from chat import Chat
from config import readFromConfig
from dataclasses import Data
from solver import Solver

from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from shutil import get_terminal_size
from twisted.internet.protocol import ReconnectingClientFactory

debug = readFromConfig("General", "debug_mode")


class GameProtocol(WebSocketClientProtocol):
    def onOpen(self):
        if debug:
            print("[Connection] Connection established!")
        self.block_chat = False  # It will block chat when question are shown
        self.chat = Chat()
        self.solver = Solver()

        """ Broadcast Stats """
        self.bs_enable = readFromConfig("BroadcastStats", "enable")
        self.bs_connected = readFromConfig("BroadcastStats", "show_connected")
        self.bs_playing = readFromConfig("BroadcastStats", "show_playing")
        self.bs_eliminated = readFromConfig("BroadcastStats", "show_eliminated")

        """ Game Summary """
        self.gs_enable = readFromConfig("GameSummary", "enable")
        self.gs_prize = readFromConfig("GameSummary", "show_prize")
        self.gs_userids = readFromConfig("GameSummary", "show_userids")
        self.gs_usernames = readFromConfig("GameSummary", "show_usernames")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = json.loads(payload.decode())

            if message["type"] == "question":
                self.block_chat = True
                self.solver.solve(message)
            elif message["type"] == "questionClosed":
                self.block_chat = False
            elif message["type"] == "questionSummary":
                self.block_chat = True
                self.solver.solve(message)
            elif message["type"] == "questionFinished":
                self.block_chat = False

            if not self.block_chat:
                if (message["type"] == "interaction" and message["itemId"] == "chat") or message["type"] == "kicked":
                    self.chat.showMessage(message)
                elif message["type"] == "broadcastStats" and self.bs_enable:
                    connected = str(message["viewerCounts"]["connected"])
                    playing = str(message["viewerCounts"]["playing"])
                    watching = str(message["viewerCounts"]["watching"])

                    print(" Broadcast Stats ".center(get_terminal_size()[0], "="))
                    if self.bs_connected:
                        print(("Connected Players: " + connected).center(get_terminal_size()[0]))
                    if self.bs_playing:
                        print(("Playing Players: " + playing).center(get_terminal_size()[0]))
                    if self.bs_eliminated:
                        print(("Eliminated Players: " + watching).center(get_terminal_size()[0]))
                    print("".center(get_terminal_size()[0], "="))

            if message["type"] == "gameSummary":
                if self.gs_enable:
                    self.block_chat = True

                    winnerCount = str(message["numWinners"])
                    winnerList = message["winners"]

                    print(" Game Summary ".center(get_terminal_size()[0], "="))
                    print((winnerCount + " Winners!").center(get_terminal_size()[0]))

                    for winner in range(len(winnerList)):
                        userInfo = winnerList[winner]

                        toPrint = ""

                        if self.gs_usernames or self.gs_userids:
                            if self.gs_usernames:
                                toPrint += str(userInfo["name"]) + ' '
                            if self.gs_usernames and self.gs_userids:
                                toPrint += '(' + str(userInfo["id"]) + ') '
                            elif self.gs_userids:
                                toPrint += str(userInfo["id"]) + ' '

                        if self.gs_prize:
                            toPrint += "just won " + str(userInfo["prize"] + "!")

                    print("".center(get_terminal_size()[0], "="))
            elif message["type"] == "postGame":
                self.block_chat = False

            if message["type"] == "broadcastEnded":
                Data.allowReconnecting = False
                self.transport.loseConnection()


class GameFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = GameProtocol

    def clientConnectionFailed(self, connector, reason):
        if debug:
            print("[Connection] Connection failed! Retrying...")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        if Data.allowReconnecting:
            if debug:
                print("[Connection] Connection has been lost! Retrying...")
            self.retry(connector)
        else:
            print(" Game Ended! ".center(get_terminal_size()[0], "*"))
