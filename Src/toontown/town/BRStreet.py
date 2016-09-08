from direct.task.Task import Task
import random
from pandac.PandaModules import Vec3

from toontown.town.Street import Street
 


class BRStreet(Street):
    def __init__(self, loader, parentFSM, doneEvent):
        Street.__init__(self, loader, parentFSM, doneEvent)


    def enter(self, requestStatus):
        Street.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self.__windTask, 'BR-wind')

    def exit(self):
        Street.exit(self)
        taskMgr.remove('BR-wind')
        
    def __windTask(self, task):
        base.playSfx(random.choice(self.loader.windSound))
        time = random.random() * 8.0 + 1
        taskMgr.doMethodLater(time, self.__windTask, 'BR-wind')
        return Task.done