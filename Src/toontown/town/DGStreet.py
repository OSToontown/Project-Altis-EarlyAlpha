from pandac.PandaModules import Vec3

from toontown.town.Street import Street
 
 
class DGStreet(Street):
    def __init__(self, loader, parentFSM, doneEvent):
        Street.__init__(self, loader, parentFSM, doneEvent)

    def enter(self, requestStatus, visibilityFlag=1, arrowsOn=1):
        Street.enter(self, requestStatus, visibilityFlag, arrowsOn)

    def exit(self, visibilityFlag=1):
        Street.exit(self, visibilityFlag)
        