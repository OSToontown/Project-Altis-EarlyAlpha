from toontown.safezone import FFPlayground
from toontown.safezone import SafeZoneLoader


class FFSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = FFPlayground.FFPlayground
        self.musicFile = 'phase_14/audio/bgm/FF_nbrhood.ogg'
        self.activityMusicFile = 'phase_14/audio/bgm/FF_SZ.ogg'
        self.dnaFile = 'phase_14/dna/daisys_garden_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_14/dna/storage_FF_sz.pdna'

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_8/audio/sfx/SZ_DG_bird_01.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_02.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_03.ogg',
                                            'phase_8/audio/sfx/SZ_DG_bird_04.ogg'])

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)
        del self.birdSound
