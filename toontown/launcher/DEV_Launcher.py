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


class DEV_Launcher(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        #  Create the socket and configure it
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.settimeout(5)

        self.createGUI()

        os.environ['TT_PLAYCOOKIE'] = 'DEFAULT'
        os.environ['TT_GAMESERVER'] = '127.0.0.1'

        self.accept("tab", self.focus)
        self.accept("escape", sys.exit)

        self.current_focus = 0

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

    def focus(self):
        if self.current_focus == 0:
            self.current_focus = 1
            self.username_entry['focus'] = 1
            self.ip_entry['focus'] = 0
        else:
            self.current_focus = 0
            self.username_entry['focus'] = 0
            self.ip_entry['focus'] = 1

    def loginbutton(self):
        os.environ['ttUsername'] = self.username_entry.get()
        os.environ['ttPassword'] = self.password_entry.get()
        os.environ['TT_GAMESERVER'] = self.ip_entry.get()

        self.clientsock.connect((str(self.ip_entry.get()), 4014))
        username = str(self.username_entry.get())
        password = str(self.password_entry.get())

        sendData = {str(self.encrypt(username)): str(self.encrypt(password))}
        sendData = json.dumps(sendData)
        self.clientsock.send(sendData)
        self.client()

    def playgame(self, playcookie):
        os.environ['TT_PLAYCOOKIE'] = playcookie
        try:
            os.system('C:\Panda3D-1.9.0\python\ppython.exe -m toontown.toonbase.ToontownStart')
        except:
            pass

        sys.exit(1)

    def createGUI(self):
        self.main_frame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-1, 1, -1, 1))
        self.username_text = OnscreenText(text="Username:", pos=(-0.6, 0, 0))
        self.username_entry = DirectEntry(text="", initialText="", scale=0.1, numLines=1, pos=(-0.3, 0, 0),
                                          cursorKeys=1,
                                          obscured=0, width=10)
        self.password_text = OnscreenText(text="Password:", pos=(-0.6, -0.2))
        self.password_entry = DirectEntry(text="", initialText="", scale=0.1, numLines=1, pos=(-0.3, 0, -0.2),
                                          cursorKeys=1,
                                          obscured=1, width=10)
        self.ip_text = OnscreenText(text="Server IP:", pos=(-0.6, -0.4))
        self.ip_entry = DirectEntry(text="", initialText="", scale=0.1, numLines=1, pos=(-0.3, 0, -0.4),
                                    cursorKeys=1,
                                    obscured=0, width=10)
        self.login_button = DirectButton(text="Login", scale=0.1, pos=(0, 0, -0.6), command=self.loginbutton)

        self.username_entry.reparentTo(self.main_frame)
        self.username_text.reparentTo(self.main_frame)
        self.password_entry.reparentTo(self.main_frame)
        self.password_text.reparentTo(self.main_frame)
        self.ip_entry.reparentTo(self.main_frame)
        self.ip_text.reparentTo(self.main_frame)
        self.login_button.reparentTo(self.main_frame)

launcher = DEV_Launcher()
launcher.run()