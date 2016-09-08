from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.fishing.DistributedFishingPondAI import DistributedFishingPondAI
from toontown.fishing.DistributedFishingTargetAI import DistributedFishingTargetAI
from toontown.fishing.DistributedPondBingoManagerAI import DistributedPondBingoManagerAI
from toontown.fishing import FishingTargetGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone import TreasureGlobals
from toontown.safezone.DistributedGameTableAI import DistributedGameTableAI
from toontown.parties.DistributedPartyJukebox40ActivityAI import DistributedPartyJukebox40ActivityAI

from EFlyingTreasurePlannerAI import EFlyingTreasurePlannerAI
from DistributedCannonAI import DistributedCannonAI
from DistributedTargetAI import DistributedTargetAI
from RentalItemGlobals import RentalTablesPosHpr
import CannonGlobals
import random

from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.safezone import TreasureGlobals
from toontown.toonbase import ToontownGlobals
from toontown.estate import HouseGlobals
import time

class DistributedEstateAI(DistributedObjectAI):
    notify = directNotify.newCategory("DistributedEstateAI")
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toons = [0, 0, 0, 0, 0, 0]
        self.rentalType = 0
        self.cloudType = 0
        self.dawnTime = 0
        self.lastEpochTimestamp = 0
        self.rentalTimestamp = 0
        self.flyingTreasurePlanner = None
        self.flyingTreasureIds = []
        self.houses = [None, None, None, None, None, None]

        self.pond = None
        self.spots = []

        self.targets = []

        self.owner = None

        self.rentalObjects = []
        self.cannonTarget = None
        self.jukebox = None

    @property
    def hostId(self):
        return 1000000001

    def generate(self):
        DistributedObjectAI.generate(self)

        self.pond = DistributedFishingPondAI(simbase.air)
        self.pond.setArea(ToontownGlobals.MyEstate)
        self.pond.generateWithRequired(self.zoneId)
        self.pond.start()

        self.pond.bingoMgr = DistributedPondBingoManagerAI(simbase.air)
        self.pond.bingoMgr.setPondDoId(self.pond.getDoId())
        self.pond.bingoMgr.generateWithRequired(self.zoneId)
        self.pond.bingoMgr.initTasks()

        for i in xrange(FishingTargetGlobals.getNumTargets(ToontownGlobals.MyEstate)):
            target = DistributedFishingTargetAI(self.air)
            target.setPondDoId(self.pond.getDoId())
            target.generateWithRequired(self.zoneId)
            self.targets.append(target)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(49.1029, -124.805, 0.344704, 90, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.5222, -134.739, 0.390713, 75, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(41.31, -144.559, 0.375978, 45, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        spot = DistributedFishingSpotAI(self.air)
        spot.setPondDoId(self.pond.getDoId())
        spot.setPosHpr(46.8254, -113.682, 0.46015, 135, 0, 0)
        spot.generateWithRequired(self.zoneId)
        self.spots.append(spot)

        self.createTreasurePlanner()

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        if self.getRentalTimeStamp() == 0:
            return
        elif self.getRentalTimeStamp() < int(time.time()):
            # Our rental items have expired. Don't load them.
            self.b_setRentalTimeStamp(0)
            self.b_setRentalType(0)
            return
        else:
            self.generateRentalItems(self.getRentalType())

    def generateRentalItems(self, rentalType):
        if self.rentalObjects:
            self.deleteRentalItems()

        if rentalType == ToontownGlobals.RentalCannon:
            self.cannonTarget = DistributedTargetAI(self.air)
            self.cannonTarget.generateWithRequired(self.zoneId)

            for drop in CannonGlobals.cannonDrops:
                cannon = DistributedCannonAI(self.air)
                cannon.setEstateId(self.doId)
                cannon.setTargetId(self.cannonTarget.doId)
                cannon.setPosHpr(*drop)
                cannon.generateWithRequired(self.zoneId)
                self.rentalObjects.append(cannon)
                self.generateFlyingTreasures()
                self.b_setClouds(1)

        elif rentalType == ToontownGlobals.RentalGameTable:
              for game in CannonGlobals.cannonDrops:
                  gameTable = DistributedGameTableAI(self.air, self.zoneId, 'rental-table', *game)
                  gameTable.generateWithRequired(self.zoneId)
                  self.rentalObjects.append(gameTable)

        elif rentalType == ToontownGlobals.RentalJukebox:
              self.jukebox = DistributedPartyJukebox40ActivityAI(self.air, self.doId, (0, 0, 0, 0))
              self.jukebox.generateWithRequired(self.zoneId)
              self.jukebox.sendUpdate('setX', [41.148])
              self.jukebox.sendUpdate('setY', [-155.598])
              self.jukebox.sendUpdate('setH', [148.7051])
              self.jukebox.sendUpdate('unloadSign')
              self.rentalObjects.append(self.jukebox)

    def generateFlyingTreasures(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = \
            TreasureGlobals.SafeZoneTreasureSpawns[ToontownGlobals.MyEstate]

        for sp in spawnPoints:
            spawnPoints[spawnPoints.index(sp)] = (sp[0] + random.randint(-30, 30),
                                                  sp[1] + random.randint(0, 25),
                                                  sp[2] + random.randint(10, 30))

        maxTreasures = 10

        self.flyingTreasurePlanner = EFlyingTreasurePlannerAI(self.zoneId, treasureType, healAmount, spawnPoints,
                                                              spawnRate, maxTreasures)
        self.flyingTreasurePlanner.start()

        def setFlyingTreasures(task):
            for t in self.flyingTreasurePlanner.treasures:
                if t:
                    self.flyingTreasureIds.append(t.doId)
            self.setTreasureIds(self.flyingTreasureIds)
            return task.done

        taskMgr.doMethodLater(1.1, setFlyingTreasures, 'flying-treasures')

    def deleteRentalItems(self):
        if self.rentalObjects:
            for object in self.rentalObjects:
                object.requestDelete()
        if self.cannonTarget:
            self.cannonTarget.requestDelete()

        self.rentalObjects = []
        self.cannonTarget = None

    def destroy(self):
        for house in self.houses:
            if house:
                house.requestDelete()
        if self.pond:
            self.pond.requestDelete()
            for spot in self.spots:
                spot.requestDelete()
            for target in self.targets:
                target.requestDelete()
        if self.flyingTreasurePlanner:
            self.flyingTreasurePlanner.stop()
        if self.treasurePlanner:
            self.treasurePlanner.stop()

        self.deleteRentalItems()

        self.requestDelete()

    def setEstateReady(self):
        pass

    def setClientReady(self):
        self.sendUpdate('setEstateReady', [])

    def setEstateType(self, type):
        self.estateType = type

    def d_setEstateType(self, type):
        self.sendUpdate('setEstateType', [type])

    def b_setEstateType(self, type):
        self.setEstateType(type)
        self.d_setEstateType(type)

    def getEstateType(self):
        return self.estateType

    def setClosestHouse(self, todo0):
        pass

    def setTreasureIds(self, flyingTreasureIds):
        self.sendUpdate('setTreasureIds', [flyingTreasureIds])

    def createTreasurePlanner(self):
        treasureType, healAmount, spawnPoints, spawnRate, maxTreasures = TreasureGlobals.SafeZoneTreasureSpawns[ToontownGlobals.MyEstate]
        self.treasurePlanner = SZTreasurePlannerAI(self.zoneId, treasureType, healAmount, spawnPoints, spawnRate, maxTreasures)
        self.treasurePlanner.start()

    def requestServerTime(self):
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(avId, 'setServerTime', [time.time() % HouseGlobals.DAY_NIGHT_PERIOD])

    def setServerTime(self, todo0):
        pass

    def setDawnTime(self, dawnTime):
        self.dawnTime = dawnTime

    def d_setDawnTime(self, dawnTime):
        self.sendUpdate('setDawnTime', [dawnTime])

    def b_setDawnTime(self, dawnTime):
        self.setDawnTime(dawnTime)
        self.d_setDawnTime(dawnTime)

    def getDawnTime(self):
        return self.dawnTime

    def placeOnGround(self, todo0):
        pass

    def setLastEpochTimeStamp(self, last):
        self.lastEpochTimestamp = last

    def d_setLastEpochTimeStamp(self, last):
        self.sendUpdate('setLastEpochTimeStamp', [last])

    def b_setLastEpochTimeStamp(self, last):
        self.setLastEpochTimeStamp(last)
        self.d_setLastEpochTimeStamp(last)

    def getLastEpochTimeStamp(self):
        return self.lastEpochTimestamp

    def setRentalTimeStamp(self, rental):
        self.rentalTimestamp = rental

    def d_setRentalTimeStamp(self, rental):
        self.sendUpdate('setRentalTimeStamp', [rental])

    def b_setRentalTimeStamp(self, rental):
        self.setRentalTimeStamp(rental)
        self.d_setRentalTimeStamp(rental)

    def getRentalTimeStamp(self):
        return self.rentalTimestamp

    def setRentalType(self, typeIndex):
        self.rentalType = typeIndex

    def d_setRentalType(self, typeIndex):
        self.sendUpdate('setRentalType', [typeIndex])

    def b_setRentalType(self, typeIndex):
        self.setRentalType(typeIndex)
        self.d_setRentalType(typeIndex)

    def getRentalType(self):
        return self.rentalType

    def setSlot0ToonId(self, id):
        self.toons[0] = id

    def d_setSlot0ToonId(self, id):
        self.sendUpdate('setSlot0ToonId', [id])

    def b_setSlot0ToonId(self, id):
        self.setSlot0ToonId(id)
        self.d_setSlot0ToonId(id)

    def getSlot0ToonId(self):
        return self.toons[0]

    def setSlot1ToonId(self, id):
        self.toons[1] = id

    def d_setSlot1ToonId(self, id):
        self.sendUpdate('setSlot1ToonId', [id])

    def b_setSlot1ToonId(self, id):
        self.setSlot1ToonId(id)
        self.d_setSlot1ToonId(id)

    def getSlot1ToonId(self):
        return self.toons[1]

    def setSlot2ToonId(self, id):
        self.toons[2] = id

    def d_setSlot2ToonId(self, id):
        self.sendUpdate('setSlot2ToonId', [id])

    def b_setSlot2ToonId(self, id):
        self.setSlot2ToonId(id)
        self.d_setSlot2ToonId(id)

    def getSlot2ToonId(self):
        return self.toons[2]

    def setSlot3ToonId(self, id):
        self.toons[3] = id

    def d_setSlot3ToonId(self, id):
        self.sendUpdate('setSlot3ToonId', [id])

    def b_setSlot3ToonId(self, id):
        self.setSlot3ToonId(id)
        self.d_setSlot3ToonId(id)

    def getSlot3ToonId(self):
        return self.toons[3]

    def setSlot4ToonId(self, id):
        self.toons[4] = id

    def d_setSlot4ToonId(self, id):
        self.sendUpdate('setSlot4ToonId', [id])

    def b_setSlot5ToonId(self, id):
        self.setSlot4ToonId(id)
        self.d_setSlot4ToonId(id)

    def setSlot5ToonId(self, id):
        self.toons[5] = id

    def d_setSlot5ToonId(self, id):
        self.sendUpdate('setSlot5ToonId', [id])

    def b_setSlot5ToonId(self, id):
        self.setSlot5ToonId(id)
        self.d_setSlot5ToonId(id)

    def getSlot5ToonId(self):
        return self.toons[5]


    def setIdList(self, idList):
        for i in xrange(len(idList)):
            if i >= 6:
                return
            self.toons[i] = idList[i]

    def d_setIdList(self, idList):
        self.sendUpdate('setIdList', [idList])

    def b_setIdList(self, idList):
        self.setIdList(idList)
        self.d_setIdLst(idList)

    def setClouds(self, clouds):
        self.cloudType = clouds

    def d_setClouds(self, clouds):
        self.sendUpdate('setClouds', [clouds])

    def b_setClouds(self, clouds):
        self.setClouds(clouds)
        self.d_setClouds(clouds)

    def getClouds(self):
        return self.cloudType

    def cannonsOver(self):
        pass

    def gameTableOver(self):
        pass

    def updateToons(self):
        self.d_setSlot0ToonId(self.toons[0])
        self.d_setSlot1ToonId(self.toons[1])
        self.d_setSlot2ToonId(self.toons[2])
        self.d_setSlot3ToonId(self.toons[3])
        self.d_setSlot4ToonId(self.toons[4])
        self.d_setSlot5ToonId(self.toons[5])

    def rentItem(self, typeIndex, duration):
        self.b_setRentalType(typeIndex)
        self.b_setRentalTimeStamp(duration)
        self.generateRentalItems(typeIndex)
