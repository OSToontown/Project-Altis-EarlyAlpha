import sys
import os
from socket import *
import json
from Crypto.Cipher import XOR
import base64

import AltisLauncher


class AltisLauncherApp():
    def __init__(self):
        self.username = None
        self.password = None

        #  Create the socket and configure it
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.settimeout(5)

        os.environ['TT_PLAYCOOKIE'] = '.DEFAULT'
        os.environ['TT_GAMESERVER'] = '127.0.0.1' #'158.69.213.51' for Owen's server.
        self.login()

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

    def login(self):
        self.username = os.environ.get('TTUSERNAME', 'None')
        self.password = os.environ.get('TTPASSWORD', 'None')

        self.clientsock.connect(('127.0.0.1', 4014))#'158.69.213.51', 4014)) for Owen's server.

        sendData = {str(self.encrypt(self.username)): str(self.encrypt(self.password))}
        sendData = json.dumps(sendData)
        self.clientsock.send(sendData)
        self.client()
        
        os.environ['TTUSERNAME'] = 'None'
        os.environ['TTPASSWORD'] = 'None'

    def playgame(self, playcookie):
        try:
            os.system('Panda3D-1.9.0\python\ppython.exe -m toontown.toonbase.ToontownStart -c ' + playcookie)
        except:
            pass

        sys.exit(1)
        
AltisLauncherApp()
