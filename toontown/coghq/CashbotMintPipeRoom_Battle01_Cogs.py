from SpecImports import *
from toontown.toonbase import ToontownGlobals
import random
CogParent = 10000
LeftCogParent = 10007
RightCogParent = 10010
BattleCellId = 0
LeftBattleCellId = 1
RightBattleCellId = 2
BattleCells = {BattleCellId: {'parentEntId': CogParent,
                'pos': Point3(0, 0, 0)},
 LeftBattleCellId: {'parentEntId': LeftCogParent,
                    'pos': Point3(0, 0, 0)},
 RightBattleCellId: {'parentEntId': RightCogParent,
                     'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 1,
  'level': 14,
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': 11,
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': 10,
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': 10,
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': LeftCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': LeftBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': LeftCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': LeftBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': LeftCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': LeftBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': LeftCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': LeftBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': RightCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': RightBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': RightCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': RightBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': RightCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': RightBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': RightCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': RightBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0}]  
ReserveCogData = []
