# Embedded file name: toontown.toonfest.DistributedTFTower
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from pandac.PandaModules import NodePath
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.gui.DirectGui import *
ChangeDirectionDebounce = 1.0
ChangeDirectionTime = 1.0

class DistributedTFTower(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        layerOneDict = {}
        layerTwoDict = {}
        layerThreeDict = {}
        self.layerList = [layerOneDict, layerTwoDict, layerThreeDict]
        self.layerStrings = ['LayerOne', 'LayerTwo', 'LayerThree']
        for target in self.layerList:
            target['spinStartTime'] = 0.0
            target['rpm'] = 0.0
            target['degreesPerSecond'] = target['rpm'] / 60.0 * 360.0
            target['offset'] = 0.0
            target['oldOffset'] = 0.0
            target['lerpStart'] = 0.0
            target['lerpFinish'] = 1.0
            target['lastChangeDirection'] = 0.0

        self.speedUpSound = None
        self.changeDirectionSound = None
        self.muteTower = False
        self.nameText = DirectFrame(relief=None, text='', text_font=ToontownGlobals.getSignFont(), text_fg=(0.0, 0.98, 0.5, 1), text_scale=0.15, text_pos=(0, -0.1), pos=(0, 0, 0.86))
        self.nameText.setTransparency(1)
        self.nameText.hide()
        self.randomizeText = DirectFrame(relief=None, text='', text_font=ToontownGlobals.getSignFont(), text_fg=(1, 0.92, 0.2, 1), text_scale=0.1, text_pos=(0, -0.18), pos=(0, 0, 0.86))
        self.randomizeText.setTransparency(1)
        self.randomizeText.hide()
        self.textSequence = Parallel(Func(self.nameText.show), Func(self.randomizeText.show), Sequence(self.nameText.scaleInterval(0.5, 1.0, 0.3), self.nameText.scaleInterval(0.2, 1.1), self.nameText.scaleInterval(0.2, 1.0)), Sequence(self.nameText.colorScaleInterval(0.4, (1, 1, 1, 1), (1, 1, 1, 0)), Wait(4.0), self.nameText.colorScaleInterval(0.4, (1, 1, 1, 0), (1, 1, 1, 1)), Func(self.nameText.hide)), Sequence(self.randomizeText.scaleInterval(0.5, 1.0, 0.3), self.randomizeText.scaleInterval(0.2, 1.1), self.randomizeText.scaleInterval(0.2, 1.0)), Sequence(self.randomizeText.colorScaleInterval(0.4, (1, 1, 1, 1), (1, 1, 1, 0)), Wait(4.0), self.randomizeText.colorScaleInterval(0.4, (1, 1, 1, 0), (1, 1, 1, 1)), Func(self.randomizeText.hide)))
        return

    def generate(self):
        self.layerOne = base.cr.playGame.hood.loader.base1
        self.layerTwo = base.cr.playGame.hood.loader.base2
        self.layerThree = base.cr.playGame.hood.loader.base3
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTower1, self.layerOne)
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTower2, self.layerTwo)
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTower3, self.layerThree)
        self.accept('mutePlaygroundActivity', self.__muteTower)
        self.accept('unmutePlaygroundActivity', self.__unmuteTower)
        self.accept('enterbase1_collision', self.__handleOnFloor, [self.layerStrings[0]])
        self.accept('exitbase1_collision', self.__handleOffFloor)
        self.accept('enterbase2_collision', self.__handleOnFloor, [self.layerStrings[1]])
        self.accept('exitbase2_collision', self.__handleOffFloor)
        self.accept('enterbase3_collision', self.__handleOnFloor, [self.layerStrings[2]])
        self.accept('exitbase3_collision', self.__handleOffFloor)
        tower = base.cr.playGame.hood.loader.body
        sign = base.cr.playGame.hood.loader.sign
        self.towerScale = Sequence(tower.scaleInterval(0.25, (1.0, 1.0, 0.9), (1.0, 1.0, 1.0), blendType='easeInOut'), tower.scaleInterval(0.25, (1.0, 1.0, 1.0), blendType='easeInOut'))
        self.towerHpr = Parallel(Sequence(Wait(0.1), tower.hprInterval(1.4, (0.0, 0.0, 7.0), (0.0, 0.0, -7.0), blendType='easeInOut'), Wait(0.1), tower.hprInterval(1.4, (0.0, 0.0, -7.0), blendType='easeInOut')), Sequence(sign.hprInterval(1.5, (-10.0, 0.0, 0.0), (10.0, 0.0, 0.0), blendType='easeInOut'), sign.hprInterval(1.5, (10.0, 0.0, 0.0), blendType='easeInOut')))
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        self.speedUpSound = base.loadSfx('phase_4/audio/sfx/MG_Tag_C.ogg')
        self.slowDownSound = base.loadSfx('phase_4/audio/sfx/MG_Tag_A.ogg')
        self.changeDirectionSound = base.loadSfx('phase_13/audio/sfx/bounce1.ogg')
        self.__startSpin()
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTower1)
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTower2)
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTower3)
        self.ignore('mutePlaygroundActivity')
        self.ignore('unmutePlaygroundActivity')
        self.ignore('enterbase1_collisions')
        self.ignore('exitbase1_collisions')
        self.ignore('enterbase2_collisions')
        self.ignore('exitbase2_collisions')
        self.ignore('enterbase3_collisions')
        self.ignore('exitbase3_collisions')
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.textSequence.finish()
        self.textSequence = None
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.muteTower = None
        self.__stopSpin()
        del self.layerOne
        del self.layerTwo
        del self.layerThree
        del self.layerList
        del self.layerStrings
        del self.nameText
        del self.randomizeText
        return

    def __muteTower(self):
        self.muteTower = True

    def __unmuteTower(self):
        self.muteTower = False

    def __startSpin(self):
        for layer in self.layerStrings:
            taskMgr.add(self.__updateSpin, self.taskName('towerSpin' + layer + 'Task'), extraArgs=[layer])

    def __stopSpin(self):
        self.towerScale.finish()
        self.towerHpr.finish()
        for layer in self.layerStrings:
            taskMgr.remove(self.taskName('towerSpin' + layer + 'Task'))

    def __updateSpin(self, layer):
        if layer == 'LayerOne':
            node = self.layerOne
            var = self.layerList[0]
        elif layer == 'LayerTwo':
            node = self.layerTwo
            var = self.layerList[1]
        elif layer == 'LayerThree':
            node = self.layerThree
            var = self.layerList[2]
        now = globalClock.getFrameTime()
        if now > var['lerpFinish']:
            offset = var['offset']
        elif now > var['lerpStart']:
            t = (now - var['lerpStart']) / (var['lerpFinish'] - var['lerpStart'])
            offset = var['oldOffset'] + t * (var['offset'] - var['oldOffset'])
        else:
            offset = var['oldOffset']
        heading = var['degreesPerSecond'] * (now - var['spinStartTime']) + offset
        node.setHpr(heading % 360.0, 0.0, 0.0)
        return Task.cont

    def setLayerOneSpeed(self, rpm, offset, timestamp, layer):
        self.setSpeed(rpm, offset, timestamp, layer)

    def setLayerTwoSpeed(self, rpm, offset, timestamp, layer):
        self.setSpeed(rpm, offset, timestamp, layer)

    def setLayerThreeSpeed(self, rpm, offset, timestamp, layer):
        self.setSpeed(rpm, offset, timestamp, layer)

    def setSpeed(self, rpm, offset, timestamp, layer):
        if layer == 'LayerOne':
            var = self.layerList[0]
        elif layer == 'LayerTwo':
            var = self.layerList[1]
        elif layer == 'LayerThree':
            var = self.layerList[2]
        timestamp = globalClockDelta.networkToLocalTime(timestamp)
        degreesPerSecond = rpm / 60.0 * 360.0
        now = globalClock.getFrameTime()
        oldHeading = var['degreesPerSecond'] * (now - var['spinStartTime']) + var['offset']
        oldHeading = oldHeading % 360.0
        oldOffset = oldHeading - degreesPerSecond * (now - timestamp)
        var['rpm'] = rpm
        var['degreesPerSecond'] = degreesPerSecond
        var['offset'] = offset
        var['spinStartTime'] = timestamp
        while oldOffset - offset < -180.0:
            oldOffset += 360.0

        while oldOffset - offset > 180.0:
            oldOffset -= 360.0

        var['oldOffset'] = oldOffset
        var['lerpStart'] = now
        var['lerpFinish'] = timestamp + ChangeDirectionTime

    def playTextEffect(self):
        if self.textSequence.isPlaying():
            self.textSequence.finish()
        self.textSequence.start()

    def playSpeedUp(self, avId):
        if not self.muteTower:
            av = base.cr.doId2do.get(avId)
            if not av:
                return
            self.nameText['text'] = av.getName()
            if len(av.getName()) > 20:
                self.nameText['text_scale'] = 0.13
            elif len(av.getName()) > 30:
                self.nameText['text_scale'] = 0.11
            self.randomizeText['text'] = TTLocalizer.ToonfestTowerSpeedup
            self.playTextEffect()
            base.playSfx(self.speedUpSound)

    def playSlowDown(self, avId):
        if not self.muteTower:
            av = base.cr.doId2do.get(avId)
            if not av:
                return
            self.nameText['text'] = av.getName()
            if len(av.getName()) > 20:
                self.nameText['text_scale'] = 0.13
            elif len(av.getName()) > 30:
                self.nameText['text_scale'] = 0.11
            self.randomizeText['text'] = TTLocalizer.ToonfestTowerSlowdown
            self.playTextEffect()
            base.playSfx(self.slowDownSound)

    def playChangeDirection(self, avId):
        if not self.muteTower:
            av = base.cr.doId2do.get(avId)
            if not av:
                return
            self.nameText['text'] = av.getName()
            if len(av.getName()) > 20:
                self.nameText['text_scale'] = 0.13
            elif len(av.getName()) > 30:
                self.nameText['text_scale'] = 0.11
            self.randomizeText['text'] = TTLocalizer.ToonfestTowerReverse
            self.playTextEffect()
            base.playSfx(self.changeDirectionSound)

    def __handleOnFloor(self, layer, collEntry):
        base.cr.playGame.getPlace().activityFsm.request('On' + layer)

    def __handleOffFloor(self, collEntry):
        base.cr.playGame.getPlace().activityFsm.request('off')

    def __handleSpeedUpButton(self, collEntry, layer):
        self.sendUpdate('requestSpeedUp', [layer])
        if not self.muteTower:
            base.playSfx(self.speedUpSound)

    def __handleChangeDirectionButton(self, collEntry, layer):
        now = globalClock.getFrameTime()
        if now - self.lastChangeDirection < ChangeDirectionDebounce:
            return
        self.lastChangeDirection = now
        self.sendUpdate('requestChangeDirection', [layer])
        if not self.muteTower:
            base.playSfx(self.changeDirectionSound)