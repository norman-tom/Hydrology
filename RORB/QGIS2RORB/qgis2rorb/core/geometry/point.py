class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y
    
    def __str__(self):
        return "[{},{}]".format(self._x, self._y)
    
    def coordinates(self) ->tuple[float, float]:
        return (self._x, self._y) 
