from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase import Loader
from toontown.toontowngui import ToontownLoadingScreen
from toontown.dna import DNAParser
from direct.stdpy.file import open
from direct.stdpy import threading

class ToontownLoader(Loader.Loader):
    TickPeriod = 0.06

    def __init__(self, base):
        Loader.Loader.__init__(self, base)
        self.inBulkBlock = None
        self.blockName = None
        self.loadingScreen = ToontownLoadingScreen.ToontownLoadingScreen()
        return

    def destroy(self):
        self.loadingScreen.destroy()
        del self.loadingScreen
        Loader.Loader.destroy(self)

    def loadDNA(self, filename):
        filename = '/' + filename

        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading DNA:\n" + filename
        print("Loading DNA: " + filename)
            
        with open(filename, 'r') as f:
            tree = DNAParser.parse(f)
            
        self.tick()

        return tree

    def beginBulkLoad(self, name, label, range, gui, tipCategory, zoneId):
        self._loadStartT = globalClock.getRealTime()
        Loader.Loader.notify.info("starting bulk load of block '%s'" % name)
        if self.inBulkBlock:
            Loader.Loader.notify.warning("Tried to start a block ('%s'), but am already in a block ('%s')" % (name, self.blockName))
            return None
        self.inBulkBlock = 1
        self._lastTickT = globalClock.getRealTime()
        self.blockName = name
        self.loadingScreen.begin(range, label, gui, tipCategory, zoneId)
        return None

    def endBulkLoad(self, name):
        if not self.inBulkBlock:
            Loader.Loader.notify.warning("Tried to end a block ('%s'), but not in one" % name)
            return None
        if name != self.blockName:
            Loader.Loader.notify.warning("Tried to end a block ('%s'), other then the current one ('%s')" % (name, self.blockName))
            return None
        self.inBulkBlock = None
        expectedCount, loadedCount = self.loadingScreen.end()
        now = globalClock.getRealTime()
        Loader.Loader.notify.info("At end of block '%s', expected %s, loaded %s, duration=%s" % (self.blockName,
         expectedCount,
         loadedCount,
         now - self._loadStartT))
        return

    def abortBulkLoad(self):
        if self.inBulkBlock:
            Loader.Loader.notify.info("Aborting block ('%s')" % self.blockName)
            self.inBulkBlock = None
            self.loadingScreen.abort()
        return

    def tick(self):
        if self.inBulkBlock:
            now = globalClock.getRealTime()
            if now - self._lastTickT > self.TickPeriod:
                self._lastTickT += self.TickPeriod
                self.loadingScreen.tick()
                try:
                    base.cr.considerHeartbeat()
                except:
                    pass

    def loadModel(self, *args, **kw):
        print("Loading model: " + args[0])
        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading model:\n" + args[0]
        ret = Loader.Loader.loadModel(self, *args, **kw)
        
        if ret:
            gsg = base.win.getGsg()
            if gsg:
                ret.prepareScene(gsg)
        self.tick()
        return ret

    def loadFont(self, *args, **kw):
        print("Loading: " + args[0])
        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading font:\n" + args[0]
        ret = Loader.Loader.loadFont(self, *args, **kw)
        self.tick()
        return ret

    def loadTexture(self, texturePath, alphaPath = None, okMissing = False):
        print("Loading texture: " + texturePath)
        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading texture:\n" + texturePath
        ret = Loader.Loader.loadTexture(self, texturePath, alphaPath, okMissing=okMissing)
       # ret.setMinfilter(SamplerState.FT_linear_mipmap_linear)
        self.tick()
        if alphaPath:
            self.tick()
        return ret

    def loadSfx(self, soundPath):
        print("Loading sound: " + soundPath)
        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading SFX:\n" + soundPath
        ret = Loader.Loader.loadSfx(self, soundPath)
        self.tick()
        return ret

    def loadMusic(self, soundPath):
        print("Loading music: " + soundPath)
        if self.loadingScreen.loadingObj:
            self.loadingScreen.loadingObj['text'] = "Loading music:\n " + soundPath
        ret = Loader.Loader.loadMusic(self, soundPath)
        self.tick()
        return ret