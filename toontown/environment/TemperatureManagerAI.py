from toontown.toonbase import ToontownGlobals
from toontown.environment import TemperatureGlobals

class TemperatureManagerAI:

    def __init__(self, air):
        self.air = air
        self._temperatures = {}
    
    def update(self, zoneId):
        pass
    
    def loadHood(self, zoneId):
        if zoneId not in ToontownGlobals.Hoods:
            return
        
        self._temperatures[zoneId] = 0.0
    
    def unloadHood(self, zoneId):
        if zoneId not in self._temperatures:
            return
        
        del self._temperatures[zoneId]
    
    def delete(self):
        self._temperatures = None
