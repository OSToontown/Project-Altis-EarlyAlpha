# Embedded file name: toontown.toonfest.DistributedTFBalloon
from pandac.PandaModules import *
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from random import choice
import ToonfestGlobals

class DistributedTFBalloon(DistributedObject, FSM):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'HotAirBalloonFSM')
        self.avId = 0
        self.flightPathIndex = 0
        self.geom = base.cr.playGame.hood.loader.geom
        self.balloon = loader.loadModel('phase_6/models/events/tf_balloon')
        self.balloon.reparentTo(self.geom)
        self.balloon.setPos(ToonfestGlobals.BalloonBaseProperties[0])
        self.balloon.setH(ToonfestGlobals.BalloonBaseProperties[1])
        self.balloon.setScale(ToonfestGlobals.BalloonBaseProperties[2])
        self.cr.parentMgr.registerParent(ToontownGlobals.SPHotAirBalloon, self.balloon)
        self.collisionNP = self.balloon.find('**/basket_wall_collision')
        for count in range(2, 12):
            self.balloon.find('**/fuse' + str(count)).remove()

        self.driver = NPCToons.createLocalNPC(2022)
        self.driver.setPos(2.0, 2.0, 0.2)
        self.driver.setH(150)
        self.driver.setScale(1 / ToonfestGlobals.BalloonBaseProperties[2])
        self.driver.loop('neutral')
        self.driver.initializeBodyCollisions('toon-alec')
        self.driver.addActive()
        self.flightPaths = ToonfestGlobals.generateFlightPaths(self)
        self.toonFlightPaths = ToonfestGlobals.generateToonFlightPaths(self)
        self.speechSequence = ToonfestGlobals.generateSpeechSequence(self)
        self.acceptPassengers = False

    def delete(self):
        self.demand('Off')
        self.ignore('enter' + self.collisionNP.node().getName())
        self.cr.parentMgr.unregisterParent(ToontownGlobals.SPHotAirBalloon)
        self.balloon.removeNode()
        self.driver.delete()
        DistributedObject.delete(self)

    def setState(self, state, timestamp, avId):
        if avId != self.avId:
            self.avId = avId
        self.demand(state, globalClockDelta.localElapsedTime(timestamp))

    def enterWaiting(self, offset):
        self.driver.reparentTo(self.balloon)
        self.accept('enter' + self.collisionNP.node().getName(), self.__handleToonEnter)
        x, y, z = ToonfestGlobals.BalloonBaseProperties[0]
        self.balloonIdle = Sequence(Wait(0.3), self.balloon.posInterval(3, (x, y, z + 1.0)), Wait(0.3), self.balloon.posInterval(3, (x, y, z)))
        if self.balloon.getPos() == ToonfestGlobals.BalloonTowerProperties[0]:
            self.acceptPassengers = False
            self.balloonReturn = Sequence(self.balloon.posHprInterval(1.0, Point3(212, -23, 207), (370, 0, 0), blendType='easeIn'), self.balloon.posHprInterval(2.0, Point3(210, -2, 210), (380, 1, 2)), self.balloon.posHprInterval(4.0, Point3(280, 55, 187), (390, 1, 2)), self.balloon.posHprInterval(8.0, Point3(302, 20, 160), (360, -2, 0)), self.balloon.posHprInterval(5.0, Point3(315, -64, 117), (50, 2, 2)), self.balloon.posHprInterval(5.0, Point3(310, -172, 55), (0, 0, 0)), self.balloon.posHprInterval(1.5, Point3(295, -265, 30), (-80, 2, 2), blendType='easeOut'), Func(self.balloon.setPos, x, y, z), Func(self.balloon.setH, ToonfestGlobals.BalloonBaseProperties[1]), Func(self.balloonIdle.loop), Wait(0.5), Func(self.allowPassengers))
            self.balloonReturn.start()
            self.balloonReturn.setT(offset)
        else:
            print self.balloon.getPos()
            self.acceptPassengers = True
            self.balloon.setPos(x, y, z)
            self.balloon.setH(ToonfestGlobals.BalloonBaseProperties[1])
            self.balloonIdle.loop()
            self.balloonIdle.setT(offset)

    def allowPassengers(self):
        self.acceptPassengers = True

    def __handleToonEnter(self, collEntry):
        if self.avId != 0:
            return
        if self.state != 'Waiting' or not self.acceptPassengers:
            if self.driver.nametag.getChat() == '':
                self.driver.setChatAbsolute('Hey there! Come back when the Fireworks start for a ride to the top of the tower!', CFSpeech | CFTimeout)
            return
        self.sendUpdate('requestEnter', [])

    def exitWaiting(self):
        self.balloonIdle.finish()
        self.ignore('enter' + self.collisionNP.node().getName())

    def enterOccupied(self, offset):
        if self.avId == base.localAvatar.doId:
            base.localAvatar.disableAvatarControls()
            self.hopOnAnim = Sequence(Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPHotAirBalloon), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), Wait(0.3), base.localAvatar.posInterval(0.2, (0, 0, 3)), base.localAvatar.posInterval(0.3, (0, 0, 3)), Func(base.localAvatar.enableAvatarControls), Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender)))
            self.hopOnAnim.start()
        try:
            self.speechSequence = self.speechSequence
            self.speechSequence.start()
            self.speechSequence.setT(offset)
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def exitOccupied(self):
        try:
            self.hopOnAnim.finish()
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def setFlightPath(self, flightPathIndex):
        self.flightPathIndex = flightPathIndex

    def enterStartRide(self, offset):
        try:
            self.rideSequence = self.flightPaths[self.flightPathIndex]
            self.rideSequence.start()
            self.rideSequence.setT(offset)
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

        if self.avId == base.localAvatar.doId:
            try:
                self.toonRideSequence = self.toonFlightPaths[self.flightPathIndex]
                self.toonRideSequence.start()
                self.toonRideSequence.setT(offset)
            except Exception as e:
                self.notify.debug('Exception: %s' % e)

    def exitStartRide(self):
        try:
            self.rideSequence.finish()
            self.speechSequence.finish()
        except Exception as e:
            self.notify.debug('Exception: %s' % e)

    def enterRideOver(self, offset):
        if self.avId == base.localAvatar.doId:
            base.localAvatar.disableAvatarControls()
            self.hopOffAnim = Sequence(Parallel(Func(base.localAvatar.b_setParent, ToontownGlobals.SPRender), Func(base.localAvatar.b_setAnimState, 'jump', 1.0)), Wait(0.3), base.localAvatar.posInterval(0.2, (211, -30, 210)), base.localAvatar.posInterval(0.3, (212, -35, 204)), Wait(0.3), Func(base.localAvatar.enableAvatarControls), Wait(0.3), Func(base.localAvatar.b_setAnimState, 'neutral'))
            self.hopOffAnim.start()