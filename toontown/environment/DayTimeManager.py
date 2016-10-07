from panda3d.core import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
import time
from direct.showbase import PythonUtil
from toontown.hood import Place
from DayTimeGlobals import *

class DayTimeManager(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DayTimeManager')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dayTrack = None
        self.sunTrack = None
        
    def unload(self):
        self.killDaytimeTask()
        if self.dayTrack:
            self.dayTrack.pause()
            self.dayTrack = None
        self.killSunTask()
        if self.sunTrack:
            self.sunTrack.pause()
            self.sunTrack = None

    def setDawnTime(self, ts):
        self.notify.debug('setDawnTime')
        self.dawnTime = ts
        self.sendUpdate('requestServerTime', [])

    def setServerTime(self, ts):
        self.notify.debug('setServerTime')
        self.serverTime = ts
        self.clientTime = time.time() % DayTimeGlobals.DAY_NIGHT_PERIOD
        self.deltaTime = self.clientTime - self.serverTime
        if base.dayNightEnabled:
            self.initDaytimeTask()
            self.initSunTask()

    def getDeltaTime(self):
        curTime = time.time() % DayTimeGlobals.DAY_NIGHT_PERIOD
        dawnTime = self.dawnTime
        dT = (curTime - dawnTime - self.deltaTime) % DayTimeGlobals.DAY_NIGHT_PERIOD
        self.notify.debug(
            'getDeltaTime = %s. curTime=%s. dawnTime=%s. serverTime=%s.  deltaTime=%s'
            % (dT, curTime, dawnTime, self.serverTime, self.deltaTime))
        return dT

    def initDaytimeTask(self):
        self.killDaytimeTask()
        task = Task(self.dayTimeTask)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task, self.taskName('daytime'))

    def killDaytimeTask(self):
        taskMgr.remove(self.taskName('daytime'))

    def dayTimeTask(self, task):
        taskName = self.taskName('daytime')
        track = Sequence(Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, DayTimeGlobals.HALF_DAY_PERIOD, Vec4(1, 0.6, 0.6, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, DayTimeGlobals.HALF_DAY_PERIOD, Vec4(1, 0.8, 0.8, 1))), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, DayTimeGlobals.HALF_NIGHT_PERIOD, Vec4(0.2, 0.2, 0.5, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, DayTimeGlobals.HALF_NIGHT_PERIOD, Vec4(0.4, 0.4, 0.6, 1))), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, DayTimeGlobals.HALF_NIGHT_PERIOD, Vec4(0.6, 0.6, 0.8, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, DayTimeGlobals.HALF_NIGHT_PERIOD, Vec4(0.7, 0.7, 0.8, 1))), Parallel(LerpColorScaleInterval(base.cr.playGame.hood.loader.geom, DayTimeGlobals.HALF_DAY_PERIOD, Vec4(1, 1, 1, 1)), LerpColorScaleInterval(base.cr.playGame.hood.sky, DayTimeGlobals.HALF_DAY_PERIOD, Vec4(1, 1, 1, 1))), Func(base.cr.playGame.hood.loader.geom.clearColorScale), Func(base.cr.playGame.hood.sky.clearColorScale))
        if self.dayTrack:
            self.dayTrack.finish()
        self.dayTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
        self.dayTrack.start(ts)
        taskMgr.doMethodLater(DayTimeGlobals.DAY_NIGHT_PERIOD - ts, self.dayTimeTask, self.taskName('daytime'))
        return Task.done

    def initSunTask(self):
        self.killSunTask()
        task = Task(self.sunTask)
        dT = self.getDeltaTime()
        task.ts = dT
        taskMgr.add(task, self.taskName('sunTask'))

    def killSunTask(self):
        taskMgr.remove(self.taskName('sunTask'))

    def sunTask(self, task):
        sunMoonNode = base.cr.playGame.hood.loader.sunMoonNode
        sun = base.cr.playGame.hood.loader.sun
        h = 30
        halfPeriod = DayTimeGlobals.DAY_NIGHT_PERIOD / 2.0
        track = Sequence(Parallel(LerpHprInterval(sunMoonNode, DayTimeGlobals.HALF_DAY_PERIOD, Vec3(0, 0, 0)), LerpColorScaleInterval(sun, DayTimeGlobals.HALF_DAY_PERIOD, Vec4(1, 1, 0.5, 1))), Func(sun.clearColorScale), Func(self.stopBirds), LerpHprInterval(sunMoonNode, 0.2, Vec3(0, -h - 3, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, -h + 2, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, -h - 1.5, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, -h, 0)), Func(self.notify.debug, 'night'), Wait(DayTimeGlobals.HALF_NIGHT_PERIOD - 0.5), LerpHprInterval(sunMoonNode, DayTimeGlobals.HALF_NIGHT_PERIOD, Vec3(0, 0, 0)), Func(self.startBirds), LerpHprInterval(sunMoonNode, 0.2, Vec3(0, h + 3, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, h - 2, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, h + 1.5, 0)), LerpHprInterval(sunMoonNode, 0.1, Vec3(0, h, 0)), Func(self.notify.debug, 'day'), Func(sunMoonNode.setHpr, 0, h, 0), Wait(DayTimeGlobals.HALF_DAY_PERIOD - 0.5))
        if self.sunTrack:
            self.sunTrack.finish()
        self.sunTrack = track
        ts = 0
        if hasattr(task, 'ts'):
            ts = task.ts
            if ts > DayTimeGlobals.HALF_DAY_PERIOD and ts < DayTimeGlobals.DAY_NIGHT_PERIOD - DayTimeGlobals.HALF_DAY_PERIOD:
                self.stopBirds()
                self.startCrickets()
            else:
                self.stopCrickets()
                self.startBirds()
        self.sunTrack.start(ts)
        taskMgr.doMethodLater(DayTimeGlobals.DAY_NIGHT_PERIOD - ts, self.sunTask, self.taskName('sunTask'))
        return Task.done

    def stopBirds(self):
        taskMgr.remove('estate-birds')

    def startBirds(self):
        self.stopBirds()
        taskMgr.doMethodLater(1, self.birds, 'estate-birds')

    def birds(self, task):
        base.playSfx(random.choice(base.cr.playGame.hood.loader.birdSound))
        t = random.random() * 20.0 + 1
        taskMgr.doMethodLater(t, self.birds, 'estate-birds')
        return Task.done

    def stopCrickets(self):
        taskMgr.remove('estate-crickets')

    def startCrickets(self):
        self.stopCrickets()
        taskMgr.doMethodLater(1, self.crickets, 'estate-crickets')

    def crickets(self, task):
        sfx = random.choice(base.cr.playGame.hood.loader.cricketSound)
        track = Sequence(Func(base.playSfx, sfx), Wait(1))
        track.start()
        t = random.random() * 20.0 + 1
        taskMgr.doMethodLater(t, self.crickets, 'estate-crickets')
        return Task.done