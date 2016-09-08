import CatalogItem
from toontown.pets import PetTricks
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.pets import PetDNA, Pet

class CatalogPetTrickItem(CatalogItem.CatalogItem):
    sequenceNumber = 0
    petPicture = None

    def makeNewItem(self, trickId):
        self.trickId = trickId
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 1

    def reachedPurchaseLimit(self, avatar):
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        if self.trickId in avatar.petTrickPhrases:
            return 1
        return 0

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptPet
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.PetTrickTypeName

    def getName(self):
        phraseId = PetTricks.TrickId2scIds[self.trickId][0]
        return OTPLocalizer.SpeedChatStaticText[phraseId]

    def recordPurchase(self, avatar, optional):
        avatar.petTrickPhrases.append(self.trickId)
        avatar.d_setPetTrickPhrases(avatar.petTrickPhrases)
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        self.model = Pet.Pet(forGui=1)
        dna = avatar.getPetDNA()
        if dna == None:
            dna = PetDNA.getRandomPetDNA()
        self.model.setDNA(dna)
        self.model.setH(180)
        frame, ival = self.makeFrameModel(self.model, 0)
        self.model.setScale(2.0)
        self.model.setP(-40)
        track = PetTricks.getTrickIval(self.model, self.trickId)
        name = 'petTrick-item-%s' % self.sequenceNumber
        CatalogPetTrickItem.sequenceNumber += 1
        if track != None:
            track = Sequence(Sequence(track), ActorInterval(self.model, 'neutral', duration=2), name=name)
        else:
            self.model.animFSM.request('neutral')
            track = Sequence(Wait(4), name=name)
        self.hasPicture = True
        return (frame, track)

    def cleanupPicture(self):
        CatalogItem.CatalogItem.cleanupPicture(self)

        self.model.detachNode()
        self.model = None

    def output(self, store = -1):
        return 'CatalogPetTrickItem(%s%s)' % (self.trickId, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.trickId - other.trickId

    def getHashContents(self):
        return self.trickId

    def getBasePrice(self):
        return 500

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.trickId = di.getUint8()
        self.dna = None
        if self.trickId not in PetTricks.TrickId2scIds:
            raise ValueError

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.trickId)

def getAllPetTricks():
    list = []
    for trickId in PetTricks.TrickId2scIds.keys():
        list.append(CatalogPetTrickItem(trickId))

    return list
