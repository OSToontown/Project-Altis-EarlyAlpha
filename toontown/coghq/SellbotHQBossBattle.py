from panda3d.core import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedSellbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class SellbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotHQBossBattle')

    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        self.teleportInPosHpr = (0, 95, 18, 180, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus, DistributedSellbotBoss.OneBossCog)
        self.__setupHighSky()

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)
        self.__cleanupHighSky()

    def startSky(self):
        self.sky = loader.loadModel('phase_9/models/cogHQ/cog_sky')
        self.sky.reparentTo(camera)
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        self.sky.setBin('background', 0)

    def stopSky(self):
        taskMgr.remove('skyTrack')
        self.sky.removeNode()

    def __setupHighSky(self):
        self.startSky()
        sky = self.sky
        sky.setH(250)
        sky.setZ(-200)

    def __cleanupHighSky(self):
        sky = self.sky
        sky.setH(0)
        sky.setZ(0)
        self.stopSky()
