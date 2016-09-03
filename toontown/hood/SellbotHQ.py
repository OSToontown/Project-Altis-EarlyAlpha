from toontown.coghq.SellbotCogHQLoader import SellbotCogHQLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.CogHood import CogHood


class SellbotHQ(CogHood):
    notify = directNotify.newCategory('SellbotHQ')

    ID = ToontownGlobals.SellbotHQ
    LOADER_CLASS = SellbotCogHQLoader

    def load(self):
        CogHood.load(self)
        self.skyFile = 'phase_3.5/models/props/Sellbot_sky'
        self.sky.setScale(2.0)
        self.sky.setZ(9.75)
        self.sky.setHpr(-500.0, -700.0, -400.0)

    def enter(self, requestStatus):
        CogHood.enter(self, requestStatus)

        base.localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.CogHQCameraNear, ToontownGlobals.CogHQCameraFar)
