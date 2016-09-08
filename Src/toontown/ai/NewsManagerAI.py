from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class NewsManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('NewsManagerAI')

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.accept('avatarEntered', self.__handleAvatarEntered)

    def __handleAvatarEntered(self, avatar):
        pass

    def setPopulation(self, todo0):
        pass

    def setBingoWin(self, todo0):
        pass

    def setBingoStart(self):
        self.sendUpdate('setBingoStart', [])

    def setBingoEnd(self):
        self.sendUpdate('setBingoEnd', [])

    def setCircuitRaceStart(self):
        pass

    def setCircuitRaceEnd(self):
        pass

    def setTrolleyHolidayStart(self):
        pass

    def setTrolleyHolidayEnd(self):
        pass

    def setTrolleyWeekendStart(self):
        pass

    def setTrolleyWeekendEnd(self):
        pass

    def setRoamingTrialerWeekendStart(self):
        pass

    def setRoamingTrialerWeekendEnd(self):
        pass

    def setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        self.sendUpdate('setInvasionStatus', args=[msgType, cogType, numRemaining, skeleton])

    def setHolidayIdList(self, holidays):
        self.sendUpdate('setHolidayIdList', holidays)

    def holidayNotify(self):
        pass

    def setWeeklyCalendarHolidays(self, todo0):
        pass

    def getWeeklyCalendarHolidays(self):
        return []

    def setYearlyCalendarHolidays(self, todo0):
        pass

    def getYearlyCalendarHolidays(self):
        return []

    def setOncelyCalendarHolidays(self, todo0):
        pass

    def getOncelyCalendarHolidays(self):
        return []

    def setRelativelyCalendarHolidays(self, todo0):
        pass

    def getRelativelyCalendarHolidays(self):
        return []

    def setMultipleStartHolidays(self, todo0):
        pass

    def getMultipleStartHolidays(self):
        return []

    def sendSystemMessage(self, todo0, todo1):
        pass

