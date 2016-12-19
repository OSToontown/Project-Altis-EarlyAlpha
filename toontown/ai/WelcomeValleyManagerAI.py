from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals

class WelcomeValleyManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('WelcomeValleyManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.welcomeValleyZoneId = 0

    def generate(self):
        DistributedObjectAI.generate(self)

        # todo: allocate welcome valley zone using unique id allocator, and assign welcomeValleyZoneId

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def toonSetZone(self, avId, zoneId):
        self.clientSetZone(zoneId, avId)

    def clientSetZone(self, zoneId, avId=None):
        if not avId:
            avId = self.air.getAvatarIdFromSender()

        if avId not in self.air.doId2do.keys():
            # sender was not found in the AI's doId2do, don't set the toons zone.
            return

        self.air.doId2do[avId].sendSetZone(zoneId)

    def requestZoneIdMessage(self, origZoneId, context):
        if origZoneId != ToontownGlobals.WelcomeValleyToken:
            # bad zoneId request, set context to null so the client will not change zones.
            self.d_requestZoneIdResponse(0, 0)
            return

        # zone id request was successful, now redirect the toon to the welcome valley allocated zoneId.
        self.d_requestZoneIdResponse(self.welcomeValleyZoneId, context)

        # the avatar is now changing zones, but we have to notify the server that the avatar is in a different zone.
        self.clientSetZone(self.welcomeValleyZoneId)

    def d_requestZoneIdResponse(self, zoneId, context):
        self.sendUpdate('requestZoneIdResponse', [zoneId, context])

    def disable(self):
        DistributedObjectAI.disable(self)

    def delete(self):
        DistributedObjectAI.delete(self)
        self.welcomeValleyZoneId = 0
