from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
from toontown.environment import DistributedDayTimeManagerAI
from toontown.environment import DistributedRainManagerAI
from toontown.golf import GolfGlobals

class GZHoodAI(HoodAI):
    notify = directNotify.newCategory('HoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.GolfZone

    def __init__(self, air):
        HoodAI.__init__(self, air)
        self.notify.info("Creating zone... Chip 'n Dale's MiniGolf")

        self.golfKarts = []

        self.createZone()

    def createZone(self):
        self.spawnObjects()

    def spawnObjects(self):
        HoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
		
    def createTime(self):
        self.dayTimeMgr = DistributedDayTimeManagerAI.DistributedDayTimeManagerAI(self.air)
        self.dayTimeMgr.generateWithRequired(self.HOOD)  
        self.dayTimeMgr.start()
        self.notify.info('Day Time Manager turned on for zone ' + str(self.HOOD))
            
    def createRain(self):
        self.rainMgr = DistributedRainManagerAI.DistributedRainManagerAI(self.air)
        self.rainMgr.generateWithRequired(self.HOOD)  
        self.rainMgr.start(False)
        self.notify.info('Rain Manager turned on for zone ' + str(self.HOOD))
