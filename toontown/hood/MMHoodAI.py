from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.safezone import DistributedMMPianoAI

class MMHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.MinniesMelodyland

    def createZone(self):
        self.notify.info("Creating zone... Minnie's Melodyland")
        self.piano = None
        self.classicChar = None

        SZHoodAI.createZone(self)

        self.piano = DistributedMMPianoAI.DistributedMMPianoAI(self.air)
        self.piano.generateWithRequired(self.safezone)   

        self.spawnObjects()
