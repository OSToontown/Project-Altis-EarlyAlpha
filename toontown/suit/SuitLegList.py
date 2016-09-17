# Embedded file name: toontown.suit.SuitLegList
from toontown.toonbase import ToontownGlobals
import SuitTimings
from toontown.dna import DNAStoreSuitPoint

class SuitLegList:

    def __init__(self, suitGraph, path):
        self.suitGraph = suitGraph
        self.suitLegType = 0
        self.startTime = 0.0
        self.legTime = 0.0
        self.blockNumber = 0
        self.legs = []
        self.points = path
        self.createFirstLeg()
        self.createMidLegs()
        self.createLastLeg()
        self.cacheStartTimes()

    def createFirstLeg(self):
        startPoint = self.points[0]
        secondPoint = self.points[1]
        if startPoint.type == DNAStoreSuitPoint.SIDEDOORPOINT:
            legType = SuitLeg.TFromSuitBuilding
        else:
            legType = SuitLeg.TFromSky
        self.legs.append(SuitLeg(self.suitGraph, startPoint, secondPoint, legType))

    def createMidLegs(self):
        i = 0
        while i < len(self.points) - 1:
            a = self.points[i]
            b = self.points[i + 1]
            self.createLeg(a, b)
            i += 1

    def createLeg(self, a, b):
        if a.type in (DNAStoreSuitPoint.FRONTDOORPOINT, DNAStoreSuitPoint.SIDEDOORPOINT):
            legType = SuitLeg.TWalkToStreet
        elif b.type in (DNAStoreSuitPoint.FRONTDOORPOINT, DNAStoreSuitPoint.SIDEDOORPOINT):
            legType = SuitLeg.TWalkFromStreet
        else:
            legType = SuitLeg.TWalk
        if a.type == DNAStoreSuitPoint.COGHQOUTPOINT:
            self.legs.append(SuitLeg(self.suitGraph, a, b, SuitLeg.TFromCoghq))
            self.legs.append(SuitLeg(self.suitGraph, a, b, legType))
        elif b.type == DNAStoreSuitPoint.COGHQINPOINT:
            self.legs.append(SuitLeg(self.suitGraph, a, b, legType))
            self.legs.append(SuitLeg(self.suitGraph, a, b, SuitLeg.TToCoghq))
        else:
            self.legs.append(SuitLeg(self.suitGraph, a, b, legType))

    def createLastLeg(self):
        endPoint = self.points[-1]
        prevPoint = self.points[-2]
        if endPoint.type == DNAStoreSuitPoint.FRONTDOORPOINT:
            legType = SuitLeg.TToToonBuilding
        elif endPoint.type == DNAStoreSuitPoint.SIDEDOORPOINT:
            legType = SuitLeg.TToSuitBuilding
        else:
            legType = SuitLeg.TToSky
        self.legs.append(SuitLeg(self.suitGraph, prevPoint, endPoint, legType))
        self.legs.append(SuitLeg(self.suitGraph, prevPoint, endPoint, SuitLeg.TOff))

    def cacheStartTimes(self):
        time = 0.0
        self.startTimes = []
        for leg in self.legs:
            self.startTimes.append(time)
            time += leg.getLegTime()

    def getStartTime(self, index):
        return self.startTimes[index]

    def getLegIndexAtTime(self, time, startLeg):
        i = startLeg
        while i + 1 < self.getNumLegs() and self.getStartTime(i + 1) < time:
            i += 1

        return i

    def getNumLegs(self):
        return len(self.legs)

    def getZoneId(self, legNum):
        return self.legs[legNum].getZone()

    def getType(self, legNum):
        return self.legs[legNum].getType()

    def getBlockNumber(self, legNum):
        return self.legs[legNum].getBlockNumber()

    def isPointInRange(self, point, startTime, endTime):
        leg = self.getLegIndexAtTime(startTime, 0)
        time = startTime
        while time < endTime:
            if leg >= len(self.legs):
                return False
            if self[leg].pointA == point or self[leg].pointB == point:
                return True
            time += self[leg].getLegTime()
            leg += 1

        return False

    def __getitem__(self, key):
        return self.legs[key]


class SuitLeg:
    TWalkFromStreet = 0
    TWalkToStreet = 1
    TWalk = 2
    TFromSky = 3
    TToSky = 4
    TFromSuitBuilding = 5
    TToSuitBuilding = 6
    TToToonBuilding = 7
    TFromCoghq = 8
    TToCoghq = 9
    TOff = 10
    TypeToName = {0: 'WalkFromStreet',
     1: 'WalkToStreet',
     2: 'Walk',
     3: 'FromSky',
     4: 'ToSky',
     5: 'FromSuitBuilding',
     6: 'ToSuitBuilding',
     7: 'ToToonBuilding',
     8: 'FromCogHQ',
     9: 'ToCogHQ',
     10: 'Off'}

    def __init__(self, suitGraph, pointA, pointB, type):
        self.suitGraph = suitGraph
        self.pointA = pointA
        self.pointB = pointB
        self.posA = pointA.getPos()
        self.posB = pointB.getPos()
        self.type = type
        self.zoneId = self.suitGraph.getEdgeZone(self.suitGraph.getConnectingEdge(self.pointA, self.pointB))

    def getLegTime(self):
        if self.type in (SuitLeg.TWalk, SuitLeg.TWalkFromStreet, SuitLeg.TWalkToStreet):
            return (self.posA - self.posB).length() / ToontownGlobals.SuitWalkSpeed
        elif self.type == SuitLeg.TFromSky:
            return SuitTimings.fromSky
        elif self.type == SuitLeg.TToSky:
            return SuitTimings.toSky
        elif self.type == SuitLeg.TFromSuitBuilding:
            return SuitTimings.fromSuitBuilding
        elif self.type == SuitLeg.TToSuitBuilding:
            return SuitTimings.toSuitBuilding
        elif self.type == SuitLeg.TToToonBuilding:
            return SuitTimings.toToonBuilding
        else:
            return SuitTimings.toToonBuilding

    def getPosA(self):
        return self.posA

    def getPosB(self):
        return self.posB

    def getPosAtTime(self, time):
        if self.type in (SuitLeg.TFromSky, SuitLeg.TFromSuitBuilding, SuitLeg.TFromCoghq):
            return self.getPosA()
        if self.type in (SuitLeg.TToSky,
         SuitLeg.TToSuitBuilding,
         SuitLeg.TToToonBuilding,
         SuitLeg.TToCoghq,
         SuitLeg.TOff):
            return self.getPosB()
        fraction = time / self.getLegTime()
        fraction = min(max(fraction, 0.0), 1.0)
        delta = self.getPosB() - self.getPosA()
        pos = self.getPosA() + delta * (time / self.getLegTime())
        return pos

    def getZone(self):
        return self.zoneId

    def getBlockNumber(self):
        block = self.pointB.getLandmarkBuildingIndex()
        if block is not None:
            return block
        else:
            return self.pointA.getLandmarkBuildingIndex()
            return

    @staticmethod
    def getTypeName(type):
        return SuitLeg.TypeToName[type]

    def getType(self):
        return self.type