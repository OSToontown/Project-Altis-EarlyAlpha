from otp.ai.MagicWordGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class StaffManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("StaffManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.modsOnline = []
        self.adminsOnline = []
        self.sysadminsOnline = []

    def addModOnline(self, doId):
        self.modsOnline.append(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('modOnline', [doId])
			
    def addAdminOnline(self, doId):
        self.adminsOnline.append(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('adminOnline', [doId])
			
    def addSysAdminOnline(self, doId):
        self.sysadminsOnline.append(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('sysadminOnline', [doId])
			
    def removeModFromOnline(self, doId):
        if doId not in self.getActiveStaff():
            return
        self.modsOnline.remove(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('staffOffline', [doId])
			
    def removeAdminFromOnline(self, doId):
        if doId not in self.getActiveStaff():
            return
        self.adminsOnline.remove(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('staffOffline', [doId])
			
    def removeSysAdminFromOnline(self, doId):
        if doId not in self.getActiveStaff():
            return
        self.sysadminsOnline.remove(doId)
        for toon in self.getActiveStaff():
            self.sendUpdate('staffOffline', [doId])
			
    def getOnlineMods(self):
        return self.modsOnline
		
    def getOnlineAdmins(self):
        return self.adminsOnline
		
    def getOnlineSysAdmins(self):
        return self.sysadminsOnline
		
    def getActiveStaff(self):
        return self.modsOnline + self.adminsOnline + self.sysadminsOnline
			
