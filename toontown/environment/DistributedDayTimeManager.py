# TODO: Make the sky texture change

from panda3d.core import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpColorScaleInterval
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
import DayTimeGlobals
from DistributedWeatherMGR import DistributedWeatherMGR

class DistributedDayTimeManager(DistributedWeatherMGR):
    notify = directNotify.newCategory('DistributedDayTimeManager')
    
    def __init__(self, cr):
        DistributedWeatherMGR.__init__(self, cr)
        self.cr = cr
        self.currentTime = None
        self.interval = 100
        self.hood = base.cr.playGame.hood
        self.interval = 150
        
    def announceGenerate(self):
        DistributedWeatherMGR.announceGenerate(self)
        
    def delete(self):
        self.currSeq.finish()
        render.setColorScale(Vec4(1, 1, 1, 1))
        DistributedWeatherMGR.delete(self)
        
    def enterT0(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[0], DayTimeGlobals.COLORS[23])
        self.currSeq.start()
        print 'Daytime Manager: Entered T0'
        
    def exitT0(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT1(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[1], DayTimeGlobals.COLORS[0])
        self.currSeq.start()
        print 'Daytime Manager: Entered T1'
        
    def exitT1(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT2(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[2], DayTimeGlobals.COLORS[1])
        self.currSeq.start()
        print 'Daytime Manager: Entered T2'
        
    def exitT2(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT3(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[3], DayTimeGlobals.COLORS[2])
        self.currSeq.start()
        print 'Daytime Manager: Entered T3'
        
    def exitT3(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT4(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[4], DayTimeGlobals.COLORS[3])
        self.currSeq.start()
        print 'Daytime Manager: Entered T4'
        
    def exitT4(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT5(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[5], DayTimeGlobals.COLORS[4])
        self.currSeq.start()
        print 'Daytime Manager: Entered T5'
        
    def exitT5(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT6(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[6], DayTimeGlobals.COLORS[5])
        self.currSeq.start()
        print 'Daytime Manager: Entered T6'
        
    def exitT6(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT7(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[7], DayTimeGlobals.COLORS[6])
        self.currSeq.start()
        print 'Daytime Manager: Entered T7'
        
    def exitT7(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT8(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[8], DayTimeGlobals.COLORS[7])
        self.currSeq.start()
        print 'Daytime Manager: Entered T8'
        
    def exitT8(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT9(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[9], DayTimeGlobals.COLORS[8])
        self.currSeq.start()
        print 'Daytime Manager: Entered T9'
        
    def exitT9(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT10(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[10], DayTimeGlobals.COLORS[9])
        self.currSeq.start()
        print 'Daytime Manager: Entered T10'
        
    def exitT10(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT11(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[11], DayTimeGlobals.COLORS[10])
        self.currSeq.start()
        print 'Daytime Manager: Entered T11'
        
    def exitT11(self):
        self.currSeq.finish()
        self.currSeq = None
        
    def enterT12(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[12], DayTimeGlobals.COLORS[11])
        self.currSeq.start()
        print 'Daytime Manager: Entered T12'
        
    def exitT12(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT13(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[13], DayTimeGlobals.COLORS[12])
        self.currSeq.start()
        print 'Daytime Manager: Entered T13'

    def exitT13(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT14(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[14], DayTimeGlobals.COLORS[13])
        self.currSeq.start()
        print 'Daytime Manager: Entered T14'

    def exitT14(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT15(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[15], DayTimeGlobals.COLORS[14])
        self.currSeq.start()
        print 'Daytime Manager: Entered T15'

    def exitT15(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT16(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[16], DayTimeGlobals.COLORS[15])
        self.currSeq.start()
        print 'Daytime Manager: Entered T16'

    def exitT16(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT17(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[17], DayTimeGlobals.COLORS[16])
        self.currSeq.start()
        print 'Daytime Manager: Entered T17'

    def exitT17(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT18(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[18], DayTimeGlobals.COLORS[17])
        self.currSeq.start()
        print 'Daytime Manager: Entered T18'

    def exitT18(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT19(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[19], DayTimeGlobals.COLORS[18])
        self.currSeq.start()
        print 'Daytime Manager: Entered T19'

    def exitT19(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT20(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[20], DayTimeGlobals.COLORS[19])
        self.currSeq.start()
        print 'Daytime Manager: Entered T20'

    def exitT20(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT21(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[21], DayTimeGlobals.COLORS[20])
        self.currSeq.start()
        print 'Daytime Manager: Entered T21'

    def exitT21(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT22(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[22], DayTimeGlobals.COLORS[21])
        self.currSeq.start()
        print 'Daytime Manager: Entered T22'

    def exitT22(self):
        self.currSeq.finish()
        self.currSeq = None

    def enterT23(self, timestamp):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[23], DayTimeGlobals.COLORS[22])
        self.currSeq.start()
        print 'Daytime Manager: Entered T23'

    def exitT23(self):
        self.currSeq.finish()
        self.currSeq = None
        
    # TODO: Add the next 12 hours, for now im just going to use this in reverse to go to night, but we should add the next 12 to make it look more like its going into night time, liek make the sky more orange
