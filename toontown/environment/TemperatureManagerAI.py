from toontown.toonbase import ToontownGlobals
from toontown.environment import TemperatureGlobals
import random
import math

class TemperatureManagerAI:

    def __init__(self, air):
        self.air = air
        self._temperatures = {}
    
    def calculateRandom(self, high, low):
        return random.randint(low, high) # todo: kinda cheep way of randomly setting starting tempearture
    
    def update(self, task, zoneId):
        # todo, update temperature based on time of day.
        return task.again
    
    def loadHood(self, zoneId):
        if zoneId not in ToontownGlobals.Hoods:
            return
        
        self._temperatures[zoneId] = self.calculateRandom(*TemperatureGlobals.hood2average[
            zoneId])
    
    def unloadHood(self, zoneId):
        if zoneId not in self._temperatures.keys():
            return
        
        del self._temperatures[zoneId]
    
    def delete(self):
        self._temperatures = None
