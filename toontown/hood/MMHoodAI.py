from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.safezone import DistributedMMPianoAI
from toontown.ai import DistributedTrickOrTreatTargetAI
from toontown.ai import DistributedWinterCarolingTargetAI
from toontown.ai import HolidayGlobals


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


        if HolidayGlobals.WhatHolidayIsIt() == 'Winter':
            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(4614)


            self.WinterCarolingTargetManager = DistributedWinterCarolingTargetAI.DistributedWinterCarolingTargetAI(self.air)
            self.WinterCarolingTargetManager.generateWithRequired(4614)

        if HolidayGlobals.WhatHolidayIsIt() == 'Halloween':
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(4835)


            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(4835)
