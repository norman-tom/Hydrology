from qgis2rorb.core.gis.line import Line
from qgis2rorb.core.gis.polygon import Polygon

def createLine(length:int):
    line = []
    for x in range(length):
        y = pow(x , 1)
        line.append((x, y))
    return line

def main():
    v = createLine(11)
    poly = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    for p in poly:
        print(p)
    
    print(poly.length())
    print(poly.area())
    print(poly.centroid())

if (__name__ == "__main__"):
    main()