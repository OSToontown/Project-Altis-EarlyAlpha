from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase import ToontownTimer
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedTarget(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTarget')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.geom = None
        self.numConsecutiveHits = 0
        self.enabled = 0
        self.score = 0
        self.hitTime = 0
        self.targetBounceTrack = None
        self.pinballInfo = {}
        self.pinballHiScore = 0
        self.pinballHiScorer = ''
        self.onscreenMessage = None
        self.fadeTrack = None
        return

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)
        if self.targetBounceTrack:
            self.targetBounceTrack.finish()
            self.targetBounceTrack = None
        if self.fadeTrack:
            self.fadeTrack.pause()
            self.fadeTrack = None
        return

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.load()

    def load(self):
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.setPos(1.1, 0, -0.15)
        self.timer.hide()
        self.geom = loader.loadModel('phase_5.5/models/estate/target')
        self.geom.reparentTo(base.cr.playGame.hood.loader.geom)
        self.geom.setPos(0, 0, 40)
        self.geom.setScale(3)
        self.geom.stash()
        self.hitSound = base.loadSfx('phase_4/audio/sfx/MG_Tag_A.ogg')
        self.rewardSound = base.loadSfx('phase_4/audio/sfx/MG_pos_buzzer.ogg')
        self.scoreText = TextNode('scoreText')
        self.scoreText.setTextColor(1, 0, 0, 1)
        self.scoreText.setAlign(self.scoreText.ACenter)
        self.scoreText.setFont(getSignFont())
        self.scoreText.setText('0')
        self.scoreNode = self.timer.attachNewNode(self.scoreText)
        self.scoreNode.setPos(0, 0, 0.35)
        self.scoreNode.setScale(0.25)
        self.curPinballScoreText = TextNode('pinballScoreText')
        self.curPinballScoreText.setTextColor(1, 0, 0, 1)
        self.curPinballScoreText.setAlign(self.scoreText.ACenter)
        self.curPinballScoreText.setFont(getSignFont())
        self.curPinballScoreText.setText('')
        self.curPinballScoreNode = render.attachNewNode(self.curPinballScoreText)
        self.curPinballScoreNode.setPos(0.5, 0.5, 0.3)
        self.curPinballScoreNode.setScale(0.25)
        colSphere = CollisionSphere(0, 0, 0, 3.5)
        colSphere.setTangible(0)
        colNode = CollisionNode('targetSphere')
        colNode.addSolid(colSphere)
        colSphereNode = self.geom.attachNewNode(colNode)
        self.accept('hitTarget', self.handleHitTarget)
        self.accept('missedTarget', self.handleMissedTarget)
        self.accept('entertargetSphere', self.handleEnterTarget)

    def delete(self):
        self.ignoreAll()
        self.scoreNode.removeNode()
        del self.scoreNode
        self.curPinballScoreNode.removeNode()
        del self.curPinballScoreNode
        self.geom.removeNode()
        del self.geom
        self.timer.destroy()
        del self.timer
        del self.rewardSound
        del self.hitSound
        DistributedObject.DistributedObject.delete(self)

    def setState(self, enabled, score, time):
        if self.enabled != enabled:
            if self.fadeTrack:
                self.fadeTrack.pause()
            if enabled:
                self.fadeTrack = Sequence(Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameStart), Func(self.geom.unstash), self.geom.colorScaleInterval(1.0, Vec4(1.0, 1.0, 1.0, 1.0)), Wait(1), Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameInst))
            else:
                self.fadeTrack = Sequence(self.geom.colorScaleInterval(1.0, Vec4(1.0, 1.0, 1.0, 0.0)), Func(self.geom.stash), Func(self.hideTimer), Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameEnd))
            self.fadeTrack.start()
            self.enabled = enabled
        if score != self.score:
            self.setLevel(score)

    def setReward(self, reward):
        base.playSfx(self.rewardSound)

    def handleEnterTarget(self, collEntry):
        self.handleHitTarget()

    def handleHitTarget(self, avId = None, vel = None):
        if not avId:
            avId = base.localAvatar.doId
        if self.enabled:
            self.sendUpdate('setResult', [avId])
        if vel:
            if self.targetBounceTrack:
                self.targetBounceTrack.finish()
            pos = self.geom.getPos()
            dist = Vec3(vel)
            dist.normalize()
            newPos = pos - dist * 1.5
            springPos = pos + dist
            self.notify.debug('reaction distance = %s,%s,%s' % (vel[0], vel[1], vel[2]))
            self.targetBounceTrack = Sequence(LerpPosInterval(self.geom, duration=0.1, pos=newPos, blendType='easeOut'), LerpPosInterval(self.geom, duration=0.25, pos=springPos, blendType='easeOut'), LerpPosInterval(self.geom, duration=0.2, pos=pos, blendType='easeOut'))
            self.targetBounceTrack.start()

    def handleMissedTarget(self):
        if self.enabled:
            self.sendUpdate('setResult', [0])

    def handleHitCloud(self):
        if self.enabled:
            self.sendUpdate('setBonus', [0.5])

    def setLevel(self, level):
        self.notify.debug('setLevel(%s)' % level)
        self.score = level
        self.scoreText.setText('+' + str(int(self.score)))


    def setPosition(self, x, y, z):
        self.geom.setPos(x, y, z)

    def setCurPinballScore(self, avId, score, multiplier):
        self.notify.debug('setCurPinballScore %d %d %d' % (avId, score, multiplier))
        if self.pinballInfo.get(avId) == None:
            self.pinballInfo[avId] = [0, 0, 0]
        pinballEntry = self.pinballInfo[avId]
        pinballEntry[1] = score
        pinballEntry[2] = multiplier
        curScore = score * multiplier
        if curScore > pinballEntry[0]:
            pinballEntry[0] = curScore
        if curScore > self.pinballHiScore:
            self.pinballHiScore = pinballEntry[0]
            toon = base.cr.doId2do.get(avId)
            if toon:
                self.pinballHiScorer = toon.getName()
        return

    def b_setCurPinballScore(self, avId, score, multiplier):
        self.setCurPinballScore(avId, score, multiplier)
        self.sendUpdate('setCurPinballScore', [avId, score, multiplier])

    def setPinballHiScore(self, score):
        self.pinballHiScore = score
        self.showScore()

    def setPinballHiScorer(self, name):
        self.pinballHiScorer = name
        self.showScore()

    def hideGui(self):
        pass

    def showGui(self):
        pass
