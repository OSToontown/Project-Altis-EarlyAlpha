from direct.fsm.StatePush import FunctionCall
from otp.level.EntityStateVarSet import EntityStateVarSet
from otp.level.LevelSpec import LevelSpec

class CogdoLevelGameBase:

    def getLevelSpec(self):
        return LevelSpec(self.getSpec())