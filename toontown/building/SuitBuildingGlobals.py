from ElevatorConstants import *
SuitBuildingInfo = (((1, 1), 
  (1, 3),
  (4, 4),
  (8, 10),
  (1,)), 
 ((1, 2), 
  (2, 4),
  (5, 5),
  (8, 10),
  (1, 1.2)), 
 ((1, 3),
  (3, 5),
  (6, 6),
  (8, 10),
  (1, 1.3, 1.6)), 
 ((2, 3), 
  (4, 6),
  (7, 7),
  (8, 10),
  (1, 1.4, 1.8)), 
 ((2, 4), 
  (5, 7),
  (8, 8),
  (8, 10),
  (1,
   1.6,
   1.8,
   2)), 
 ((3, 4),
  (6, 8),
  (9, 9),
  (10, 12),
  (1,
   1.6,
   2,
   2.4)), 
 ((3, 5),
  (6, 9),
  (10, 10),
  (10, 14),
  (1,
   1.6,
   1.8,
   2.2,
   2.4)),  
 ((4, 5), 
  (7, 10),
  (11, 11),
  (12, 16),
  (1,
   1.8,
   2.4,
   3,
   3.2)), 
 ((5, 5),
  (8, 11),
  (12, 12),
  (14, 20),
  (1.4,
   1.8,
   2.6,
   3.4,
   4)),  
 ((6, 6),
  (9, 12),
  (12, 12),
  (20, 25),
  (1.8,
   2.6,
   3.4,
   4.2,
   4.8,
   5.6)), 
 ((7, 7), 
  (10, 12),
  (12, 12),
  (25, 30),
  (2.6,
   3.4,
   4.2,
   4.8,
   5.6,
   6.4,
   7.2)), 
 ((1, 1), 
  (4, 12), #VP Cogs 
  (12, 12),
  (100, 100),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (8, 12), #VP Skelecogs 
  (12, 12),
  (150, 150),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (7, 12), #CFO Cogs 
  (12, 12),
  (150, 150),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (8, 12), #CFO Skelecogs 
  (12, 12),
  (200, 200),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (8, 12), #CJ Cogs 
  (12, 12),
  (300, 300),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (9, 12), #CEO Waiters 
  (12, 12),
  (275, 275),
  (1,
   1,
   1,
   1,
   1),
  (1,)),
 ((1, 1),
  (1, 5),
  (5, 5),
  (33, 33),
  (1,
   1,
   1,
   1,
   1)),
 ((1, 1),
  (4, 5),
  (5, 5),
  (50, 50),
  (1,
   1,
   1,
   1,
   1)), 
 ((1, 1),
  (11, 12), #CEO Banquet 
  (12, 12),
  (206, 206),
  (1,
   1,
   1,
   1,
   1),
  (1,)))
SUIT_BLDG_INFO_FLOORS = 0
SUIT_BLDG_INFO_SUIT_LVLS = 1
SUIT_BLDG_INFO_BOSS_LVLS = 2
SUIT_BLDG_INFO_LVL_POOL = 3
SUIT_BLDG_INFO_LVL_POOL_MULTS = 4
SUIT_BLDG_INFO_REVIVES = 5
VICTORY_RUN_TIME = ElevatorData[ELEVATOR_NORMAL]['openTime'] + TOON_VICTORY_EXIT_TIME
TO_TOON_BLDG_TIME = 8
VICTORY_SEQUENCE_TIME = VICTORY_RUN_TIME + TO_TOON_BLDG_TIME
CLEAR_OUT_TOON_BLDG_TIME = 4
TO_SUIT_BLDG_TIME = 8
