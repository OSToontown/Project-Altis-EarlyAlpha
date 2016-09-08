from direct.task import Task
import random
from pandac.PandaModules import Vec3, Point3

from toontown.classicchars import CCharPaths
from toontown.safezone import Playground
from toontown.toonbase import TTLocalizer


class DGPlayground(Playground.Playground):
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self.__birds, 'DG-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('DG-birds')

    def showPaths(self):
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Goofy))

    def __birds(self, task):
        base.playSfx(random.choice(self.loader.birdSound))
        time = random.random() * 20.0 + 1
        taskMgr.doMethodLater(time, self.__birds, 'DG-birds')
        return Task.done