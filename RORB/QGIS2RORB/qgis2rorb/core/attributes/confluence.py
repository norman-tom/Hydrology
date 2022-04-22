from .node import Node

class Confluence(Node):
    def __init__(self, name: str = "", x: float = 0, y: float = 0, out: bool = False) -> None:
        super().__init__(name, x, y)
        self._isOut: bool = out
        """
        Identify if this confluence is the out node, which is the last node in the graph. 
        """
    def setOut(self):
        """
        Identify that this confluence is the last node in the graph.
        """
        self._isOut = True
    
    def isOut(self) -> bool:
        """
        Returns whether this confluence is the last node in the graph.
        """
        return self._isOut