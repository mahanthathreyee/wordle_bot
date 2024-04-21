from enum import Enum

class TileType(Enum):
    INCORRECT=0
    MISPLACED=1
    CORRECT=2
    
    #region Decorators
    def __json__(self):
        return self.name
    #endregion
