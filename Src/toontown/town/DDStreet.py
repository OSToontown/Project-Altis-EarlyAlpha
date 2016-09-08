from pandac.PandaModules import Vec3

from toontown.town import Street


class DDStreet(Street.Street):
    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def enter(self, requestStatus):
        Street.Street.enter(self, requestStatus)
        self.loader.hood.setWhiteFog()

    def exit(self):
        Street.Street.exit(self)
        self.loader.hood.setNoFog()

