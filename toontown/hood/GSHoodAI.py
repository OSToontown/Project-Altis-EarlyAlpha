from toontown.toonbase import ToontownGlobals
from toontown.hood import HoodAI
from toontown.building.DistributedBuildingMgrAI import DistributedBuildingMgrAI
from toontown.environment import DistributedDayTimeManagerAI
from toontown.environment import DistributedRainManagerAI

class GSHoodAI(HoodAI.HoodAI):
    notify = directNotify.newCategory('HoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.GoofySpeedway

    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air)
        self.notify.info("Creating zone... Goofy Speedway")

        self.createZone()
        self.spawnObjects()
        self.createTime()
        self.createRain()

    def createZone(self):
        HoodAI.HoodAI.createZone(self)
        self.air.dnaStoreMap[self.HOOD] = self.air.loadDNA(self.air.genDNAFileName(self.HOOD)).generateData()
        self.buildingMgr = DistributedBuildingMgrAI(self.air, self.HOOD, self.air.dnaStoreMap[self.HOOD], self.air.trophyMgr)

    def spawnObjects(self):
        HoodAI.HoodAI.spawnObjects(self)
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
