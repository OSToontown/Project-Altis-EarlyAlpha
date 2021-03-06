import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.wantUD = config.GetBool('want-ud', True)

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        if config.GetBool('want-ClientServicesManagerUD', self.wantUD):
            # Only generate the root object once, with the CSMUD.
            rootObj = DistributedDirectoryAI(self)
            rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        self.createGlobals()
        self.notify.info('UberDOG has successfully initialized.')
		#nice to know it didnt hang
    def createGlobals(self):
        """
        Create "global" objects.
        """
        self.csm = self.generateGlobalIfWanted(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.chatAgent = self.generateGlobalIfWanted(OTP_DO_ID_CHAT_MANAGER, 'ChatAgent')
        self.friendsManager = self.generateGlobalIfWanted(OTP_DO_ID_TT_FRIENDS_MANAGER, 'TTFriendsManager')
        if config.GetBool('want-parties', True):
            # want-parties overrides config for want-GlobalPartyManagerUD
            self.globalPartyMgr = self.generateGlobalIfWanted(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        else:
            self.globalPartyMgr = None

    def generateGlobalIfWanted(self, doId, name):
        """
        We only create the "global" objects if we explicitly want them, or if
        the config file doesn't define it, we resort to the value of self.wantUD.
        If we don't want the object, we return None.
        """
        if config.GetBool('want-%sUD' % name, self.wantUD):
            return self.generateGlobalObject(doId, name)
        else:
            return None
