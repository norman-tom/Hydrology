import numpy as np

from qgis2rorb.core.graph.catchment import Catchment

class Traveller:
    def __init__(self, catchment: Catchment):
        self._colour = np.zeros(len(catchment._incidenceMatrixDS), dtype=int)
        self._us = catchment._incidenceMatrixUS
        self._ds = catchment._incidenceMatrixDS
        self._endSentinel = catchment._endSentinel
        self._pos = 0

    def up(self, i: int) -> int:
            for val in self._us[i]:
                if val != -1:
                    if self._colour[val] == 0:
                        return self.up(val)
                    else:
                        continue
            return i

    def down(self, i: int) -> int:
        self._colour[i] = 1
        for val in self._ds[i]:
            if val != -1:
                return val
        return self._endSentinel
    
    def next(self) -> int:
        up = self.up(self._pos)
        if up == self._pos:
            self._pos = self.down(self._pos)
            return up
        else:
            self._pos = up
            return self.next()
    
    def setPos(self, i: int) -> None:
        self._pos = i