from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton

import os
import sys


class DEV_Launcher(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.createGUI()

        os.environ['TT_PLAYCOOKIE'] = 'DEFAULT'
        os.environ['TT_GAMESERVER'] = '127.0.0.1'

    def login(self):
        os.environ['TT_PLAYCOOKIE'] = self.username_entry.get()
        os.environ['TT_GAMESERVER'] = self.ip_entry.get()

        os.system('C:\Panda3D-1.10.0\python\ppython.exe -m toontown.toonbase.ToontownStart')

        sys.exit(1)

    def createGUI(self):
        self.main_frame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-1, 1, -1, 1))
        self.username_text = OnscreenText(text="Username:", pos=(-0.6, 0, 0))
        self.username_entry = DirectEntry(text="", initialText="", scale=0.1, numLines=1, pos=(-0.3, 0, 0),
                                          cursorKeys=0,
                                          obscured=0, width=10)
        self.ip_text = OnscreenText(text="Server IP:", pos=(-0.6, -0.2))
        self.ip_entry = DirectEntry(text="", initialText="", scale=0.1, numLines=1, pos=(-0.3, 0, -0.2),
                                    cursorKeys=0,
                                    obscured=0, width=10)
        self.login_button = DirectButton(text="Login", scale=0.1, pos=(0, 0, -0.4), command=self.login)

        self.username_entry.reparentTo(self.main_frame)
        self.username_text.reparentTo(self.main_frame)
        self.ip_entry.reparentTo(self.main_frame)
        self.ip_text.reparentTo(self.main_frame)
        self.login_button.reparentTo(self.main_frame)

launcher = DEV_Launcher()
launcher.run()