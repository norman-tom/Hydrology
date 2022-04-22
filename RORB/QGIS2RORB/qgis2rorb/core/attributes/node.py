from qgis2rorb.core.geometry.point import Point

class Node(Point):
    def __init__(self, name: str = "", x: float = 0.0, y: float = 0.0) -> None:
        super().__init__(x, y)
        self._name: str = name

    def setName(self, name: str):
       self._name = name

    def getName(self) -> str:
        return self._name
