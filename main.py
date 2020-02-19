#!/usr/bin/env python

import random
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

websocket.enableTrace(False)

class GameClient:
    def __init__(self, url):
        self.ws = websocket.WebSocketApp(url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.turn = False
        self.started = False
        self.available = list()


    def on_message(self, message):
        #print("recu = ", message)

        # COMMAND
        if message[0] == '$':
            if message[1:] == "AWAITING":
                self.turn = False
                print("En attente de l'autre joueur")
            if message[1:] == "START":
                self.started = True
            if "OPPONENT" in message[1:]:
                print("L'adervsaire à joué : ", message.split(" ")[1])
            if message[1:] == "READY":
                self.turn = True

        # ERROR
        if message[0] == '!':
            print("Erreur : ", message[1:])

        # INFO
        if message[0] == '#':
            if(message[1:].split(" ")[0] == "AVAILABLE"):
                self.available.extend(message[1:].split(" ")[1:])
                self.play()
                return
            else:
                print("Information : ", message[1:])

        # RESULT
        if message[0] == '=':
            self.turn = False
            print("Capturé(s) : ", message[1:].split(" "))

        if self.started and self.turn:
            self.ws.send("$AVAILABLE")


    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        def run(*args):
            print("Connecté.")

        thread.start_new_thread(run, ())

    def run(self):
        self.ws.run_forever()

    def play(self):
        time.sleep(0.1)
        coord = random.choice(self.available)
        print("coord : ", coord)
        self.ws.send(coord)
        #coord_input = input("Entrez la coordonnée : ")
        #self.ws.send(coord_input)


client = GameClient("ws://localhost:8989/room/toto")
client.run()
