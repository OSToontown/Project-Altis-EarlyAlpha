# Embedded file name: toontown.toonfest.DistributedTFTrampolineActivity
from toontown.parties.DistributedPartyTrampolineActivity import DistributedPartyTrampolineActivity
from toontown.toonbase import TTLocalizer

class DistributedTFTrampolineActivity(DistributedPartyTrampolineActivity):

    def __init__(self, cr, doJellyBeans = True, doTricks = False, texture = None, useTokens = True):
        DistributedPartyTrampolineActivity.__init__(self, cr, doJellyBeans, doTricks, 'phase_13/maps/tt_t_ara_pty_trampolineVictory.jpg', useTokens)

    def getTitle(self):
        return TTLocalizer.PartyTrampolineToonfestTitle