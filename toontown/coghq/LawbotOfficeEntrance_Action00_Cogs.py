from SpecImports import *
import random
CogParent1 = 110600
CogParent2 = 110700
Battle1CellId = 0
Battle2CellId = 1
BattleCells = {Battle1CellId: {'parentEntId': CogParent1,
                'pos': Point3(0, 0, 0)},
 Battle2CellId: {'parentEntId': CogParent2,
                'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent1,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8]),
  'battleCell': Battle1CellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent1,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8]),
  'battleCell': Battle1CellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent2,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8]),
  'battleCell': Battle2CellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent2,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8]),
  'battleCell': Battle2CellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0}]
ReserveCogData = []
