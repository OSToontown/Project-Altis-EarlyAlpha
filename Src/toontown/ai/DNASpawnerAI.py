# For DNAParsing
from DNAParser import DNAStorage
from DNAParser import *

class DNASpawnerAI: 

	def _createObjects(self, group, zone):

	if group.getName() == 'prop_game_table_DNARoot'):
          pos = group.getPos()
          hpr = group.getHpr()
          nameInfo = group.getName().split('_')
          tableIndex = int(group.parent.getName().split('_')[-1])
          picnicTable = DistributedPicnicTableAI.DistributedPicnicTableAI(simbase.air, zone, nameInfo[2], pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
          picnicTable.setTableIndex(tableIndex)
          picnicTable.generateOtpObject(simbase.air.districtId, zone, ['setX', 'setY', 'setZ', 'setH', 'setP', 'setR'])        

    for i in range(group.getNumChildren()):
            child = group.at(i)
            self._createObjects(child, zone)
        