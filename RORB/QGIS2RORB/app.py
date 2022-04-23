from cProfile import label
from qgis2rorb.core.attributes.reach import Reach
from qgis2rorb.core.attributes.basin import Basin
from qgis2rorb.core.attributes.confluence import Confluence
from qgis2rorb.core.graph.catchment import Catchment
import matplotlib.pyplot as plt

def main():
    #Dummy catchment. This is after the GIS shape files have been parsed and have spit out the data
    confluences = [Confluence('1', 0.0, 0.0, True), \
        Confluence('2', 1.0, 1.0), \
        Confluence('3', 2.0, 1.0)]
    basins = [Basin('A', 2.0, 2.0, 0.5, 0.0), \
        Basin('B', 3.0, 2.0, 0.35, 0.1), \
        Basin('C', 3.0, 1.0, 1.0, 0.0), \
        Basin('D', 4.0, 1.2), \
        Basin('E', 4.2, 1.0), \
        Basin('F', 3.5, 1.5), \
        Basin('G', 3.2, 2.5)]
    reaches = [Reach('1-2', [(0.0,0.0), (1.0,1.0,)], 1, 0), \
        Reach('2-A', [(1.0,1.0),(2.0,2.0)], 1, 0), \
        Reach('2-3', [(2.0,1.0),(1.0,1.0)], 1, 0), \
        Reach('3-B', [(3.0,2.0),(2.0,1.0)], 1, 0), \
        Reach('3-C', [(3.0,1.0),(2.5,0.5),(2.0,1.0)], 1, 0), \
        Reach('C-D', [(3.0, 1.0),(4.0, 1.2)], 1, 0), \
        Reach('B-G', [(3.0, 2.0),(3.2, 2.5)], 1, 0), \
        Reach('C-E', [(3.0, 1.0),(4.2, 1.0)], 1, 0), \
        Reach('C-F', [(3.0, 1.0),(3.5, 1.5)], 1, 0)]

    #Plot the data to make sure it is correct.
    cx = []
    cy = []
    for c in confluences:
        cx.append(c.coordinates()[0])
        cy.append(c.coordinates()[1])
    
    bx = []
    by = []
    for b in basins:
        bx.append(b.coordinates()[0])
        by.append(b.coordinates()[1])


    for r in reaches:
        x = []
        y = []
        for p in r:
            x.append(p.coordinates()[0])
            y.append(p.coordinates()[1])
        plt.scatter(x, y, label=r.getName())
        plt.plot(x, y)

    plt.scatter(cx, cy)
    plt.scatter(bx, by)
    plt.legend(loc="upper left")
    plt.show()

    catchment = Catchment(confluences, basins, reaches)
    print(catchment.connect())


if (__name__ == "__main__"):
    main()