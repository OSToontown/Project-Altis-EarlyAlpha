'''
Created on Sep 12, 2016

@author: Drew
'''

from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import random

from toontown.hood import SkyUtil
from toontown.launcher import DownloadForceAcknowledge
from toontown.toon import ToonDNA, Toon, ToonHead
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp

MAIN_POS = (-60, 1, 11)
MAIN_HPR = (-90, 5, 0)

chooser_notify = DirectNotifyGlobal.directNotify.newCategory('PickAToon')

MAX_AVATARS = 6

class PickAToon:
    
    def __init__(self, avatarList, parentFSM, doneEvent):
        self.toonList = {i: (i in [x.position for x in avatarList]) for i in xrange(6)}
        self.avatarList = avatarList
        self.selectedToon = 0
        self.doneEvent = doneEvent
        self.jumpIn = None
        return

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)
        
    def enter(self):
        base.disableMouse()
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        self.deleteButton.show()
        self.patNode.unstash()

        self.checkPlayButton()
        self.updateFunc()
        self.setButtonNames()
                
    def exit(self):
        base.cam.iPosHpr()
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.deleteButton.hide()
        return None

    def load(self):
        self.patNode = render.attachNewNode('patNode')
        self.patNode2d = aspect2d.attachNewNode('patNode2d')
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        gui2 = loader.loadModel('phase_3/models/gui/quit_button')
        newGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        
        self.background = loader.loadModel('phase_4/models/neighborhoods/toontown_central_full')
        self.background.reparentTo(render)
        for frame in render.findAllMatches('*/doorFrame*'):
            frame.removeNode()
        self.sky = loader.loadModel('phase_3.5/models/props/TT_sky')
        SkyUtil.startCloudSky(self)
        base.camera.setPosHpr(MAIN_POS, MAIN_HPR)

        self.title = OnscreenText(TTLocalizer.AvatarChooserPickAToon, scale=TTLocalizer.ACtitle, parent=hidden, fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))

        # Quit Button
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitHover = quitHover
        self.quitButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text=TTLocalizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(1.08, 0, -0.907), command=self.__handleQuit)
        self.quitButton.reparentTo(base.a2dBottomLeft)
        self.quitButton.setPos(0.25, 0, 0.075)
        
        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()

        # DMENU Pat Screen Stuff
        self.play = DirectButton(relief = None, image = (btnUp, btnDn, btnRlvr), text = 'PLAY THIS TOON', text_scale = .050, scale=1.2, pos=(0, 0, -0.93), image_color = (1, 1, 1, 1), image1_color = (0.8, 0.8, 0, 1), image2_color = (0.15, 0.82, 1.0, 1), command=self.playGame, parent=self.patNode2d)
        
        self.toon = Toon.Toon()
        self.toon.setPosHpr(-46, 1, 8.1, 90, 0, 0)
        self.toon.reparentTo(self.patNode)
        
        self.pickAToonGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        self.buttonBgs = []
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareRed'))
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareGreen'))
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squarePurple'))
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareBlue'))
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squarePink'))
        self.buttonBgs.append(self.pickAToonGui.find('**/tt_t_gui_pat_squareYellow'))
        
        self.toon1 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [0], image = self.buttonBgs[0])
        self.toon1.reparentTo(self.patNode2d)
        self.toon1.setPos(-1, 0, 0.5)
        self.toon1.setScale(.5)
        
        self.toon2 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [1], image = self.buttonBgs[1])
        self.toon2.reparentTo(self.patNode2d)
        self.toon2.setPos(-.6, 0, 0.5)
        self.toon2.setScale(.5)
        
        self.toon3 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [2], image = self.buttonBgs[2])
        self.toon3.reparentTo(self.patNode2d)
        self.toon3.setPos(-.2, 0, 0.5)
        self.toon3.setScale(.5)
        
        self.toon4 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [3], image = self.buttonBgs[3])
        self.toon4.reparentTo(self.patNode2d)
        self.toon4.setPos(.2, 0, 0.5)
        self.toon4.setScale(.5)
        
        self.toon5 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [4], image = self.buttonBgs[4])
        self.toon5.reparentTo(self.patNode2d)
        self.toon5.setPos(.6, 0, 0.5)
        self.toon5.setScale(.5)
        
        self.toon6 = DirectButton(text = ' ', relief = None, command=self.selectToon, extraArgs = [5], image = self.buttonBgs[5])
        self.toon6.reparentTo(self.patNode2d)
        self.toon6.setPos(1, 0, 0.5)
        self.toon6.setScale(.5)

