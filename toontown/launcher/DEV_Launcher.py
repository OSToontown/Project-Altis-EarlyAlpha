from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton

from socket import *
import json
from Crypto.Cipher import XOR
import base64

import os
import sys


class DEV_Launcher():

    def __init__(self):

        #  Create the socket and configure it
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.settimeout(5)

        os.environ['TT_PLAYCOOKIE'] = '.DEFAULT'
        os.environ['TT_GAMESERVER'] = '127.0.0.1'

        username = raw_input('Username: ')
        password = raw_input('Password: ')
        ip = raw_input('IP: ')

        self.clientsock.connect((str(ip), 4014))

        sendData = {str(self.encrypt(str(username))): str(self.encrypt(str(password)))}
        sendData = json.dumps(sendData)
        self.clientsock.send(sendData)
        self.client()

    def client(self):
        data = self.clientsock.recv(1024)
        self.handle(data)

        self.clientsock.close()

    def handle(self, data):
        data = json.loads(data)
        self.key = ''
        for key, value in data.iteritems():
            self.key = key
        self.value = data[self.key]
        self.key = self.decrypt(self.key)
        self.value = self.decrypt(self.value)

        if self.key == 'error':
            print self.key + ': ' + self.value
        elif self.key == 'playcookie':
            self.playgame(self.value)

    def encrypt(self, plaintext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return base64.b64encode(cipher.encrypt(plaintext))

    def decrypt(self, ciphertext):
        cipher = XOR.new('iplaypokemongoeveryday')
        return cipher.decrypt(base64.b64decode(ciphertext))

    def playgame(self, playcookie):
        try:
            os.system('C:\Panda3D-1.9.0\python\ppython.exe -m toontown.toonbase.ToontownStart -c ' + playcookie)
        except:
            pass

        sys.exit(1)

launcher = DEV_Launcher()
launcher.run()