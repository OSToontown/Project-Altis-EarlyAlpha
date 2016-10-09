# TODO: Make the sky texture change

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
import DayTimeGlobals
from DistributedWeatherMGR import DistributedWeatherMGR

class DistributedDayTimeManager(DistributedWeatherMGR):
    notify = directNotify.newCategory('DistributedDayTimeManager')
    
    def __init__(self, cr):
        DistributedWeatherMGR.__init__(self, cr)
        self.cr = cr
        self.currentTime = None
        
    def announceGenerate(self):
        DistributedWeatherMGR.announceGenerate(self)
        
    def delete(self):
        render.setColorScale(Vec4(1, 1, 1, 1))
        DistributedWeatherMGR.delete(self)
        
    def enterT0(self, timestamp):
        render.setColorScale(Vec4(0.2, 0.2, 0.4, 1))
        
    def exitT0(self):
        pass
        
    def enterT1(self, timestamp):
        render.setColorScale(Vec4(0.25, 0.25, 0.45, 1))
        
    def exitT1(self):
        pass
        
    def enterT2(self, timestamp):
        render.setColorScale(Vec4(0.4, 0.3, 0.5, 1))
        
    def exitT2(self):
        pass
        
    def enterT3(self, timestamp):
        render.setColorScale(Vec4(0.45, 0.35, 0.55, 1))
        
    def exitT3(self):
        pass
        
    def enterT4(self, timestamp):
        render.setColorScale(Vec4(0.45, 0.40, 0.6, 1))
        
    def exitT4(self):
        pass
        
    def enterT5(self, timestamp):
        render.setColorScale(Vec4(0.45, 0.45, 0.65, 1))
        
    def exitT5(self):
        pass
        
    def enterT6(self, timestamp):
        render.setColorScale(Vec4(0.5, 0.5, 0.7, 1))
        
    def exitT6(self):
        pass
        
    def enterT7(self, timestamp):
        render.setColorScale(Vec4(0.6, 0.6, 0.75, 1))
        
    def exitT7(self):
        pass
        
    def enterT8(self, timestamp):
        render.setColorScale(Vec4(0.68, 0.68, 0.8, 1))
        
    def exitT8(self):
        pass
        
    def enterT9(self, timestamp):
        render.setColorScale(Vec4(0.75, 0.85, 0.85, 1))
        
    def exitT9(self):
        pass
        
    def enterT10(self, timestamp):
        render.setColorScale(Vec4(0.85, 0.85, 0.9, 1))
        
    def exitT10(self):
        pass
        
    def enterT11(self, timestamp):
        render.setColorScale(Vec4(0.95, 0.95, 0.95, 1))
        
    def exitT11(self):
        pass
        
    def enterT12(self, timestamp):
        render.setColorScale(Vec4(1.0, 1.0, 1.0, 1))
        
    def exitT12(self):
        pass
        
    # TODO: Add the next 12 hours, for now im just going to use this in reverse to go to night, but we should add the next 12 to make it look more like its going into night time, liek make the sky more orange