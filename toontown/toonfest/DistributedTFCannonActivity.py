# Embedded file name: toontown.toonfest.DistributedTFCannonActivity
from toontown.parties.DistributedPartyCannonActivity import DistributedPartyCannonActivity
from toontown.toonbase import TTLocalizer

class DistributedTFCannonActivity(DistributedPartyCannonActivity):

    def getTitle(self):
        return TTLocalizer.ToonfestCannonActivityTitle