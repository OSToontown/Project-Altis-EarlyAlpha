from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.building import Elevator
from panda3d.core import *
from panda3d.direct import *
from toontown.coghq import CogHQExterior
from toontown.dna.DNAParser import loadDNAFileAI, DNAStorage
from toontown.hood import ZoneUtil

class LawbotHQExterior(CogHQExterior.CogHQExterior):
    notify = DirectNotifyGlobal.directNotify.newCategory('LawbotHQExterior')
    dnaFile = 'phase_11/dna/cog_hq_lawbot_sz.pdna'

    def enter(self, requestStatus):
        CogHQExterior.CogHQExterior.enter(self, requestStatus)
        # Load the CogHQ DNA file:
        dnaStore = DNAStorage()
        dnaFileName = self.genDNAFileName(self.zoneId)
        loadDNAFileAI(dnaStore, dnaFileName)

        # Collect all of the vis group zone IDs:
        self.zoneVisDict = {}
        for i in xrange(dnaStore.getNumDNAVisGroupsAI()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            visGroup = dnaStore.getDNAVisGroupAI(i)
            visZoneId = int(base.cr.hoodMgr.extractGroupName(groupFullName))
            visZoneId = ZoneUtil.getTrueZoneId(visZoneId, self.zoneId)
            visibles = []
            for i in xrange(visGroup.getNumVisibles()):
                visibles.append(int(visGroup.getVisible(i)))
            visibles.append(ZoneUtil.getBranchZone(visZoneId))
            self.zoneVisDict[visZoneId] = visibles

        # Next, we want interest in all vis groups due to this being a Cog HQ:
        base.cr.sendSetZoneMsg(self.zoneId, self.zoneVisDict.values()[0])