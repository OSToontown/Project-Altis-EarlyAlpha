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
        self.hood = base.cr.playGame.hood
        self.interval = 150
        self.hour2sky = {
            0: 'night',
            1: 'night',
            2: 'night',
            3: 'night',
            4: 'night',
            5: 'night',
            6: 'mml',
            7: 'mml',
            8: 'day',
            9: 'day',
            10: 'day',
            11: 'day',
            12: 'day',
            13: 'day',
            14: 'day',
            15: 'day',
            16: 'day',
            17: 'mml',
            18: 'mml',
            19: 'mml',
            20: 'night',
            21: 'night',
            22: 'night',
            23: 'night'
        }
        
    def setSky(self, sky):
        self.hood.skyTransition(str(sky)) 
        
    def announceGenerate(self):
        DistributedWeatherMGR.announceGenerate(self)
        
    def delete(self):
        self.currSeq.finish()
        render.setColorScale(Vec4(1, 1, 1, 1))
        DistributedWeatherMGR.delete(self)
    
    def update(self, currentHour):
        self.currSeq = LerpColorScaleInterval(render, self.interval, DayTimeGlobals.COLORS[
            0 if currentHour == 23 else currentHour + 1], DayTimeGlobals.COLORS[currentHour])
        
        self.currSeq.start()
        
        # update sky
        self.setSky(self.hour2sky[currentHour])

# TODO: Add the next 12 hours, for now im just going to use this in reverse to go to night, but we should add the next 12 to make it look more like its going into night time, liek make the sky more orange
