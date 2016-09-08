from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD


class CentralLoggerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("CentralLoggerUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

    def sendMessage(self, category, description, sender, receiver):
        pass

    def logAIGarbage(self):
        pass
