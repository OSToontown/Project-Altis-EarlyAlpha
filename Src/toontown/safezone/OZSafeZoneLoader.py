import copy
from direct.actor import Actor
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import random

from otp.avatar import Avatar
from otp.otpbase import OTPGlobals
from toontown.distributed import DelayDelete
from toontown.effects import Bubbles
from toontown.hood import ZoneUtil
from toontown.safezone.OZPlayground import OZPlayground
from toontown.safezone.SafeZoneLoader import SafeZoneLoader
from toontown.toon import Toon, ToonDNA
from toontown.pets import Pet
from toontown.nametag import *
from toontown.nametag.NametagGlobals import *
from toontown.nametag.NametagGroup import *
from toontown.toonbase import ToontownGlobals
from toontown.chat.ChatGlobals import *

class OZSafeZoneLoader(SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.musicFile = 'phase_6/audio/bgm/OZ_SZ.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/GS_KartShop.ogg'
        self.dnaFile = 'phase_6/dna/outdoor_zone_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_OZ_sz.pdna'
        self.__toonTracks = {}
        del self.fsm
        self.fsm = ClassicFSM.ClassicFSM('SafeZoneLoader', [State.State('start', self.enterStart, self.exitStart, ['quietZone', 'playground', 'toonInterior']),
         State.State('playground', self.enterPlayground, self.exitPlayground, ['quietZone', 'golfcourse']),
         State.State('toonInterior', self.enterToonInterior, self.exitToonInterior, ['quietZone']),
         State.State('quietZone', self.enterQuietZone, self.exitQuietZone, ['playground', 'toonInterior', 'golfcourse']),
         State.State('golfcourse', self.enterGolfCourse, self.exitGolfCourse, ['quietZone', 'playground']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def load(self):
        self.done = 0
        self.geyserTrack = None
        SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.ogg', 'phase_4/audio/sfx/SZ_TC_bird2.ogg', 'phase_4/audio/sfx/SZ_TC_bird3.ogg'])
        self.underwaterSound = base.loadSfx('phase_4/audio/sfx/AV_ambient_water.ogg')
        self.swimSound = base.loadSfx('phase_4/audio/sfx/AV_swim_single_stroke.ogg')
        self.submergeSound = base.loadSfx('phase_5.5/audio/sfx/AV_jump_in_water.ogg')
        geyserPlacer = self.geom.find('**/geyser*')
        waterfallPlacer = self.geom.find('**/waterfall*')
        binMgr = CullBinManager.getGlobalPtr()
        binMgr.addBin('water', CullBinManager.BTFixed, 29)
        binMgr = CullBinManager.getGlobalPtr()
        pool = self.geom.find('**/pPlane5*')
        pool.setTransparency(1)
        pool.setColorScale(1.0, 1.0, 1.0, 1.0)
        pool.setBin('water', 50, 1)
        self.geyserModel = loader.loadModel('phase_6/models/golf/golf_geyser_model')
        self.geyserSound = loader.loadSfx('phase_6/audio/sfx/OZ_Geyser.ogg')
        self.geyserSoundInterval = SoundInterval(self.geyserSound, node=geyserPlacer, listenerNode=base.camera, seamlessLoop=False, volume=1.0, cutOff=120)
        self.geyserSoundNoToon = loader.loadSfx('phase_6/audio/sfx/OZ_Geyser_No_Toon.ogg')
        self.geyserSoundNoToonInterval = SoundInterval(self.geyserSoundNoToon, node=geyserPlacer, listenerNode=base.camera, seamlessLoop=False, volume=1.0, cutOff=120)
        if self.geyserModel:
            self.geyserActor = Actor.Actor(self.geyserModel)
            self.geyserActor.loadAnims({'idle': 'phase_6/models/golf/golf_geyser'})
            self.geyserActor.reparentTo(render)
            self.geyserActor.setPlayRate(8.6, 'idle')
            self.geyserActor.loop('idle')
            self.geyserActor.setDepthWrite(0)
            self.geyserActor.setTwoSided(True, 11)
            self.geyserActor.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.geyserActor.setBin('fixed', 0)
            mesh = self.geyserActor.find('**/mesh_tide1')
            joint = self.geyserActor.find('**/uvj_WakeWhiteTide1')
            mesh.setTexProjector(mesh.findTextureStage('default'), joint, self.geyserActor)
            self.geyserActor.setPos(geyserPlacer.getPos())
            self.geyserActor.setZ(geyserPlacer.getZ() - 100.0)
            self.geyserPos = geyserPlacer.getPos()
            self.geyserPlacer = geyserPlacer
            self.startGeyser()
            base.sfxPlayer.setCutoffDistance(160)
            self.geyserPoolSfx = loader.loadSfx('phase_6/audio/sfx/OZ_Geyser_BuildUp_Loop.ogg')
            self.geyserPoolSoundInterval = SoundInterval(self.geyserPoolSfx, node=self.geyserPlacer, listenerNode=base.camera, seamlessLoop=True, volume=1.0, cutOff=120)
            self.geyserPoolSoundInterval.loop()
            self.bubbles = Bubbles.Bubbles(self.geyserPlacer, render)
            self.bubbles.renderParent.setDepthWrite(0)
            self.bubbles.start()
        self.collBase = render.attachNewNode('collisionBase')
        self.geyserCollSphere = CollisionSphere(0, 0, 0, 7.5)
        self.geyserCollSphere.setTangible(1)
        self.geyserCollNode = CollisionNode('barrelSphere')
        self.geyserCollNode.setIntoCollideMask(OTPGlobals.WallBitmask)
        self.geyserCollNode.addSolid(self.geyserCollSphere)
        self.geyserNodePath = self.collBase.attachNewNode(self.geyserCollNode)
        self.geyserNodePath.setPos(self.geyserPos[0], self.geyserPos[1], self.geyserPos[2] - 100.0)
        self.waterfallModel = loader.loadModel('phase_6/models/golf/golf_waterfall_model')
        if self.waterfallModel:
            self.waterfallActor = Actor.Actor(self.waterfallModel)
            self.waterfallActor.loadAnims({'idle': 'phase_6/models/golf/golf_waterfall'})
            self.waterfallActor.reparentTo(render)
            self.waterfallActor.setPlayRate(2.5, 'idle')
            self.waterfallActor.loop('idle')
            mesh = self.waterfallActor.find('**/mesh_tide1')
            joint = self.waterfallActor.find('**/uvj_WakeWhiteTide1')
            mesh.setTexProjector(mesh.findTextureStage('default'), joint, self.waterfallActor)
        self.waterfallActor.setPos(waterfallPlacer.getPos())
        self.accept('clientLogout', self._handleLogout)

        #Remove the orignal TB entrance
        self.geom.find('**/prop_outdoor_zone_entrance_DNARoot').removeNode()

        #Load in the destroyed one
        self.destroyedEntrance = loader.loadModel('phase_6/models/golf/oz_entrance_destroyed')
        self.destroyedEntrance.reparentTo(render)
        self.destroyedEntrance.setPosHpr(-47.8387, -143.259, 0.1, 180, 0, 0.1)

        self.constructionSite = render.attachNewNode('constructionSite')

        self.constructionCollision = self. constructionSite.attachNewNode(CollisionNode('constructionCollision'))
        self.constructionCollision.setPos(-48, -169.50, 0)
        self.constructionCollision.node().addSolid(CollisionSphere(0, 0, 0, 35))

        self.constructionSign = loader.loadModel('phase_4/models/props/construction_sign')
        self.constructionSign.reparentTo(render)
        self.constructionSign.find('**/o16').hide()
        self.constructionSign.find('**/o16_1').hide()
        self.constructionSign.find('**/stand').hide()
        self.constructionSign.find('**/post').hide()
        self.sign = self.constructionSign.find('**/sign_board')
        self.sign.setPosHpr(-37, -104.50, -0.50, 180, 0, 0)
        self.sign.setScale(3)

        self.replacedLog = self.destroyedEntrance.find('**/outdoor_zone_entrance1:outdoor_zone_entrance_pCylinder7')
        self.replacedLog.setPos(3, 0, 0)
        self.replacedLog.setScale(0.75)


        #Load in Fluffy
        self.fluffy = Pet.Pet()
        self.fluffy.setDNA(ToontownGlobals.FluffyDNA['Fluffy'])
        self.fluffy.setPosHpr(-47, -146, 0, 17.10, 0, 0)
        self.fluffy.setName('Fluffy')
        self.fluffy.reparentTo(render)
        self.fluffy.initializeBodyCollisions('pet')
        self.fluffy.setPickable(0)
        self.fluffy.addActive()
        self.fluffySequence = Sequence(
        Func(self.fluffy.setChatAbsolute, "Can someone help me find my home? I think it's in \x01WLRed\x01 those mountains.", CFSpeech|CFTimeout),
        Wait(8),
        Func(self.fluffy.setChatAbsolute, "The mountains there. Oh I can't remember the name..Come on think Fluffy think!", CFSpeech|CFTimeout),
        Wait(8),
        Func(self.fluffy.loop, 'jump'),
        Func(self.fluffy.setChatAbsolute, "Oh I just can't remember! It's right on my tail but I just can't.", CFSpeech|CFTimeout),
        Func(self.fluffy.loop, 'neutralSad'),
        Wait(8),
        Func(self.fluffy.loop, 'dig'),
        Func(self.fluffy.setChatAbsolute, "This dirt is almost as hard as rock! What is under this anyways?", CFSpeech|CFTimeout),
        Func(self.fluffy.loop, 'neutralSad'),
        Wait(8),
        Func(self.fluffy.setChatAbsolute, "I'll be so happy once I see Flippy again!", CFSpeech|CFTimeout),
        Wait(9),
        )
        self.fluffySequence.loop()


    def exit(self):
        self.clearToonTracks()
        SafeZoneLoader.exit(self)
        self.ignore('clientLogout')

    def startGeyser(self, task = None):
        if hasattr(base.cr, 'DTimer') and base.cr.DTimer:
            self.geyserCycleTime = 20.0
            useTime = base.cr.DTimer.getTime()
            timeToNextGeyser = 20.0 - useTime % 20.0
            taskMgr.doMethodLater(timeToNextGeyser, self.doGeyser, 'geyser Task')
        else:
            taskMgr.doMethodLater(5.0, self.startGeyser, 'start geyser Task')

    def doGeyser(self, task = None):
        if not self.done:
            self.setGeyserAnim()
            useTime = base.cr.DTimer.getTime()
            timeToNextGeyser = 20.0 - useTime % 20.0
            taskMgr.doMethodLater(timeToNextGeyser, self.doGeyser, 'geyser Task')
        return task.done

    def restoreLocal(self, task = None):
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.collisionsOn()
        base.localAvatar.dropShadow.show()

    def restoreRemote(self, remoteAv, task = None):
        if remoteAv in Avatar.Avatar.ActiveAvatars:
            remoteAv.startSmooth()
            remoteAv.dropShadow.show()

    def setGeyserAnim(self, task = None):
        if self.done:
            return
        maxSize = 0.4 * random.random() + 0.75
        time = 1.0
        self.geyserTrack = Sequence()
        upPos = Vec3(self.geyserPos[0], self.geyserPos[1], self.geyserPos[2])
        downPos = Vec3(self.geyserPos[0], self.geyserPos[1], self.geyserPos[2] - 8.0)
        avList = copy.copy(Avatar.Avatar.ActiveAvatars)
        avList.append(base.localAvatar)
        playSound = 0
    
        self.geyserTrack.append(Func(self.doPrint, 'geyser start'))
        self.geyserTrack.append(Func(self.geyserNodePath.setPos, self.geyserPos[0], self.geyserPos[1], self.geyserPos[2]))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, 2.0 * time, 0.75, 0.01), LerpPosInterval(self.geyserActor, 2.0 * time, pos=downPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.75), LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, 2.0 * time, 0.75, maxSize), LerpPosInterval(self.geyserActor, 2.0 * time, pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.75), LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, 2.0 * time, 0.75, maxSize), LerpPosInterval(self.geyserActor, 2.0 * time, pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.75), LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, 4.0 * time, 0.01, maxSize), LerpPosInterval(self.geyserActor, 4.0 * time, pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Func(self.geyserNodePath.setPos, self.geyserPos[0], self.geyserPos[1], self.geyserPos[2] - 100.0))
        self.geyserTrack.append(Func(self.doPrint, 'geyser end'))
        self.geyserTrack.start()
        if playSound:
            self.geyserSoundInterval.start()
        else:
            self.geyserSoundNoToonInterval.start()

    def changeCamera(self, newParent, newPos, newHpr):
        camera.reparentTo(newParent)
        camera.setPosHpr(newPos, newHpr)

    def doPrint(self, thing):
        return 0
        print thing

    def unload(self):
        del self.birdSound
        SafeZoneLoader.unload(self)
        self.done = 1
        self.collBase.removeNode()
        if self.geyserTrack:
            self.geyserTrack.finish()
        self.geyserTrack = None
        self.geyserActor.cleanup()
        self.geyserModel.removeNode()
        self.waterfallActor.cleanup()
        self.waterfallModel.removeNode()
        self.bubbles.destroy()
        del self.bubbles
        self.geyserPoolSoundInterval.finish()
        self.geyserPoolSfx.stop()
        self.geyserPoolSfx = None
        self.geyserPoolSoundInterval = None
        self.geyserSoundInterval.finish()
        self.geyserSound.stop()
        self.geyserSoundInterval = None
        self.geyserSound = None
        self.geyserSoundNoToonInterval.finish()
        self.geyserSoundNoToon.stop()
        self.geyserSoundNoToonInterval = None
        self.geyserSoundNoToon = None

        self.constructionCollision.removeNode()
        del self.constructionCollision

        if self.constructionSign is not None:
            self.constructionSign.removeNode()
            self.constructionSign = None
        self.replacedLog.removeNode()
        self.destroyedEntrance.removeNode()
        self.sign.removeNode()
        del self.replacedLog
        del self.destroyedEntrance
        del self.sign

        self.fluffySequence.finish()
        self.fluffy.delete()
		
    def enterPlayground(self, requestStatus):
        self.playgroundClass = OZPlayground
        SafeZoneLoader.enterPlayground(self, requestStatus)

    def exitPlayground(self):
        taskMgr.remove('titleText')
        self.hood.hideTitleText()
        SafeZoneLoader.exitPlayground(self)
        self.playgroundClass = None
        return

    def handlePlaygroundDone(self):
        status = self.place.doneStatus
        self.doneStatus = status
        messenger.send(self.doneEvent)

    def enteringARace(self, status):
        if not status['where'] == 'golfcourse':
            return 0
        if ZoneUtil.isDynamicZone(status['zoneId']):
            return status['hoodId'] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId(status['zoneId']) == self.hood.hoodId

    def enteringAGolfCourse(self, status):
        if not status['where'] == 'golfcourse':
            return 0
        if ZoneUtil.isDynamicZone(status['zoneId']):
            return status['hoodId'] == self.hood.hoodId
        else:
            return ZoneUtil.getHoodId(status['zoneId']) == self.hood.hoodId

    def enterGolfCourse(self, requestStatus):
        if 'curseId' in requestStatus:
            self.golfCourseId = requestStatus['courseId']
        else:
            self.golfCourseId = 0
        self.accept('raceOver', self.handleRaceOver)
        self.accept('leavingGolf', self.handleLeftGolf)
        base.transitions.irisOut(t=0.2)

    def exitGolfCourse(self):
        del self.golfCourseId

    def handleRaceOver(self):
        print 'you done!!'

    def handleLeftGolf(self):
        req = {'loader': 'safeZoneLoader',
         'where': 'playground',
         'how': 'teleportIn',
         'zoneId': 6000,
         'hoodId': 6000,
         'shardId': None}
        self.fsm.request('quietZone', [req])
        return

    def _handleLogout(self):
        self.clearToonTracks()

    def storeToonTrack(self, avId, track):
        self.clearToonTrack(avId)
        self.__toonTracks[avId] = track

    def clearToonTrack(self, avId):
        oldTrack = self.__toonTracks.get(avId)
        if oldTrack:
            oldTrack.pause()
            DelayDelete.cleanupDelayDeletes(oldTrack)
            del self.__toonTracks[avId]

    def clearToonTracks(self):
        keyList = []
        for key in self.__toonTracks:
            keyList.append(key)

        for key in keyList:
            if key in self.__toonTracks:
                self.clearToonTrack(key)
