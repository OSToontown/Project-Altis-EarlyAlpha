from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons

class DLHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.DonaldsDreamland

    def createZone(self):
        self.notify.info("Creating zone... Donald's Dreamland")

        SZHoodAI.createZone(self)
        self.spawnObjects()
