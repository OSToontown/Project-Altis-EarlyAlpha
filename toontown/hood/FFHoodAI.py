from toontown.hood import HoodAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals

class DLHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.FunnyFarm,
                               ToontownGlobals.FunnyFarm)

        self.trolley = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()