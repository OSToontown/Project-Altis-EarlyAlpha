from panda3d.core import *
from panda3d.direct import *
import ToonHood
from toontown.town import MMTownLoader
from toontown.safezone import MMSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
from otp.ai.MagicWordGlobal import *

class MMHood(ToonHood.ToonHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = MinniesMelodyland
        self.townLoaderClass = MMTownLoader.MMTownLoader
        self.safeZoneLoaderClass = MMSafeZoneLoader.MMSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_MM.pdna'
        self.holidayStorageDNADict = {WINTER_DECORATIONS: ['phase_6/dna/winter_storage_MM.pdna'],
         WACKY_WINTER_DECORATIONS: ['phase_6/dna/winter_storage_MM.pdna'],
         HALLOWEEN_PROPS: ['phase_6/dna/halloween_props_storage_MM.pdna'],
         SPOOKY_PROPS: ['phase_6/dna/halloween_props_storage_MM.pdna']}
        self.skyFile = 'phase_6/models/props/MM_sky'
        self.spookySkyFile = 'phase_6/models/props/MM_sky'
        self.titleColor = (1.0, 0.5, 0.5, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('MMHood').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('MMHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)

@magicWord(category=CATEGORY_OVERRIDE)
def spooky():
    """
    Activates the 'spooky' effect on the current area.
    """
    hood = base.cr.playGame.hood
    if not hasattr(hood, 'startSpookySky'):
        return "Couldn't find spooky sky."
    if hasattr(hood, 'magicWordSpookyEffect'):
        return 'The spooky effect is already active!'
    hood.magicWordSpookyEffect = True
    hood.startSpookySky()
    fadeOut = base.cr.playGame.getPlace().loader.geom.colorScaleInterval(
        1.5, Vec4(0.55, 0.55, 0.65, 1), startColorScale=Vec4(1, 1, 1, 1),
        blendType='easeInOut')
    fadeOut.start()
    spookySfx = base.loadSfx('phase_4/audio/sfx/spooky.ogg')
    spookySfx.play()
    return 'Activating the spooky effect...'
