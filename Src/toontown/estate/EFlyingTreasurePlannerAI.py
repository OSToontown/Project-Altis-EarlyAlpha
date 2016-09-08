from toontown.safezone.SZTreasurePlannerAI import SZTreasurePlannerAI
from toontown.safezone.DistributedEFlyingTreasureAI import DistributedEFlyingTreasureAI


class EFlyingTreasurePlannerAI(SZTreasurePlannerAI):
    def preSpawnTreasures(self):
        for i in xrange(self.maxTreasures):
            self.placeTreasure(i)

    def placeTreasure(self, index):
        spawnPoint = self.spawnPoints[index]
        treasure = DistributedEFlyingTreasureAI(simbase.air, self, self.treasureType, spawnPoint[0], spawnPoint[1], spawnPoint[2])
        treasure.generateWithRequired(self.zoneId)
        self.treasures[index] = treasure 