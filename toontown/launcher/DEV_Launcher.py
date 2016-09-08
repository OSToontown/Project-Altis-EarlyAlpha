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

        self.accept("tab", self.focus)
        self.accept("escape", sys.exit)

        self.current_focus = 0

    def focus(self):
        if self.current_focus == 0:
            self.current_focus = 1
            self.username_entry['focus'] = 1
            self.ip_entry['focus'] = 0
        else:
            self.current_focus = 0
            self.username_entry['focus'] = 0
            self.ip_entry['focus'] = 1

    def login(self):
        os.environ['ttrUsername'] = self.username_entry.get()
        os.environ['ttrPassword'] = self.password_entry.get()
        os.environ['TTR_GAMESERVER'] = self.ip_entry.get()
        os.environ['TTR_PLAYCOOKIE'] = self.username_entry.get()

        os.system('C:\Panda3D-1.9.0\python\ppython.exe -m toontown.toonbase.ToontownStart')

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
        self.login_button = DirectButton(text="Login", scale=0.1, pos=(0, 0, -0.6), command=self.login)

        self.username_entry.reparentTo(self.main_frame)
        self.username_text.reparentTo(self.main_frame)
        self.password_entry.reparentTo(self.main_frame)
        self.password_text.reparentTo(self.main_frame)
        self.ip_entry.reparentTo(self.main_frame)
        self.ip_text.reparentTo(self.main_frame)
        self.login_button.reparentTo(self.main_frame)

launcher = DEV_Launcher()
launcher.run()