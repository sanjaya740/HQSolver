from config import readFromConfig

from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
from twisted.internet.protocol import ReconnectingClientFactory

debug = readFromConfig("General", "debug_mode")


class GameProtocol(WebSocketClientProtocol):
    def onOpen(self):
        if debug:
            print("[Connection] Connection established!")

    def onMessage(self, payload, isBinary):
        message = payload.decode()


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
