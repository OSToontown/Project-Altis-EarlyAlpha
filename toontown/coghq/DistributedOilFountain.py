from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from pandac.PandaModules import NodePath
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *

class DistributedOilFountain(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOilFountain')
    GEAR_INDEX = xrange(12)
    GEYSER_INDEX = xrange(1, 5)

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.gearLerps = []
        self.geysers = []

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.geom = self.cr.playGame.hood.loader.geom

    def announceGenerate(self):
        self.geyser = loader.loadModel('phase_12/models/bossbotHQ/ttr_m_ara_bbhq_geyser')
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        self.stopGearLoop()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        del self.gearLerps
        self.geyser.removeNode()
        DistributedObject.DistributedObject.delete(self)

    def startGearLoop(self, timestamp):
        elapsedTime = globalClockDelta.localElapsedTime(timestamp, bits=32)
        if not self.gearLerps:
            parentId = ToontownGlobals.SPDynamic
            for top in self.geom.findAllMatches('**/Fountain_Geom:Top').getPaths():
                self.gearLerps.append(LerpHprInterval(top, 17, (0, 0, 0), (360, 0, 0)))
                base.cr.parentMgr.registerParent(parentId, top)
                parentId += 1

            for mid in self.geom.findAllMatches('**/Fountain_Geom:Middle').getPaths():
                self.gearLerps.append(LerpHprInterval(mid, 17, (0, 0, 0), (-360, 0, 0)))
                base.cr.parentMgr.registerParent(parentId, mid)
                parentId += 1

            for btm in self.geom.findAllMatches('**/Fountain_Geom:Bottom').getPaths():
                self.gearLerps.append(LerpHprInterval(btm, 17, (0, 0, 0), (360, 0, 0)))
                base.cr.parentMgr.registerParent(parentId, btm)
                parentId += 1

            self.startGeyserLoop()
            self.startCollisionListener()
        for lerp in self.gearLerps:
            lerp.loop()
            lerp.pause()
            lerp.setT(elapsedTime % lerp.getDuration())
            lerp.resume()

    def stopGearLoop(self):
        if self.gearLerps:
            for lerp in self.gearLerps:
                lerp.finish()

            self.gearLerps = []
            self.stopGeyserLoop()
            for colId in self.GEAR_INDEX:
                base.cr.parentMgr.unregisterParent(ToontownGlobals.SPDynamic + colId)

            self.stopCollisionListener()

    def startGeyserLoop(self):
        for nodeId in self.GEYSER_INDEX:
            geyserSpot = self.geom.find('**/Fountain_Geom:fountain_geyser' + str(nodeId))
            geyser = self.geyser.copyTo(geyserSpot)
            self.geysers.append(geyser)

    def stopGeyserLoop(self):
        for geyser in self.geysers:
            geyser.removeNode()

    def startCollisionListener(self):
        for colId in self.GEAR_INDEX:
            self.accept('enterFountain_Geom:gear_floor_coll' + str(colId), self.__handleOnFloor)
            self.accept('exitFountain_Geom:gear_floor_coll' + str(colId), self.__handleOffFloor)

    def __handleOnFloor(self, collision):
        base.localAvatar.b_setParent(ToontownGlobals.SPDynamic + int(collision.getIntoNode().getName()[29:]))

    def __handleOffFloor(self, collision):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def stopCollisionListener(self):
        for colId in self.GEAR_INDEX:
            self.ignore('enterFountain_Geom:gear_floor_coll' + str(colId))
            self.ignore('exitFountain_Geom:gear_floor_coll' + str(colId))
