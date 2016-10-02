from ToonHood import ToonHood
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
import CogHood
from toontown.safezone.TFSafeZoneLoader import TFSafeZoneLoader
from toontown.town.TTTownLoader import TTTownLoader # Temporary
import SkyUtil

class TFHood(ToonHood):
    notify = directNotify.newCategory('TFHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.FunnyFarm
        self.townLoaderClass = TTTownLoader # Temporary
        self.safeZoneLoaderClass = TFSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_TF.xml'
        self.skyFile = 'phase_9/models/cogHQ/old_sky'
        self.titleColor = (0.5, 0.5, 0.5, 1.0)

    def load(self):
        ToonHood.load(self)
        self.sky.setScale(2.5)
        self.sky.setZ(-1)
        self.parentFSM.getStateNamed('TFHood').addChild(self.fsm)

    def enter(self, *args):
        ToonHood.enter(self, *args)
        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        ToonHood.exit(self)

    def unload(self):
        self.parentFSM.getStateNamed('TFHood').removeChild(self.fsm)
        ToonHood.unload(self)
