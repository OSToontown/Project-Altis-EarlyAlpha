from pandac.PandaModules import LVector3f
from toontown.pets import PetConstants

class Mover:
    notify = directNotify.newCategory('Mover')

    def __init__(self, nodePath, fwdSpeed=PetConstants.FwdSpeed, rotSpeed=PetConstants.RotSpeed):
        self.nodePath = nodePath
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed

        self.shove = LVector3f(0, 0, 0)
        self.rotShove = LVector3f(0, 0, 0)
        self.rotForce = LVector3f(0, 0, 0)
        self.force = LVector3f(0, 0, 0)

        self.impulses = {}

    def getNodePath(self):
        return self.nodePath

    def setFwdSpeed(self, fwdSpeed):
        self.fwdSpeed = fwdSpeed

    def getFwdSpeed(self):
        return self.fwdSpeed

    def setRotSpeed(self, rotSpeed):
        self.rotSpeed = rotSpeed

    def getRotSpeed(self):
        return self.rotSpeed

    def addShove(self, shove):
        self.shove += shove

    def addRotShove(self, rotShove):
        self.rotShove += rotShove

    def addRotForce(self, rotForce):
        self.rotForce += rotForce

    def addForce(self, force):
        self.force += force

    def destroy(self):
        for name in self.impulses.keys():
            self.removeImpulse(name)

    def addImpulse(self, name, impulse):
        self.impulses[name] = impulse
        impulse.setMover(self)

    def removeImpulse(self, name):
        self.impulses[name].destroy()
        del self.impulses[name]

    def getCollisionEventName(self):
        return 'moverCollision-' + str(id(self))

    def move(self):
        dt = globalClock.getDt()

        for value in self.impulses.values():
            value.process(dt)

        self.integrate(dt)

    def integrate(self, dt):
        v4 = self.force * dt
        v5 = self.rotForce * dt
        v7 = self.shove * dt
        v13 = self.rotShove * dt

        v8 = self.force * (dt**2)
        v9 = v8 / 2.0
        v10 = v4 * dt
        v11 = v10 + v9

        pos = v11 + v7
        self.nodePath.setFluidPos(self.nodePath, pos)

        v14 = self.rotForce * (dt**2)
        v15 = v14 / 2.0
        v16 = v5 * dt
        v17 = v16 + v15

        hpr = v17 + v13
        self.nodePath.setHpr(self.nodePath, hpr)

        self.force = LVector3f(0, 0, 0)
        self.rotForce = LVector3f(0, 0, 0)
        self.shove = LVector3f(0, 0, 0)
        self.rotShove = LVector3f(0, 0, 0)