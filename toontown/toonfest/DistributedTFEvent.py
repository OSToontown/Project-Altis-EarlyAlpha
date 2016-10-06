from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from otp.nametag.NametagConstants import *
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.election import ElectionGlobals
from toontown.toon import NPCToons, Toon
from toontown.pets import Pet
import DistributedTFTower
import ToonfestGlobals
import random

class DistributedTFEvent(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTFEvent')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.geom = base.cr.playGame.hood.loader.geom
        self.hasFlippyStand = False
        self.hasCogdummies = False
        self.muteEvent = False
        self.dayTrack = None
        self.sunTrack = None
        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.loop('neutral')
        self.flippy.setPos(178.6, -265.6, 5.2)
        self.flippy.setH(100)
        self.flippySequence = Sequence(Func(self.flippy.setChatAbsolute, 'Welcome Toons, far and wide!', CFSpeech | CFTimeout), ActorInterval(self.flippy, 'wave'), Func(self.flippy.loop, 'neutral'), Wait(8.0), Func(self.flippy.setChatAbsolute, "It's been an amazing year at Toontown, and we're glad you could join us!", CFSpeech | CFTimeout), Wait(8.0), Func(self.flippy.setChatAbsolute, "Oh, don't mind the little guy back there. That's Fluffy!", CFSpeech | CFTimeout), Wait(6.0), Func(self.flippy.setChatAbsolute, "I found him here last year, and he's been my best pal ever since.", CFSpeech | CFTimeout), Wait(7.0), Func(self.flippy.setChatAbsolute, "He does seem to have a problem with wandering off whenever we're around here, though...", CFSpeech | CFTimeout), Wait(7.0), Func(self.flippy.setChatAbsolute, 'Doctor Surlee says he\'s some sort of creature called a "Doodle". Funny name, right?', CFSpeech | CFTimeout), Wait(8.0), Func(self.flippy.setChatAbsolute, 'Anyway, what are you waiting for?', CFSpeech | CFTimeout), ActorInterval(self.flippy, 'shrug'), Func(self.flippy.loop, 'neutral'), Wait(6.0), Func(self.flippy.setChatAbsolute, 'Grab some pies, catch some fish, and go for a spin. ToonFest is in full swing!', CFSpeech | CFTimeout), Wait(10.0))
        self.flippySequence.loop()
        self.flippy.reparentTo(self.geom)
        self.flippy.initializeBodyCollisions('toon-flippy')
        self.flippy.addActive()
        self.fluffy = Pet.Pet()
        self.fluffy.setDNA(ToontownGlobals.NPCDoodleDNA['Fluffy'])
        self.fluffySequence = Sequence(Func(self.fluffy.loop, 'neutralHappy'), Wait(4.0), ActorInterval(self.fluffy, 'toDig'), Func(self.fluffy.loop, 'dig'), Wait(1.5), ActorInterval(self.fluffy, 'fromDig'), Func(self.fluffy.loop, 'neutralHappy'), Wait(4.0), ActorInterval(self.fluffy, 'jump'), Func(self.fluffy.loop, 'neutralHappy'), Wait(4.0), ActorInterval(self.fluffy, 'dance'), Func(self.fluffy.loop, 'neutralHappy'), Wait(4.0), ActorInterval(self.fluffy, 'backflip'), Func(self.fluffy.loop, 'neutralHappy'))
        self.fluffySequence.loop()
        self.fluffy.loop('dance')
        self.fluffy.setPos(183.7, -269, 5.3)
        self.fluffy.setH(-37)
        self.fluffy.setName(TTLocalizer.NPCDoodleNames['Fluffy'])
        self.fluffy.reparentTo(self.geom)
        self.fluffy.initializeBodyCollisions('pet-fluffy')
        self.fluffy.setPickable(0)
        self.fluffy.addActive()
        self.activeSequences = []
        self.restockSfx = None

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        Toon.loadMinigameAnims()
        self.defaultSignModel = loader.loadModel('phase_13/models/parties/eventSign')
        self.activityIconsModel = loader.loadModel('phase_4/models/parties/eventSignIcons')
        self.initializeFlippyStand()
        self.requestServerTime()
        self.accept('mutePlaygroundActivity', self.__muteEvent)
        self.accept('unmutePlaygroundActivity', self.__unmuteEvent)

    def disable(self):
        if self.dayTrack:
            self.dayTrack.finish()
        if self.sunTrack:
            self.sunTrack.finish()
        for sequence in self.activeSequences:
            sequence.finish()

        self.flippySequence.finish()
        self.fluffySequence.finish()
        if self.hasFlippyStand:
            self.flippyStand.cleanup()
        if self.hasCogDummies:
            self.ignore('localPieSplat')
            for cog in self.cogDummies:
                cog.cleanup()

        self.ignore('mutePlaygroundActivity')
        self.ignore('unmutePlaygroundActivity')
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        for sequence in self.activeSequences:
            del sequence

        del self.activeSequences
        del self.flippySequence
        del self.fluffySequence
        self.flippy.delete()
        self.fluffy.delete()
        if self.hasFlippyStand:
            self.flippyStand.removeNode()
            self.pieCollision.removeNode()
            self.restockSfx = None
        if self.hasCogDummies:
            for cog in self.cogDummies:
                cog.removeNode()

            for hole in self.cogHoles:
                hole.removeNode()

        taskMgr.remove(self.taskName('daytime'))
        taskMgr.remove(self.taskName('sunTask'))
        del self.serverTime
        del self.dayTrack
        del self.sunTrack
        DistributedObject.DistributedObject.delete(self)

    def __muteEvent(self):
        self.muteEvent = True
        base.cr.playGame.hood.loader.fadeClouds(0)

    def __unmuteEvent(self):
        self.muteEvent = False
        base.cr.playGame.hood.loader.fadeClouds(1)

    def initializeFlippyStand(self):
        self.hasFlippyStand = True
        self.flippyStand = Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        self.flippyStand.reparentTo(self.geom)
        self.flippyStand.setPosHprScale(172, -254, 4.85, -55, 1, -8, 0.55, 0.55, 0.55)
        self.flippyStand.exposeJoint(None, 'modelRoot', 'LInnerShoulder')
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None, 'modelRoot', 'Box_Joint')
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint').attachNewNode('Pie_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.39, 0.0, 1.77, 0.0, 0.0, 6.0, 1.14, 1.54, 0.93)
        pie = loader.loadModel('phase_3.5/models/props/tart')
        pieS = pie.copyTo(flippyTable)
        pieS.setPosHprScale(-2.61, -0.37, -1.99, 355.6, 90.0, 4.09, 1.6, 1.6, 1.6)
        for pieSettings in ElectionGlobals.FlippyWheelbarrowPies:
            pieModel = pie.copyTo(wheelbarrowJoint)
            pieModel.setPosHprScale(*pieSettings)

        wheelbarrowJoint.setPosHprScale(3.94, 0.0, 1.06, 270.0, 344.74, 0.0, 1.43, 1.12, 1.0)
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)
        self.flippyStand.loop('idle')

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            if not self.restockSfx:
                return
            self.sendUpdate('wheelbarrowAvatarEnter', [])
            self.restockSfx.play()
        else:
            self.notify.debug('Avatar requested pies, but has the max amount!')

    def initializeCogDummies(self):
        self.hasCogDummies = True
        self.accept('localPieSplat', self.__localPieSplat)
        self.popupSequence = Sequence()
        path = 'phase_13/models/parties/cogPinata_'
        self.cog1 = Actor(path + 'actor', {'idle': path + 'idle_anim',
         'down': path + 'down_anim',
         'up': path + 'up_anim',
         'bodyHitBack': path + 'bodyHitBack_anim',
         'bodyHitFront': path + 'bodyHitFront_anim',
         'headHitBack': path + 'headHitBack_anim',
         'headHitFront': path + 'headHitFront_anim'})
        self.cog2 = Actor(path + 'actor', {'idle': path + 'idle_anim',
         'down': path + 'down_anim',
         'up': path + 'up_anim',
         'bodyHitBack': path + 'bodyHitBack_anim',
         'bodyHitFront': path + 'bodyHitFront_anim',
         'headHitBack': path + 'headHitBack_anim',
         'headHitFront': path + 'headHitFront_anim'})
        self.cog3 = Actor(path + 'actor', {'idle': path + 'idle_anim',
         'down': path + 'down_anim',
         'up': path + 'up_anim',
         'bodyHitBack': path + 'bodyHitBack_anim',
         'bodyHitFront': path + 'bodyHitFront_anim',
         'headHitBack': path + 'headHitBack_anim',
         'headHitFront': path + 'headHitFront_anim'})
        self.cogDummies = [self.cog1, self.cog2, self.cog3]
        cogNum = 1
        for cog in self.cogDummies:
            cog.reparentTo(self.geom)
            cog.loop('idle')
            bodyColl = CollisionTube(0, 0, 1, 0, 0, 5.75, 1.0)
            bodyColl.setTangible(1)
            bodyCollNode = CollisionNode('PartyCog%s-Body-Collision' % cogNum)
            bodyCollNode.setTag('pieCode', str(ToontownGlobals.PieCodePinata))
            bodyCollNode.addSolid(bodyColl)
            cog.attachNewNode(bodyCollNode)
            cogNum += 1

        self.cogHoles = []
        for holePoint in ToonfestGlobals.CogHolePopupPoints:
            hole = loader.loadModel('phase_13/models/parties/cogPinataHole')
            hole.setTransparency(True)
            hole.setPos(holePoint[0])
            hole.setP(-90)
            hole.setScale(3)
            hole.setBin('ground', 3)
            hole.reparentTo(self.geom)
            self.cogHoles.append(hole)

    def startCogPopupPoint(self, cogIndex, point, currentPos = -1):
        if cogIndex == 0:
            cog = self.cog1
            popupPoints = list(ToonfestGlobals.Cog1PopupPoints)
        elif cogIndex == 1:
            cog = self.cog2
            popupPoints = list(ToonfestGlobals.Cog2PopupPoints)
        elif cogIndex == 2:
            cog = self.cog3
            popupPoints = list(ToonfestGlobals.Cog3PopupPoints)
        else:
            self.notify.error('Recieved invalid cogIndex: %s' % cogIndex)
            return
        if currentPos != -1:
            popupPoints.pop(currentPos)
        pos = popupPoints[point][0]
        h = popupPoints[point][1]
        x, y, z = pos
        self.cogHitSound = loader.loadSfx('phase_11/audio/sfx/LB_evidence_hit.ogg')
        popupSequence = Sequence(Parallel(ActorInterval(cog, 'down'), Sequence(Wait(0.87), cog.scaleInterval(0.5, 0.8))), Func(cog.setPos, (x, y, z - 0.2)), Func(cog.setH, h), Parallel(ActorInterval(cog, 'up', endFrame=27), cog.scaleInterval(0.3, 1.0)), Func(cog.loop, 'idle'), autoFinish=1)
        self.activeSequences.append(popupSequence)
        taskMgr.doMethodLater(2, self.activeSequences.remove, 'removeSequence', [popupSequence])
        popupSequence.start()

    def __localPieSplat(self, pieCode, entry):
        if pieCode == ToontownGlobals.PieCodePinata:
            colPath = 'PartyCog%s-Body-Collision'
            if colPath % 1 in str(entry.getIntoNode()):
                cog = self.cog1
                cogIndex = 0
            elif colPath % 2 in str(entry.getIntoNode()):
                cog = self.cog2
                cogIndex = 1
            elif colPath % 3 in str(entry.getIntoNode()):
                cog = self.cog3
                cogIndex = 2
            Sequence(ActorInterval(cog, 'headHitFront', endFrame=17), Func(cog.loop, 'idle'), autoFinish=1).start()
            if not self.muteEvent:
                base.playSfx(self.cogHitSound, volume=0.5, node=cog)
            self.sendUpdate('randomizeTowerEvent', [cogIndex])

    def playCogHit(self, cogIndex, avId):
        if cogIndex == 0:
            cog = self.cog1
        elif cogIndex == 1:
            cog = self.cog2
        elif cogIndex == 2:
            cog = self.cog3
        if avId != base.localAvatar.doId and not self.muteEvent:
            base.playSfx(self.cogHitSound, volume=0.5, node=cog)

    def requestServerTime(self):
        self.sendUpdate('requestServerTime', [])

    def sendServerTime(self, elapsedTime):
        self.serverTime = elapsedTime
        self.__initDaytimeTask()
        self.__initSunTask()

    def __initDaytimeTask(self):
        self.__killDaytimeTask()
        task = Task(self.__dayTimeTask)
        task.ts = self.serverTime
        taskMgr.add(task, self.taskName('daytime'))

    def __killDaytimeTask(self):
        taskMgr.remove(self.taskName('daytime'))

    def __dayTimeTask(self, task):
        taskName = self.taskName('daytime')
        transitionPeriod = ToonfestGlobals.NighttimeCycle / 8
        fullDay = ToonfestGlobals.DaytimeCycle + ToonfestGlobals.NighttimeCycle
        track = Sequence(Func(base.cr.playGame.hood.skyNight.setColorScale, 0.4, 0.4, 0.6, 1), Wait(transitionPeriod), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, transitionPeriod, Vec4(0.6, 0.6, 0.8, 1), startColorScale=Vec4(0.3, 0.3, 0.45, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, transitionPeriod, Vec4(0.7, 0.7, 0.8, 1), startColorScale=Vec4(0.4, 0.4, 0.6, 1)), LerpColorScaleInterval(base.cr.playGame.hood.skyNight, transitionPeriod, Vec4(1, 1, 1, 0))), Wait(transitionPeriod), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, transitionPeriod, Vec4(1, 1, 1, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, transitionPeriod, Vec4(1, 1, 1, 1))), Func(base.cr.playGame.hood.loader.geom.clearColorScale), Func(base.cr.playGame.hood.sky.clearColorScale), Func(base.cr.playGame.hood.skySunset.setColorScale, 1, 1, 1, 0), Func(base.cr.playGame.hood.skyNight.setColorScale, 1, 1, 1, 0), Wait(ToonfestGlobals.DaytimeCycle), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, transitionPeriod, Vec4(1, 0.6, 0.6, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, transitionPeriod, Vec4(1, 0.8, 0.8, 1)), LerpColorScaleInterval(base.cr.playGame.hood.skySunset, transitionPeriod, Vec4(1, 0.8, 0.8, 1))), Wait(transitionPeriod), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, transitionPeriod, Vec4(0.3, 0.3, 0.45, 1)), LerpColorScaleInterval(base.cr.playGame.hood.skySunset, transitionPeriod, Vec4(0.4, 0.4, 0.6, 0)), LerpColorScaleInterval(base.cr.playGame.hood.skyNight, transitionPeriod, Vec4(0.4, 0.4, 0.6, 1))), Wait(transitionPeriod))
        if self.dayTrack:
            self.dayTrack.finish()
        self.dayTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
        self.dayTrack.start(ts)
        taskMgr.doMethodLater(fullDay - ts, self.__dayTimeTask, self.taskName('daytime'))
        return Task.done

    def __initSunTask(self):
        self.__killSunTask()
        task = Task(self.__sunTask)
        task.ts = self.serverTime
        taskMgr.add(task, self.taskName('sunTask'))

    def __killSunTask(self):
        taskMgr.remove(self.taskName('sunTask'))

    def __sunTask(self, task):
        sunMoonNode = base.cr.playGame.hood.loader.sunMoonNode
        sun = base.cr.playGame.hood.loader.sun
        h = 50
        transitionPeriod = ToonfestGlobals.NighttimeCycle / 4
        fullDay = ToonfestGlobals.DaytimeCycle + ToonfestGlobals.NighttimeCycle
        track = Sequence(Wait(transitionPeriod), LerpHprInterval(sunMoonNode, transitionPeriod, Vec3(0, -h, 0)), Wait(ToonfestGlobals.DaytimeCycle), Parallel(LerpHprInterval(sunMoonNode, transitionPeriod * 2, Vec3(0, h, 0)), LerpColorScaleInterval(sun, transitionPeriod * 2, Vec4(1, 1, 0.5, 1))), Func(sun.clearColorScale))
        if self.sunTrack:
            self.sunTrack.finish()
        self.sunTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
        self.sunTrack.start(ts)
        taskMgr.doMethodLater(fullDay - ts, self.__sunTask, self.taskName('sunTask'))
        return Task.done