#deleteButton
        trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui.bam')
        self.deleteButton = DirectButton(parent=base.a2dBottomRight,
                                         geom=(trashcanGui.find('**/TrashCan_CLSD'),
                                               trashcanGui.find('**/TrashCan_OPEN'),
                                               trashcanGui.find('**/TrashCan_RLVR')),
                                         text=('', TTLocalizer.AvatarChoiceDelete,
                                                   TTLocalizer.AvatarChoiceDelete, ''),
                                         text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                         text_scale=0.15, text_pos=(0, -0.1), relief=None,
                                         scale=.5, command=self.__handleDelete, pos=(-.2, 0, .2))

    def selectToon(self, slot):
        self.selectedToon = slot
        self.updateFunc()
        
    def updateFunc(self):
        haveToon = self.toonList[self.selectedToon]
        if self.jumpIn:
            self.jumpIn.finish()
        if haveToon:
            self.showToon()
            self.deleteButton.show()
        else:
            self.toon.hide()
            self.deleteButton.hide()
        self.checkPlayButton()
            
    def showToon(self):
        av = [x for x in self.avatarList if x.position == self.selectedToon][0]
        dna = av.dna
        
        self.toon.setDNAString(dna)
        #self.jumpIn = Sequence(
        #         Func(self.toon.animFSM.request, 'PATTeleportIn'),
        #         Wait(2),
        #         Func(self.toon.animFSM.request, 'neutral'))
        #self.jumpIn.start() # ALTIS: TODO: Add the states to Toon.py
        self.toon.animFSM.request('neutral')
        self.toon.setName(av.name)
        self.toon.show()
        
    def checkPlayButton(self):
        if self.toonList[self.selectedToon]:
            self.play['text'] = 'PLAY THIS TOON'
            self.play['command'] = self.playGame
        else:
            self.play['text'] = 'MAKE A TOON'
            self.play['command'] = self.makeToon
            
    def playGame(self):
        # TODO: Add some nice animation of the toon teleporting out or stuff
        if self.jumpIn:
            self.jumpIn.finish()
        doneStatus = {"mode": "chose", "choice": self.selectedToon}
        #Sequence (
        #          Func(self.toon.animFSM.request, 'PATTeleportOut'),
        #          Wait(4),
        #          Func(messenger.send, self.doneEvent, [doneStatus]))#.start() # ALTIS: TODO: Add the states to toon.py
        messenger.send(self.doneEvent, [doneStatus])

    def makeToon(self):
        doneStatus = {"mode": "create", "choice": self.selectedToon}
        messenger.send(self.doneEvent, [doneStatus])
        
    def setButtonNames(self):
        for k in self.avatarList:
            if k.position == 0:
                av1 = k
                self.head1 = hidden.attachNewNode('head1')
                self.head1.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head1.reparentTo(self.toon1)
                self.headModel1 = ToonHead.ToonHead()
                self.headModel1.setupHead(ToonDNA.ToonDNA(av1.dna), forGui=1)
                self.headModel1.reparentTo(self.head1)
        
        for k in self.avatarList:
            if k.position == 1:
                av2 = k
                self.head2 = hidden.attachNewNode('head2')
                self.head2.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head2.reparentTo(self.toon2)
                self.headModel2 = ToonHead.ToonHead()
                self.headModel2.setupHead(ToonDNA.ToonDNA(av2.dna), forGui=1)
                self.headModel2.reparentTo(self.head2)
        
        for k in self.avatarList:
            if k.position == 2:
                av3 = k
                self.head3 = hidden.attachNewNode('head3')
                self.head3.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head3.reparentTo(self.toon3)
                self.headModel3 = ToonHead.ToonHead()
                self.headModel3.setupHead(ToonDNA.ToonDNA(av3.dna), forGui=1)
                self.headModel3.reparentTo(self.head3)
        
        for k in self.avatarList:
            if k.position == 3:
                av4 = k
                self.head4 = hidden.attachNewNode('head4')
                self.head4.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head4.reparentTo(self.toon4)
                self.headModel4 = ToonHead.ToonHead()
                self.headModel4.setupHead(ToonDNA.ToonDNA(av4.dna), forGui=1)
                self.headModel4.reparentTo(self.head4)
        
        for k in self.avatarList:
            if k.position == 4:
                av5 = k
                self.head5 = hidden.attachNewNode('head5')
                self.head5.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head5.reparentTo(self.toon5)
                self.headModel5 = ToonHead.ToonHead()
                self.headModel5.setupHead(ToonDNA.ToonDNA(av5.dna), forGui=1)
                self.headModel5.reparentTo(self.head5)
        
        for k in self.avatarList:
            if k.position == 5:
                av6 = k
                self.head6 = hidden.attachNewNode('head6')
                self.head6.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
                self.head6.reparentTo(self.toon6)
                self.headModel6 = ToonHead.ToonHead()
                self.headModel6.setupHead(ToonDNA.ToonDNA(av6.dna), forGui=1)
                self.headModel6.reparentTo(self.head6)

    def unload(self):
        cleanupDialog('globalDialog')
        self.patNode.removeNode()
        del self.patNode
        self.patNode2d.removeNode()
        del self.patNode2d
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        del self.avatarList
        self.toon.removeNode()
        del self.toon
        if self.background is not None:
            self.background.hide()
            self.background.reparentTo(hidden)
            self.background.removeNode()
            self.background = None
        taskMgr.remove('skyTrack')
        self.sky.reparentTo(hidden)
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        return None

    def getChoice(self):
        return self.selectedToon

    def __handleDelete(self):
        messenger.send(self.doneEvent, [{'mode': 'delete'}])

    def __handleQuit(self):
        cleanupDialog('globalDialog')
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])
