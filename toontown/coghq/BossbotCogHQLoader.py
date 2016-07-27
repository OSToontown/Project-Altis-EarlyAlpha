from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import CogHQLoader
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
from direct.actor.Actor import Actor
from toontown.coghq import BossbotHQExterior
from toontown.coghq import BossbotHQBossBattle
from toontown.coghq import BossbotOfficeExterior
from toontown.coghq import CountryClubInterior
from pandac.PandaModules import DecalEffect, TextEncoder
import random
aspectSF = 0.7227

class BossbotCogHQLoader(CogHQLoader.CogHQLoader):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossbotCogHQLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        self.fsm.addState(State.State('countryClubInterior', self.enterCountryClubInterior, self.exitCountryClubInterior, ['quietZone', 'cogHQExterior']))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('countryClubInterior')

        self.musicFile = random.choice(['phase_12/audio/bgm/Bossbot_Entry_v1.ogg', 'phase_12/audio/bgm/Bossbot_Entry_v2.ogg', 'phase_12/audio/bgm/Bossbot_Entry_v3.ogg'])
        self.skyFile = 'phase_12/models/bossbotHQ/ttr_m_bossbothq_sky'
        self.cogHQExteriorModelPath = 'phase_12/models/bossbotHQ/CogGolfExterior'
        self.factoryExteriorModelPath = 'phase_11/models/lawbotHQ/LB_DA_Lobby'
        self.cogHQLobbyModelPath = 'phase_12/models/bossbotHQ/CogGolfLobby'
        self.geom = None
        self.activeGeysers = None
        return

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        Toon.loadBossbotHQAnims()

    def __fountainDamageTick(self, task):
        base.localAvatar.b_stun(ToontownGlobals.BossbotOilDamage)
        task.delayTime = 5.0
        return task.again

    def startFountainDamage(self, collision):
        taskMgr.add(self.__fountainDamageTick, 'oil-fountain-tick')

    def stopFountainDamage(self, collision):
        taskMgr.remove('oil-fountain-tick')

    def startCollisionDetection(self):
        self.accept('enterFountain_Geom:oil_trigger', self.startFountainDamage)
        self.accept('exitFountain_Geom:oil_trigger', self.stopFountainDamage)

    def stopCollisionDetection(self):
        taskMgr.remove('oil-fountain-tick')
        self.ignore('enterFountain_Geom:oil_trigger')
        self.ignore('exitFountain_Geom:oil_trigger')


    def unloadPlaceGeom(self):
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        CogHQLoader.CogHQLoader.unloadPlaceGeom(self)
        return

    def loadPlaceGeom(self, zoneId):
        self.notify.info('loadPlaceGeom: %s' % zoneId)
        zoneId = zoneId - zoneId % 100
        self.notify.debug('zoneId = %d ToontownGlobals.BossbotHQ=%d' % (zoneId, ToontownGlobals.BossbotHQ))
        if zoneId == ToontownGlobals.BossbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)
            gzLinkTunnel = self.geom.find('**/LinkTunnel1')
            gzLinkTunnel.setName('linktunnel_gz_17000_DNARoot')
            self.makeSigns()
            top = self.geom.find('**/TunnelEntrance')
            origin = top.find('**/tunnel_origin')
            origin.setH(-33.33)
            self.extra = Actor("phase_12/models/bossbotHQ/ttr_m_bossbothq_sky")
            self.extra.reparentTo(self.geom)
            self.extra.setPos(0,0,0)
            self.extra.setScale(2.0)
        
        elif zoneId == ToontownGlobals.BossbotLobby:
            if base.config.GetBool('want-qa-regression', 0):
                self.notify.info('QA-REGRESSION: COGHQ: Visit BossbotLobby')
            self.notify.debug('cogHQLobbyModelPath = %s' % self.cogHQLobbyModelPath)
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)
            self.extra = Actor("phase_12/models/bossbotHQ/ttr_m_bossbothq_sky")
            self.extra.reparentTo(self.geom)
            self.extra.setPos(0,0,0)
            self.extra.setScale(2.0)
        else:
            self.notify.warning('loadPlaceGeom: unclassified zone %s' % zoneId)
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)

    def makeSigns(self):

        def makeSign(topStr, signStr, textId):
            top = self.geom.find('**/' + topStr)
            sign = top.find('**/' + signStr)
            locator = top.find('**/sign_origin')
            signText = DirectGui.OnscreenText(text=TextEncoder.upper(TTLocalizer.GlobalStreetNames[textId][-1]), font=ToontownGlobals.getSuitFont(), scale=TTLocalizer.BCHQLsignText, fg=(0, 0, 0, 1), parent=sign)
            signText.setPosHpr(locator, 0, -0.1, -0.25, 0, 0, 0)
            signText.setDepthWrite(0)

        makeSign('Gate_2', 'Sign_6', 10700)
        makeSign('TunnelEntrance', 'Sign_2', 1000)
        makeSign('Gate_3', 'Sign_3', 10600)
        makeSign('Gate_4', 'Sign_4', 10500)
       # makeSign('GateHouse', 'Sign_5', 10200)
        #makeSign('GateHouse_2', 'Sign_5', 10300, TTLocalizer.BCHQLofficeText)


    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        Toon.unloadSellbotHQAnims()

    def enterStageInterior(self, requestStatus):
        self.placeClass = StageInterior.StageInterior
        self.stageId = requestStatus['stageId']
        self.enterPlace(requestStatus)

    def exitStageInterior(self):
        self.exitPlace()
        self.placeClass = None
        return
    
    def makeGeysers(self):
        self.activeGeysers = []
        geyser = loader.loadModel('phase_12/models/bossbotHQ/ttr_m_ara_bbhq_geyser')
        for geyserSpot in self.geom.findAllMatches('**/geyser*').getPaths():
            geyser.copyTo(geyserSpot)
            geyser.setScale(0.0)

        for count in ACTIVE_GEYSERS:
            taskMgr.add(self.__makeGeyserIval, 'geyser-task-' + str(count))

        geyser.removeNode()

    def __makeGeyserIval(self, task):
        geyser = random.choice(self.geom.findAllMatches('**/ttr_m_ara_bbhq_geyser*').getPaths())
        while geyser in self.activeGeysers:
            geyser = random.choice(self.geom.findAllMatches('**/ttr_m_ara_bbhq_geyser*').getPaths())

        length = random.randint(5, 15)
        task.delayTime = length + 3
        scale = random.randint(5, 18) / 10

        def geyserIval(node, scale, length):
            count = 0
            length = random.randint(5, 12)
            geyserIval = Sequence()
            while count < length:
                geyserIval.append(node.scaleInterval(1.25, scale + 0.1, blendType='easeInOut'))
                geyserIval.append(node.scaleInterval(1.25, scale, blendType='easeInOut'))
                count += 2.5

            return geyserIval

        geyserSequence = Sequence(Func(self.activeGeysers.append, geyser), geyser.scaleInterval(1.5, scale, blendType='easeOut'), geyserIval(geyser, scale, length), geyser.scaleInterval(1.5, 0.0, blendType='easeIn'), Func(self.activeGeysers.remove, geyser))
        geyserSequence.start()
        return task.again

    def destroyGeysers(self):
        for count in ACTIVE_GEYSERS:
            taskMgr.remove('geyser-task-' + str(count))

        self.activeGeysers = []

    def getExteriorPlaceClass(self):
        self.notify.debug('getExteriorPlaceClass')
        return BossbotHQExterior.BossbotHQExterior

    def getBossPlaceClass(self):
        self.notify.debug('getBossPlaceClass')
        return BossbotHQBossBattle.BossbotHQBossBattle

    def enterFactoryExterior(self, requestStatus):
        self.placeClass = BossbotOfficeExterior.BossbotOfficeExterior
        self.enterPlace(requestStatus)

    def exitFactoryExterior(self):
        taskMgr.remove('titleText')
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None
        return

    def enterCogHQBossBattle(self, requestStatus):
        self.notify.debug('BossbotCogHQLoader.enterCogHQBossBattle')
        CogHQLoader.CogHQLoader.enterCogHQBossBattle(self, requestStatus)
        base.cr.forbidCheesyEffects(1)

    def exitCogHQBossBattle(self):
        self.notify.debug('BossbotCogHQLoader.exitCogHQBossBattle')
        CogHQLoader.CogHQLoader.exitCogHQBossBattle(self)
        base.cr.forbidCheesyEffects(0)

    def enterCountryClubInterior(self, requestStatus):
        self.placeClass = CountryClubInterior.CountryClubInterior
        self.notify.info('enterCountryClubInterior, requestStatus=%s' % requestStatus)
        self.countryClubId = requestStatus['countryClubId']
        self.enterPlace(requestStatus)

    def exitCountryClubInterior(self):
        self.exitPlace()
        self.placeClass = None
        del self.countryClubId
        return
