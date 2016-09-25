from SZHoodAI import SZHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI

class OZHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.OutdoorZone

    def createZone(self):
        self.notify.info("Creating zone... Chip 'n Dale's Acorn Acres")

        SZHoodAI.createZone(self, False)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.spawnObjects()

    def spawnObjects(self):
        SZHoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
