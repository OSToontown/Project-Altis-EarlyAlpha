from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
import random
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import ToonInteriorColors
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase

class DistributedGagshopInterior(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore = cr.playGame.dnaStore

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def chooseDoor(self):
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        return door

    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)
        self.interior = loader.loadModel('phase_4/models/modules/gagShop_interior')
        self.interior.reparentTo(render)

        self.wallb = self.interior.find('**/random_tc1_TI_wallpaper_border')
        self.wall = self.interior.find('**/random_tc1_TI_wallpaper')
        self.floor = self.interior.find('**/floor')

        self.sign = self.interior.find('**/sign').removeNode()
        self.external = self.interior.find('**/external').removeNode()

        self.walltex = loader.loadTexture('phase_5.5/maps/VdayWall1.jpg')
        self.floortex = loader.loadTexture('phase_5.5/maps/flooring_carpetA_neutral.jpg')
        self.wall.setTexture(self.walltex, 1)
        self.wallb.setTexture(self.walltex, 1)
        self.floor.setTexture(self.floortex, 1)

        self.painting = loader.loadModel('phase_5.5/models/estate/tt_m_prp_int_painting_valentine.bam')
        self.painting.reparentTo(render)
        self.painting.setPos(0, 28, 6)
        self.painting.setScale(3)

        self.counter1 = loader.loadModel('phase_3.5/models/modules/counterShort.bam')
        self.counter1.reparentTo(render)
        self.counter1.setPos(-1, 20, 0)

        self.counter2 = loader.loadModel('phase_3.5/models/modules/counterShort.bam')
        self.counter2.reparentTo(render)
        self.counter2.setPos(12, 20, 0)

        self.vase = loader.loadModel('phase_5.5/models/estate/tt_m_prp_int_roseWatercan_valentine.bam')
        self.vase.reparentTo(self.counter1)
        self.vase.setPosHprScale(-10, 0, 2, 180, 0, 0, 2, 2, 2)

        self.vase1 = loader.loadModel('phase_5.5/models/estate/tt_m_prp_int_roseWatercan_valentine.bam')
        self.vase1.reparentTo(self.counter1)
        self.vase1.setPosHprScale(11, 0, 2, 0, 0, 0, 2, 2, 2)

        self.vase2 = loader.loadModel('phase_5.5/models/estate/tt_m_prp_int_roseVase_valentine.bam')
        self.vase2.reparentTo(render)
        self.vase2.setPosHprScale(0, 10, 15, 0, 0, 180, 2, 2, 2)

        self.rug = loader.loadModel('phase_3.5/models/modules/rug.bam')
        self.rug.reparentTo(render)
        self.rug.setPos(0, 10, 0)

        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        door = self.chooseDoor()
        doorOrigin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(doorOrigin)
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
        doorColor = self.randomGenerator.choice(self.colors['TI_door'])
        DNADoor.setupDoor(doorNP, self.interior, doorOrigin, self.dnaStore, str(self.block), doorColor)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)
        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()
        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()

    def disable(self):
        self.interior.removeNode()
        del self.interior

        self.painting.removeNode()
        del self.painting

        self.counter1.removeNode()
        del self.counter1

        self.counter2.removeNode()
        del self.counter2

        self.vase.removeNode()
        del self.vase

        self.vase1.removeNode()
        del self.vase1

        self.vase2.removeNode()
        del self.vase2

        self.rug.removeNode()
        del self.rug
        DistributedObject.DistributedObject.disable(self)
