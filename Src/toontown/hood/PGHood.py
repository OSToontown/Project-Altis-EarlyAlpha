from toontown.safezone.PGSafeZoneLoader import PGSafeZoneLoader
from toontown.town.TTTownLoader import TTTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class PGHood(ToonHood):
    notify = directNotify.newCategory('PGHood')

    ID = ToontownGlobals.FunnyFarm
    TOWNLOADER_CLASS = TTTownLoader
    SAFEZONELOADER_CLASS = PGSafeZoneLoader
    STORAGE_DNA = 'phase_4/dna/storage_TT.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0) 