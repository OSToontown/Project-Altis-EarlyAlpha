from PyQt4 import QtGui
import sys
import os
from socket import *
import json
from Crypto.Cipher import XOR
import base64

import AltisLauncher


class AltisLauncherApp(QtGui.QMainWindow, AltisLauncher.Ui_AltisLauncher):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.LoginButton.clicked.connect(self.login)
        self.QuitButton.clicked.connect(sys.exit)
        self.username = str(self.UsernameEntry.text())
        self.password = str(self.PasswordEntry.text())

        #  Create the socket and configure it
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.settimeout(5)

        os.environ['TT_PLAYCOOKIE'] = '.DEFAULT'
        os.environ['TT_GAMESERVER'] = '127.0.0.1'

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
        self.username = str(self.UsernameEntry.text())
        self.password = str(self.PasswordEntry.text())

        os.environ['ttUsername'] = self.username
        os.environ['ttPassword'] = self.password

        self.clientsock.connect(('127.0.0.1', 4014))

        sendData = {str(self.encrypt(self.username)): str(self.encrypt(self.password))}
        sendData = json.dumps(sendData)
        self.clientsock.send(sendData)
        self.client()

    def playgame(self, playcookie):
        try:
            os.system('Panda3D-1.9.0\python\ppython.exe -m toontown.toonbase.ToontownStart -c ' + playcookie)
        except:
            pass

        sys.exit(1)

def main(self):
    app = QtGui.QApplication(sys.argv)
    form = AltisLauncherApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main(QtGui.QMainWindow)