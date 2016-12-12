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
import DayTimeGlobals
from DistributedWeatherMGRAI import DistributedWeatherMGRAI

class DistributedDayTimeManagerAI(DistributedWeatherMGRAI):
    notify = directNotify.newCategory('DistributedDayTimeManagerAI')
    
    def __init__(self, air):
        DistributedWeatherMGRAI.__init__(self, air)
        self.air = air

    def start(self):
        DistributedWeatherMGRAI.start(self)
        self.interval = 150
                
        Sequence(
            Func(self.b_setState, 'T0'),
            Wait(self.interval),
            Func(self.b_setState, 'T1'),
            Wait(self.interval),
            Func(self.b_setState, 'T2'),
            Wait(self.interval),
            Func(self.b_setState, 'T3'),
            Wait(self.interval),
            Func(self.b_setState, 'T4'),
            Wait(self.interval),
            Func(self.b_setState, 'T5'),
            Wait(self.interval),
            Func(self.b_setState, 'T6'),
            Wait(self.interval),
            Func(self.b_setState, 'T7'),
            Wait(self.interval),
            Func(self.b_setState, 'T8'),
            Wait(self.interval),
            Func(self.b_setState, 'T9'),
            Wait(self.interval),
            Func(self.b_setState, 'T10'),
            Wait(self.interval),
            Func(self.b_setState, 'T11'),
            Wait(self.interval),
            Func(self.b_setState, 'T12'),
            Wait(self.interval),
            Func(self.b_setState, 'T13'),
            Wait(self.interval),
            Func(self.b_setState, 'T14'),
            Wait(self.interval),
            Func(self.b_setState, 'T15'),
            Wait(self.interval),
            Func(self.b_setState, 'T16'),
            Wait(self.interval),
            Func(self.b_setState, 'T17'),
            Wait(self.interval),
            Func(self.b_setState, 'T18'),
            Wait(self.interval),
            Func(self.b_setState, 'T19'),
            Wait(self.interval),
            Func(self.b_setState, 'T20'),
            Wait(self.interval),
            Func(self.b_setState, 'T21'),
            Wait(self.interval),
            Func(self.b_setState, 'T22'),
            Wait(self.interval),
            Func(self.b_setState, 'T23'),
            Wait(self.interval)).loop()
            
            
    def enterT0(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(0)
        
    def exitT0(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT1(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(1)
        
    def exitT1(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT2(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(2)
        
    def exitT2(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT3(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(3)
        
    def exitT3(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT4(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(4)
        
    def exitT4(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT5(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(5)
        
    def exitT5(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT6(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(6)
        
    def exitT6(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT7(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(7)
        
    def exitT7(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT8(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(8)
        
    def exitT8(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT9(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(9)
        
    def exitT9(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT10(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(10)
        
    def exitT10(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT11(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(11)
        
    def exitT11(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
        
    def enterT12(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(12)
        
    def exitT12(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT13(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(13)

    def exitT13(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT14(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(14)

    def exitT14(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT15(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(15)

    def exitT15(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT16(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(16)

    def exitT16(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT17(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(17)

    def exitT17(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT18(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(18)

    def exitT18(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT19(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(19)

    def exitT19(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT20(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(20)

    def exitT20(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT21(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(21)

    def exitT21(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT22(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(22)

    def exitT22(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None

    def enterT23(self):
        self.currSeq = Sequence(Wait(self.interval)).start()
        self.air.setHour(23)

    def exitT23(self):
        if self.currSeq is not None:
            self.currSeq.finish()
            self.currSeq = None
