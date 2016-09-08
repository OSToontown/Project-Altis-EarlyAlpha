from direct.task.Task import Task
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests
from random import randrange
import random

class DistributedNPCFlippyAI(DistributedNPCToonBaseAI):
    def requestTeleportation(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is None:
            return