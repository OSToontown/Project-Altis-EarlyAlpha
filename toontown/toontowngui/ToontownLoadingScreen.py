from panda3d.core import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
import random
logoScale = (0.5, 1.0, 0.25)  # Scale for our logo.
class ToontownLoadingScreen():
    __module__ = __name__

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.loadingGui = None
        self.range = None
        self.loadingText = None
        self.loadingObj = None
        self.loadingCircle = None
        self.background = None
        self.logo = None
        base.graphicsEngine.renderFrame()
        return

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + '\n' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory, zoneId):
        self.loadingGui = aspect2d.attachNewNode('loadingUI')
        self.loadingGui.reparentTo(aspect2d, NO_FADE_SORT_INDEX)
        base.graphicsEngine.renderFrame()
        self.background = OnscreenImage(image = 'phase_3.5/maps/loading/toon.jpg', parent = aspect2d)
        self.background.setScale(2, 1, 1)
        self.background.setBin('background', 1)
        self.background.show()
        self.background.reparentTo(self.loadingGui)
        base.graphicsEngine.renderFrame()
        self.logo = OnscreenImage(
            image='phase_3/maps/toontown-logo.png',
            scale=logoScale)
        base.graphicsEngine.renderFrame()
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        base.graphicsEngine.renderFrame()
        scale = self.logo.getScale()
        base.graphicsEngine.renderFrame()
        self.logo.setPos(0, 0, 0.65)
        self.loadingObj = OnscreenText(text='', align=TextNode.ACenter, scale=0.04, style = 3, fg = (1, 1, 1, 1))
        self.loadingObj.setPos(0, -.8)
        self.loadingCircle = OnscreenImage(image = 'phase_3/maps/dmenu/loading_circle.png')
        self.loadingCircle.show()
        base.graphicsEngine.renderFrame()
        self.loadingCircle.setScale(0.1)
        self.loadingCircle.setTransparency(TransparencyAttrib.MAlpha)
        self.loadingCircle.reparentTo(base.a2dBottomRight)
        base.graphicsEngine.renderFrame()
        self.loadingCircle.setPos(-0.1, 0, 0.1)
        base.graphicsEngine.renderFrame()
        self.loadingText = OnscreenText(text='Initializing Load...', align=TextNode.ACenter, scale=0.1, pos=(0, 0, 0))
        self.loadingText.reparentTo(aspect2d)
        base.graphicsEngine.renderFrame()
        self.loadingText["text"] = label
        base.graphicsEngine.renderFrame()
        self.loadingText.wrtReparentTo(self.loadingGui)
        self.loadingObj.wrtReparentTo(self.loadingGui)
        self.loadingCircle.wrtReparentTo(self.loadingGui)
        self.logo.wrtReparentTo(self.loadingGui)
        base.graphicsEngine.renderFrame()

    def destroy(self):
        pass
        
    def end(self):
        if self.loadingGui:
            self.loadingGui.removeNode()
            self.loadingGui = None
            
        if self.loadingText:
            self.loadingText.destroy()
            del self.loadingText
            
        if self.loadingCircle:
            self.loadingCircle.destroy()
            del self.loadingCircle
            
        if self.loadingObj:
            self.loadingObj.destroy()
            self.loadingObj = None
            
        if self.background:
            self.background.destroy()
            del self.background
            
        if self.logo:
            self.logo.destroy()
            del self.logo
            
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.loadingGui.reparentTo(hidden)
        self.loadingObj = None
        
    def tick(self):
        self.__count = self.__count + 1
        base.graphicsEngine.renderFrame()
        try:
            if self.loadingCircle:
                self.loadingCircle.setHpr(0, 0, self.__count * 15)
        except:
            pass