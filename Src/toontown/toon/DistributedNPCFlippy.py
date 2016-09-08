from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
import time

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.nametag.NametagGlobals import * 
from toontown.effects import DustCloud
from toontown.nametag import NametagGroup
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.hood import PGHood

class DistributedNPCFlippy(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

        self.pickColorGui = None
        self.pickColorGuiDoneEvent = 'pickColorGuiDone'

        self.nextCollision = 0

        self.fsm = ClassicFSM.ClassicFSM(
            'NPCFlippy',
            [
                State.State('off', self.enterOff, self.exitOff, ['pick']),
                State.State('pick', self.enterPick, self.exitPick, ['off'])
            ], 'off', 'off')
        self.fsm.enterInitialState()

        self.title = None
        self.yesButton = None
        self.noButton = None

        self.buttonModels = loader.loadModel('phase_4/models/gui/gag_shop_purchase_gui')
        self.upButton = self.buttonModels.find('**//PurchScrn_BTN_UP')
        self.downButton = self.buttonModels.find('**/PurchScrn_BTN_DN')
        self.rolloverButton = self.buttonModels.find('**/PurchScrn_BTN_RLVR')

    def disable(self):
        self.ignoreAll()

        if self.title:
            self.title.destroy()
            self.title = None

        if self.yesButton:
            self.yesButton.destroy()
            self.yesButton = None

        if self.noButton:
            self.noButton.destroy()
            self.noButton = None

        if self.buttonModels:
            self.buttonModels.removeNode()
            self.buttonModels = None

        if self.upButton:
            self.upButton.removeNode()
            self.upButton = None

        if self.downButton:
            self.downButton.removeNode()
            self.downButton = None

        if self.rolloverButton:
            self.rolloverButton.removeNode()
            self.rolloverButton = None

        if self.pickColorGui:
            self.pickColorGui.destroy()
            self.pickColorGui = None

        self.nextCollision = 0

        DistributedNPCToonBase.disable(self)

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        self.setPosHpr(-8, -74, 0, 378, 0, 0)
        self.setHat(12, 0, 0)

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        self.currentTime = time.time()
        if self.nextCollision <= self.currentTime:
            self.fsm.request('pick')
        self.nextCollision = self.currentTime + 2

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterPick(self):
    	base.cr.playGame.getPlace().setState('stopped')
        taskMgr.doMethodLater(15, self.leave, 'npcSleepTask-%s' % self.doId)
        self.popupGUI()

    def exitPick(self, task=None):
        taskMgr.remove('npcSleepTask-%s' % self.doId)
        if self.yesButton:
            self.yesButton.destroy()
            self.yesButton = None
        if self.noButton:
            self.noButton.destroy()
            self.noButton = None

        if task is not None:
            return task.done

    def popupGUI(self):
        self.setChatAbsolute('', CFSpeech)
        if isinstance(base.cr.playGame.getPlace().loader.hood, PGHood.PGHood):
            self.setChatAbsolute(TTLocalizer.FlippySummerLeave, CFSpeech)
        else:
            self.setChatAbsolute(TTLocalizer.YinPickColor, CFSpeech)
        base.setCellsActive(base.bottomCells, 0)

   
        self.yesButton = DirectButton(
            relief=None, text='Yeah!',
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23),
            text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton),
            image_scale=(6.7, 1, 6), pos=(-0.275, 0, -0.75), scale=0.15,
            command=lambda self=self: self.d_requestTeleportation())
        self.noButton = DirectButton(
            relief=None, text="Nah.",
            text_fg=(1, 1, 0.65, 1), text_pos=(0, -0.23),
            text_scale=0.8, image=(self.upButton, self.downButton, self.rolloverButton),
            image_scale=(9, 1, 6), pos=(0.275, 0, -0.75), scale=0.15,
            command=lambda self=self: self.leave())

    def d_requestTeleportation(self):
        if isinstance(base.cr.playGame.getPlace().loader.hood, PGHood.PGHood):
            base.localAvatar.magicTeleportInitiate(2000, 2000)
        else:
            base.localAvatar.magicTeleportInitiate(7000, 7000)
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')

    def leave(self, task=None):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.YinGoodbye, CFSpeech|CFTimeout)
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)

        if task is not None:
            return task.done

