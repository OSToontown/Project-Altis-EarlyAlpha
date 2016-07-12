from SpecImports import *
import random
CogParent = 10000
LowerCogParent = 10003
BattleParent = 10002
LowerBattleParent = 10005
FrontCogParent = 10013
CenterCogParent = 10040
BattleCellId = 0
LowerBattleCellId = 1
FrontBattleCellId = 2
CenterBattleCellId = 3
BattleCells = {BattleCellId: {'parentEntId': BattleParent,
                'pos': Point3(0, 0, 0)},
 LowerBattleCellId: {'parentEntId': LowerBattleParent,
                     'pos': Point3(0, 0, 0)},
 FrontBattleCellId: {'parentEntId': FrontCogParent,
                     'pos': Point3(0, 0, 0)},
 CenterBattleCellId: {'parentEntId': CenterCogParent,
                      'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([9, 10, 11, 12]),
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0, 1])},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': LowerCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': LowerBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': LowerCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': LowerBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': LowerCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': LowerBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': LowerCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': LowerBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': FrontCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': FrontBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': FrontCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': FrontBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': FrontCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': FrontBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': FrontCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': FrontBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': CenterCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': CenterBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])},
 {'parentEntId': CenterCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': CenterBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': CenterCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': CenterBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1,
  'revives': random.choice([0])},
 {'parentEntId': CenterCogParent,
  'boss': 0,
  'level': random.choice([6, 7, 8, 9, 10, 11, 12, 13]),
  'battleCell': CenterBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': random.choice([0, 1])}]
ReserveCogData = []
