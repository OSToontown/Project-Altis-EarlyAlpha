from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedMinnieAI
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

        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-minnie', True):
                self.createClassicChar()

        self.piano = DistributedMMPianoAI.DistributedMMPianoAI(self.air)
        self.piano.generateWithRequired(self.safezone)   

        self.spawnObjects()

    def createClassicChar(self):
        self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
