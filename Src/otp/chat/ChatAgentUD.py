import time

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
# TODO: OTP should not depend on Toontown... Hrrm.
from toontown.chat.TTWhiteList import TTWhiteList
import datetime
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.distributed import OtpDoGlobals
from toontown.toonbase import TTLocalizer

accountDBType = simbase.config.GetString('accountdb-type', 'developer')
from passlib.hash import bcrypt

BLACKLIST = TTLocalizer.Blacklist
OFFENSE_MSGS = ('Woah! The Toon Council is watching you! You said: %s', 'Watch your language! This is your first offense. You said "%s".',
                'Watch your language! This is your second offense. Next offense you\'ll get banned for 24 hours. You said "%s".')

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ChatAgentUD')
    notify.setInfo(True)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.whiteList = TTWhiteList()
        self.muted = {}
        self.offenses = {}

    def muteAccount(self, account, howLong):
        print ['Muted', account, howLong]
        self.muted[account] = int(time.time()/60) + howLong
        
    def persistChat(self, sender, message):
        pass

    def unmuteAccount(self, account):
        print ['unuteAccount', account]
        if account in self.muted:
            del self.muted[account]

    def chatMessage(self, message, chatMode):
        self.whiteList = TTWhiteList()

        sender = self.air.getAvatarIdFromSender()
        now = time.strftime("%c")
        if sender == 0:
            self.air.writeServerEvent('suspicious', self.air.getAccountIdFromSender(),
                                         'Account sent chat without an avatar', message)
            return

        if sender in self.muted and int(time.time()/60) < self.muted[sender]:
            return

        if chatMode == 0:
            if self.detectFoul(self.air.getMsgSender(), message):
                print self.air.getMsgSender, ' said ', message
                return

        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = config.GetBool('want-whitelist', 1)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        self.air.writeServerEvent('chat-said', sender, message, cleanMessage)
        
        self.air.friendsManager.checkOnline(sender)

        # TODO: The above is probably a little too ugly for my taste... Maybe AIR
        # should be given an API for sending updates for unknown objects?
        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, sender,
                                              self.air.ourChannel,
                                              [0, 0, '', message, modifications, 0])
        self.air.send(dg)

        print 'ChatAgentUD:', sender, ':', message



    def detectFoul(self, sender, message):
        words = message.split()
        print words
        for word in words:
            if word.lower() in BLACKLIST:
                accountId = (sender >> 32) & 0xFFFFFFFF
                avId = sender & 0xFFFFFFFF
               
                if not sender in self.offenses:
                    self.offenses[sender] = 0
                   
               
                if self.offenses[sender] >= 3:
                    msg = 'Banned'    
                   
                else:
                    msg = OFFENSE_MSGS[self.offenses[sender]] % word
                    dclass = self.air.dclassesByName['ClientServicesManagerUD']
                    dg = dclass.aiFormatUpdate('systemMessage',
                               OtpDoGlobals.OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                               sender, 1000000, [msg])
                    self.air.send(dg)
                    #self.air.banManager.ban(sender, 2, 'language')
                   
                self.air.writeServerEvent('chat-offense', accountId, word=word, num=self.offenses[sender], msg=msg)
                if self.offenses[sender] >= 3:
                    del self.offenses[sender]
                   
                return 1
               
        return 0 