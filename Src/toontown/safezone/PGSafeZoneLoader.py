from toontown.safezone import SafeZoneLoader
from toontown.safezone import PGPlayground
from direct.interval.IntervalGlobal import *
import math
import random

class PGSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = PGPlayground.PGPlayground
        self.musicFile = 'phase_13/audio/bgm/party_generic_theme_jazzy.ogg'
        self.activityMusicFile = 'phase_13/audio/bgm/party_generic_theme_jazzy.ogg'
        self.dnaFile = 'phase_13/dna/party_sz.pdna'
        self.safeZoneStorageDNAFile = 'phase_13/dna/storage_party_sz.pdna'
        self.clouds = []
        self.cloudTrack = None
        self.cloudSwitch = 0

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.loadSunMoon()

    def unload(self):
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def loadSunMoon(self):
        self.sun = loader.loadModel('phase_4/models/props/sun.bam')
        self.moon = loader.loadModel('phase_5.5/models/props/moon.bam')
        self.sunMoonNode = self.geom.attachNewNode('sunMoon')
        self.sunMoonNode.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.sun:
            self.sun.reparentTo(self.sunMoonNode)
            self.sun.setY(270)
            self.sun.setScale(2)
            self.sun.setBillboardPointEye()
        if self.moon:
            self.moon.reparentTo(self.sunMoonNode)
            self.moon.setY(-270)
            self.moon.setScale(15)
            self.moon.setBillboardPointEye()
            self.sunMoonNode.setP(30)

    def loadClouds(self):
        self.loadCloudPlatforms()
        self.startCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)

    def startCloudPlatforms(self):
        return
        if len(self.clouds):
            self.cloudTrack = self.__cloudTrack()
            self.cloudTrack.loop()

    def stopCloudPlatforms(self):
        if self.cloudTrack:
            self.cloudTrack.pause()
            del self.cloudTrack
            self.cloudTrack = None
        return

    def loadClouds(self):
        self.loadCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)

    def loadCloud(self, version, radius, zOffset):
        self.notify.debug('loadOnePlatform version=%d' % version)
        cloud = NodePath('cloud-%d%d' % (radius, version))
        cloudModel = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        cc = cloudModel.copyTo(cloud)
        colCube = cc.find('**/collision')
        colCube.setName('cloudSphere-0')
        dTheta = 2.0 * math.pi / self.numClouds
        cloud.reparentTo(self.cloudOrigin)
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]
        cloud.setPos(radius * math.cos(version * dTheta), radius * math.sin(version * dTheta), 4 * random.random() + zOffset)
        cloud.setScale(4.0)
        cloud.setTag('number', '%d%d' % (radius, version))
        x, y, z = cloud.getPos()
        cloudIval = Parallel(cloud.hprInterval(4.0, (360, 0, 0)))
        if version % 2 == 0:
            cloudIval.append(Sequence(cloud.posInterval(2.0, (x, y, z + 4), startPos=(x, y, z), blendType='easeInOut'), cloud.posInterval(2.0, (x, y, z), startPos=(x, y, z + 4), blendType='easeInOut')))
        else:
            cloudIval.append(Sequence(cloud.posInterval(2.0, (x, y, z), startPos=(x, y, z + 4), blendType='easeInOut'), cloud.posInterval(2.0, (x, y, z + 4), startPos=(x, y, z), blendType='easeInOut')))
        cloudIval.loop()
        self.clouds.append([cloud, random.choice(axes)])

    def loadSkyCollision(self):
        plane = CollisionPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 350)))
        plane.setTangible(0)
        planeNode = CollisionNode('sky_collision')
        planeNode.addSolid(plane)
        self.cloudOrigin.attachNewNode(planeNode)

    def loadCloudPlatforms(self):
        self.cloudOrigin = self.geom.attachNewNode('cloudOrigin')
        self.cloudOrigin.setZ(30)
        self.loadSkyCollision()
        self.numClouds = 18
        for i in range(self.numClouds):
            self.loadCloud(i, 110, 0)

        for i in range(self.numClouds):
            self.loadCloud(i, 130, 30)

        for i in range(self.numClouds):
            self.loadCloud(i, 110, 60)

        self.cloudOrigin.stash()

    def __cleanupCloudFadeInterval(self):
        if hasattr(self, 'cloudFadeInterval'):
            self.cloudFadeInterval.pause()
            self.cloudFadeInterval = None
        return

    def fadeClouds(self, on):
        self.__cleanupCloudFadeInterval()
        self.cloudOrigin.setTransparency(1)
        self.cloudFadeInterval = self.cloudOrigin.colorInterval(0.5, Vec4(1, 1, 1, int(on)), blendType='easeIn')
        if on:
            self.cloudOrigin.setColor(Vec4(1, 1, 1, 0))
            self.setCloudSwitch(1)
        else:
            self.cloudFadeInterval = Sequence(self.cloudFadeInterval, Func(self.setCloudSwitch, 0), Func(self.cloudOrigin.setTransparency, 0))
        self.cloudFadeInterval.start()

    def setCloudSwitch(self, on):
        self.cloudSwitch = on
        if hasattr(self, 'cloudOrigin'):
            if on:
                self.cloudOrigin.unstash()
            else:
                self.cloudOrigin.stash()

