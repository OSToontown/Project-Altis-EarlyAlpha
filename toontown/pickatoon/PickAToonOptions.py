'''
Created on Apr 2, 2016

@author: Drew
'''

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpScaleInterval
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TransparencyAttrib, Point3, Vec4, TextNode, Vec3

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
from toontown.toontowngui import TTDialog
from toontown.options import GraphicsOptions

resolution_table = [
    (800, 600),
    (1024, 768),
    (1280, 1024),
    (1600, 1200),
    (1280, 720),
    (1920, 1080)]

class PickAToonOptions:

    def __init__(self):
        self.optionsOpenSfx = None #base.loadSfx(DMenuResources.Settings_Open) # ALTIS: TODO: Add sound effects
        self.optionsCloseSfx = None #base.loadSfx(DMenuResources.Settings_Close) # ALTIS: TODO: Add sound effects

    def showOptions(self):
        #base.playSfx(self.optionsOpenSfx) # ALTIS: TODO: Add sound effects
        self.displayOptions()
        zoomIn = (LerpScaleInterval(self.optionsNode, .4, Vec3(1, 1, 1), Vec3(0, 0, 0), blendType = 'easeInOut')).start()

    def hideOptions(self):
        #base.playSfx(self.optionsCloseSfx) # ALTIS: TODO: Add sound effects
        zoomOut = (LerpScaleInterval(self.optionsNode, .4, Vec3(0, 0, 0), Vec3(1, 1, 1), blendType = 'easeInOut')).start()
        Sequence (
        Wait(.4),
        Func(self.delOptions)).start()

    def displayOptions(self):
        self.optionsNode = aspect2d.attachNewNode('optionsNode')
        self.optionsNode.reparentTo(aspect2d)


        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        quitHover = gui.find('**/QuitBtn_RLVR')


        self.optionsBox = OnscreenImage(image = 'phase_3/maps/stat_board.png')
        self.optionsBox.setTransparency(TransparencyAttrib.MAlpha)
        self.optionsBox.setPos(0, 0, 0)
        self.optionsBox.setScale(0.7)
        self.optionsBox.reparentTo(self.optionsNode)
        # Music Label
        self.Music_Label = DirectLabel(parent = self.optionsNode, relief = None, text = 'Music Volume', text_align = TextNode.ACenter, text_scale = 0.052, pos = (0, 0, 0.5))
        # Music Slider
        self.Music_toggleSlider = DirectSlider(parent = self.optionsNode, pos = (0, 0, 0.4),
                                               value = settings['musicVol'] * 100, pageSize = 5, range = (0, 100), command = self.__doMusicLevel,)
        self.Music_toggleSlider.setScale(0.4, 0.4, 0.4)
        self.Music_toggleSlider.show()

        # SFX Slider
        self.SoundFX_toggleSlider = DirectSlider(parent = self.optionsNode, pos = (0, 0.0, 0.1),
                                               value = settings['sfxVol'] * 100, pageSize = 5, range = (0, 100), command = self.__doSfxLevel)
        self.SoundFX_toggleSlider.setScale(0.4, 0.4, 0.4)
        # SFX Label
        self.SoundFX_Label = DirectLabel(parent = self.optionsNode, relief = None, text = 'SFX Volume', text_align = TextNode.ACenter, text_scale = 0.052, pos = (0, 0, 0.2))

        # Toon Chat Sound Effects
        self.ToonChatSounds_toggleButton = DirectButton(parent = self.optionsNode, relief = None, image = (guiButton.find('**/QuitBtn_UP'),
         guiButton.find('**/QuitBtn_DN'),
         guiButton.find('**/QuitBtn_RLVR'),
         guiButton.find('**/QuitBtn_UP')), image3_color = Vec4(0.5, 0.5, 0.5, 0.5), image_scale = (0.7, 1, 1), text = '', text3_fg = (0.5, 0.5, 0.5, 0.75), text_scale = 0.052, text_pos = (0, -.02), pos = (0, 0, -0.2), command = self.__doToggleToonChatSounds)
        self.ToonChatSounds_toggleButton.setScale(0.8)
        self.ToonChatSounds_Label = DirectLabel(parent = self.optionsNode, relief = None, text = 'Toon Chat Sounds', text_align = TextNode.ACenter, text_scale = 0.052, pos = (0, 0, -0.1))

        # Aspect Ratio Options
        self.AspectRatioList = DirectOptionMenu(relief = None, parent = self.optionsNode, text_align =TextNode.ACenter, pressEffect = 1, items = GraphicsOptions.AspectRatioLabels, command = self.__doWidescreen, text_scale = .6,
        image = (guiButton.find('**/QuitBtn_UP'),
        guiButton.find('**/QuitBtn_DN'),
        guiButton.find('**/QuitBtn_RLVR'),
        guiButton.find('**/QuitBtn_UP')), image_scale = 8, image3_color = Vec4(0.5, 0.5, 0.5, 0.5), text = '', text3_fg = (0.5, 0.5, 0.5, 0.75), text_pos = (1, -.02), pos = (-0.1, 0, -0.5), image_pos = (1, 0, 0))
        self.AspectRatioList.setScale(0.1)
        self.AspectRatioList.set(base.Widescreen)
        self.Widescreen_Label = DirectLabel(parent = self.optionsNode, relief = None, text = 'Aspect Ratio', text_align = TextNode.ACenter, text_scale = 0.052, pos = (0, 0, -0.4))

        # TODO: Add more graphics options like Resolution, and more graphics options like in POTCO to allow changing quality of textures, etc.

        # Set Button Text
        self.__setToonChatSoundsButton()

    def delOptions(self):
        self.optionsBox.hide()
        del self.optionsBox
        self.Music_Label.hide()
        del self.Music_Label
        self.Music_toggleSlider.hide()
        del self.Music_toggleSlider
        self.SoundFX_Label.hide()
        del self.SoundFX_Label
        self.SoundFX_toggleSlider.hide()
        del self.SoundFX_toggleSlider
        self.ToonChatSounds_Label.hide()
        del self.ToonChatSounds_Label
        self.ToonChatSounds_toggleButton.hide()
        del self.ToonChatSounds_toggleButton
        self.Widescreen_Label.hide()
        del self.Widescreen_Label
        self.AspectRatioList.hide()
        del self.AspectRatioList
        self.optionsNode.removeNode()
        del self.optionsNode

        # EZ copy from optionspage.py
    def __doMusicLevel(self):
        vol = self.Music_toggleSlider['value']
        vol = float(vol) / 100
        settings['musicVol'] = vol
        base.musicManager.setVolume(vol)
        base.musicActive = vol > 0.0

    def __doSfxLevel(self):
        vol = self.SoundFX_toggleSlider['value']
        vol = float(vol) / 100
        settings['sfxVol'] = vol
        for sfm in base.sfxManagerList:
            sfm.setVolume(vol)
        base.sfxActive = vol > 0.0

    def __doToggleToonChatSounds(self):
        messenger.send('wakeup')
        if base.toonChatSounds:
            base.toonChatSounds = 0
            settings['toonChatSounds'] = False
        else:
            base.toonChatSounds = 1
            settings['toonChatSounds'] = True
        self.settingsChanged = 1
        self.__setToonChatSoundsButton()

    def __setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

    def __doWidescreen(self, ratio):
        messenger.send('wakeup')
        ratio = self.AspectRatioList.selectedIndex
        if base.Widescreen != ratio:
            base.Widescreen = ratio
            settings['Widescreen'] = ratio
            self.settingsChanged = 1
            base.updateAspectRatio()