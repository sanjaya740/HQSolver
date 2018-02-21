import json

from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from twisted.internet.protocol import ReconnectingClientFactory

from chat import Chat
from config import readFromConfig

debug = readFromConfig("General", "debug_mode")


class GameProtocol(WebSocketClientProtocol):
    def onOpen(self):
        if debug:
            print("[Connection] Connection established!")
        self.block_chat = False  # It will block chat when question are shown
        self.chat = Chat()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = json.loads(payload.decode())

            if message["type"] == "question":
                self.block_chat = True
            elif message["type"] == "questionClosed":
                self.block_chat = False
            elif message["type"] == "questionSummary":
                self.block_chat = True
            elif message["type"] == "questionFinished":
                self.block_chat = False
            
            if not self.block_chat:
                if message["type"] == "interaction" and message["itemId"] == "chat":
                    self.chat.showMessage(message)


class GameFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = GameProtocol

    def clientConnectionFailed(self, connector, reason):
        if debug:
            print("[Connection] Connection failed! Retrying...")
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        if debug:
            print("[Connection] Connection has been lost! Retrying...")
        self.retry(connector)
