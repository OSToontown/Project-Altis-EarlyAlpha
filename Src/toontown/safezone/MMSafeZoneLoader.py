from pandac.PandaModules import *
from toontown.safezone import MMPlayground
from toontown.safezone import SafeZoneLoader
from toontown.toonbase import ToontownGlobals

class MMSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = MMPlayground.MMPlayground
        self.musicFile = 'phase_6/audio/bgm/MM_nbrhood.ogg'
        self.activityMusicFile = 'phase_6/audio/bgm/MM_SZ_activity.ogg'
        self.dnaFile = 'phase_6/dna/minnies_melody_land_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_MM_sz.pdna'
    
    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        cp = CollisionBox(Point3(7, 0, 0), 17.65, 0.5, 23.95)
        self.wallfix = base.render.attachNewNode(CollisionNode('wallhole_collision'))
        self.wallfix.node().addSolid(cp)
        self.wallfix.setPos(-99.70, -35, 6.0)
        self.geom.find('**/prop_blockade_DNARoot').removeNode()
        
    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

        self.wallfix.removeNode()
        del self.wallfix
