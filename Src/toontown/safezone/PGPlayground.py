from direct.task.Task import Task
from direct.fsm import ClassicFSM, State
import random

from toontown.classicchars import CCharPaths
from toontown.safezone import Playground
from toontown.toonbase import TTLocalizer


class PGPlayground(Playground.Playground):
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.fsm.addState(State.State('activity', self.enterActivity, self.exitActivity, ['walk', 'stopped']))
        self.fsm.getStateNamed('walk').addTransition('activity')

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)

    def enterActivity(self, setAnimState = True):
        if setAnimState:
            base.localAvatar.b_setAnimState('neutral', 1)
        self.accept('teleportQuery', self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(False)
        base.localAvatar.laffMeter.start()

    def exitActivity(self):
        base.localAvatar.setTeleportAvailable(True)
        self.ignore('teleportQuery')
        base.localAvatar.laffMeter.stop()