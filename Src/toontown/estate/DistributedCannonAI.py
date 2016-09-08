from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
import CannonGlobals
from toontown.minigame import CannonGameGlobals
from toontown.toonbase.ToontownGlobals import PinballCannonBumperInitialPos


class DistributedCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCannonAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.estateId = 0
        self.targetId = 0
        self.avId = 0
        self.cannonsActive = 0
        self.posHpr = (0, 0, 0, 0, 0, 0)
        self.cannonBumperPos = PinballCannonBumperInitialPos

    def setEstateId(self, estateId):
        self.estateId = estateId
        
    def getEstateId(self):
        return self.estateId

    def setTargetId(self, targetId):
        self.targetId = targetId
    
    def getTargetId(self):
        return self.targetId

    def setPosHpr(self, x, y, z, h, p, r):
        self.posHpr = (x, y, z, h, p, r)
        
    def getPosHpr(self):
        return self.posHpr
    
    def d_setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [x, y, z, h, p, r])

    def setActive(self, active):
        self.cannonsActive = active

    def setActiveState(self, active):
        self.sendUpdate('setActiveState', [active])

    def requestEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId == 0 or self.avId == avId:
            self.avId = avId
            self.d_setMovie(CannonGlobals.CANNON_MOVIE_LOAD, self.avId)
            self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        else:
            self.air.writeServerEvent('suspicious', avId, 'DistributedCannonAI.requestEnter cannon already occupied')
            self.notify.warning('requestEnter() - cannon already occupied')

    def requestExit(self):
        pass

    def d_setMovie(self, mode, avId):
        self.sendUpdate('setMovie', [mode, avId])

    def setCannonPosition(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        self.sendUpdate('updateCannonPosition', [avId, zRot, angle])        

    def setCannonLit(self, zRot, angle):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        fireTime = CannonGameGlobals.FUSE_TIME
        self.sendUpdate('setCannonWillFire', [avId,
         fireTime,
         zRot,
         angle,
         globalClockDelta.getRealNetworkTime()])

    def setFired(self):
        pass

    def setLanded(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            return
        self.d_setMovie(CannonGlobals.CANNON_MOVIE_LANDED, avId)

    def updateCannonPosition(self, todo0, todo1, todo2):
        pass

    def setCannonWillFire(self, todo0, todo1, todo2, todo3, todo4):
        pass

    def setCannonExit(self, todo0):
        pass

    def requestBumperMove(self, x, y, z):
        self.b_setCannonBumperPos(x, y, z)

    def b_setCannonBumperPos(self, x, y, z):
        self.setCannonBumperPos(x, y, z)
        self.d_setCannonBumperPos(x, y, z)
        
    def setCannonBumperPos(self, x, y, z):
        self.cannonBumperPos = (x, y, z)
    
    def d_setCannonBumperPos(self, x, y, z):
        self.sendUpdate('setCannonBumperPos', [x, y, z])

    def getCannonBumperPos(self):
        return self.cannonBumperPos

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.__doExit()

    def __doExit(self):
        if self.isDeleted():
            return
        if not hasattr(self, 'avId'):
            return
        if not self.avId:
            return
        self.ignore('distObjDelete-%d' % self.avId)
        self.d_setMovie(CannonGlobals.CANNON_MOVIE_FORCE_EXIT, self.avId)
        self.avId = 0
