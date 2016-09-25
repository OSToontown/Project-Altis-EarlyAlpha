from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.toon import NPCToons
from SZHoodAI import SZHoodAI

class DDHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.DonaldsDock

    def createZone(self):
        self.notify.info("Creating zone... Donald's Dock")

        SZHoodAI.createZone(self)
        self.spawnObjects()

        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)
