from shutil import ReadError

from matplotlib.cbook import Stack
from qgis2rorb.core.attributes.basin import Basin
from qgis2rorb.core.attributes.confluence import Confluence
from qgis2rorb.core.attributes.node import Node
from qgis2rorb.core.attributes.reach import Reach
from qgis2rorb.math import geometry
import numpy as np

class Catchment:
    """
    vertices: nodes
    edges: reaches

    each vertex will know about its connected edges
    each edge will know about its connected vertices
    edges must have a vertex on both ends. 
    vertices will not know about other vertices
    reaches will not know about other reaches 
    edges will have a direction either to or away from the vertex.
    edges determine their vertices and notify the vertex of their association

    """
    
    
    def __init__(self, confluences: list[Confluence] = [], basins: list[Basin] = [],  reaches: list[Reach] = []) -> None:
        self._confluences: list[Confluence] = confluences
        self._basins: list[Basin] = basins
        self._edges: list[Reach] = reaches
        self._incidenceMatrix = np.zeros((len(self._confluences) + len(self._basins), len(self._edges)))
        self._out = 0

    def connect(self):
        """
        US = 1
        DS = 2
        not connected = 0
        
        For each edge
            for each end
                find closest vertex
                record the connection
        """
        __vertices = self._confluences + self._basins 
        
        for i, edge in enumerate(self._edges):
            s = edge.getStart()
            e = edge.getEnd()
            minStart = 999
            minEnd = 999
            closestStart = 0
            closestEnd = 0
            for j, vert in enumerate(__vertices):
                tempStart = geometry.length([vert, s])
                tempEnd = geometry.length([vert, e])
                if tempStart < minStart:
                    closestStart = j
                    minStart = tempStart
                if tempEnd < minEnd:
                    closestEnd = j
                    minEnd = tempEnd
            self._incidenceMatrix[closestStart][i] = 1
            self._incidenceMatrix[closestEnd][i] = 2   

        """
        Find the out node
        
        for each node
            if isOut == True
        """
        for k, conf in enumerate(self._confluences):  
            if conf.isOut():
                self._out = k
        
        """
        Determine direction of the edges, update the incidenceMatrix
        Update the vertex to specify downstream and upstream ends of the line
        """
        __branch = []
        __visited = np.zeros((len(__vertices), len(self._edges)))
        i = self._out
        j = 0
        __branch.append((i, j))
        while(len(__branch) != 0):
            u = __branch.pop()
            if __visited[u[0]][u[1]] == 0:
                __visited[u[0]][u[1]] = 1


        return self._incidenceMatrix