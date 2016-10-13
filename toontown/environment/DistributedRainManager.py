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
from toontown.battle import BattleParticles

class DistributedRainManager(DistributedWeatherMGR):
    notify = directNotify.newCategory('DistributedRainManager')
    
    def __init__(self, cr):
        DistributedWeatherMGR.__init__(self, cr)
        self.cr = cr
        self.currentWeather = None
        self.rain = None
        self.rainRender = None
        self.rainSound = None
        
    def announceGenerate(self):
        DistributedWeatherMGR.announceGenerate(self)
        
    def delete(self):
        DistributedWeatherMGR.delete(self)
        if self.currentWeather == 0:
            self.rain.cleanup()
            self.rainSound.stop()
            del self.rain
            del self.rainRender
            del self.rainSound
        
        
    def enterRain(self, timestamp):
        self.rain = BattleParticles.loadParticleFile('raindisk.ptf')
        self.rain.setPos(0, 0, 20)
        self.rainRender = render.attachNewNode('rainRender')
        self.rainRender.setDepthWrite(0)
        self.rainRender.setBin('fixed', 1)
        self.rain.start(camera, self.rainRender)
        self.rainSound = base.loadSfx('phase_12/audio/sfx/CHQ_rain_ambient.ogg')
        base.playSfx(self.rainSound, looping=1, volume=0.25)
        self.currentWeather = 0
        
    def exitRain(self):
        pass
        
    def enterSunny(self, timestamp):
        if self.rain:
            self.rain.cleanup()
            self.rainSound.stop()
            del self.rain
            del self.rainRender
            del self.rainSound
        self.currentWeather = 1

        
    def exitSunny(self):
        pass
        
