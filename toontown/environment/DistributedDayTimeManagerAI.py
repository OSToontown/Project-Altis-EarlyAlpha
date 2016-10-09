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

    def start(self):
        DistributedWeatherMGRAI.start(self)
                
        Sequence(
            Func(self.b_setState, 'T0'),
            Wait(20),
            Func(self.b_setState, 'T1'),
            Wait(20),
            Func(self.b_setState, 'T2'),
            Wait(20),
            Func(self.b_setState, 'T3'),
            Wait(20),
            Func(self.b_setState, 'T4'),
            Wait(20),
            Func(self.b_setState, 'T5'),
            Wait(20),
            Func(self.b_setState, 'T6'),
            Wait(20),
            Func(self.b_setState, 'T7'),
            Wait(20),
            Func(self.b_setState, 'T8'),
            Wait(20),
            Func(self.b_setState, 'T9'),
            Wait(20),
            Func(self.b_setState, 'T10'),
            Wait(20),
            Func(self.b_setState, 'T11'),
            Wait(20),
            Func(self.b_setState, 'T12'),
            Wait(20),
            Func(self.b_setState, 'T11'),
            Wait(20),
            Func(self.b_setState, 'T10'),
            Wait(20),
            Func(self.b_setState, 'T9'),
            Wait(20),
            Func(self.b_setState, 'T8'),
            Wait(20),
            Func(self.b_setState, 'T7'),
            Wait(20),
            Func(self.b_setState, 'T6'),
            Wait(20),
            Func(self.b_setState, 'T5'),
            Wait(20),
            Func(self.b_setState, 'T4'),
            Wait(20),
            Func(self.b_setState, 'T3'),
            Wait(20),
            Func(self.b_setState, 'T2'),
            Wait(20),
            Func(self.b_setState, 'T1'),      
            Wait(20)).loop()
            
            
    def enterT0(self):
        pass
        
    def exitT0(self):
        pass
        
    def enterT1(self):
        pass
        
    def exitT1(self):
        pass
        
    def enterT2(self):
        pass
        
    def exitT2(self):
        pass
        
    def enterT3(self):
        pass
        
    def exitT3(self):
        pass
        
    def enterT4(self):
        pass
        
    def exitT4(self):
        pass
        
    def enterT5(self):
        pass
        
    def exitT5(self):
        pass
        
    def enterT6(self):
        pass
        
    def exitT6(self):
        pass
        
    def enterT7(self):
        pass
        
    def exitT7(self):
        pass
        
    def enterT8(self):
        pass
        
    def exitT8(self):
        pass
        
    def enterT9(self):
        pass
        
    def exitT9(self):
        pass
        
    def enterT10(self):
        pass
        
    def exitT10(self):
        pass
        
    def enterT11(self):
        pass
        
    def exitT11(self):
        pass
        
    def enterT12(self):
        pass
        
    def exitT12(self):
        pass
        
    # TODO: Add the next 12 hours, for now im just going to use this in reverse to go to night