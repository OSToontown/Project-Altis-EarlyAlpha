from direct.showbase import DirectObject

class Impulse(DirectObject.DirectObject):

    def __init__(self):
        self.mover = None
        self.nodePath = None

    def process(self, dt):
        pass

    def destroy(self):
        pass

    def getNodePath(self):
    	return self.nodePath

    def setMover(self, mover):
        self.mover = mover
        self.nodePath = self.mover.getNodePath()

    def clearMover(self):
    	self.mover = None
    	self.nodePath = None