from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedPolarPlaceEffectMgrAI
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI
from toontown.ai import HolidayGlobals
class BRHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.TheBrrrgh

    def createZone(self):
        self.notify.info("Creating zone... The Brrrgh")

        SZHoodAI.createZone(self)

        self.polarPlaceEffectManager = DistributedPolarPlaceEffectMgrAI.DistributedPolarPlaceEffectMgrAI(self.air)
        self.polarPlaceEffectManager.generateWithRequired(3821)

        self.spawnObjects()
        if HolidayGlobals.WhatHolidayIsIt() == 'Winter':
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(3828)
            
        elif HolidayGlobals.WhatHolidayIsIt() == 'Halloween':
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(3707)
