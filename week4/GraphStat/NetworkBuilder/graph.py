import pickle

class Graph:
    '''
    Illustrate the network.
    Attributes:
        numEdge, numVertex, VertexList
        Used to build a network with undirected edges, as well as save and load it.
    '''
    def __init__(self):
        self.numEdge = 0
        self.numVertex = 0
        self.VertexList = {}
    
    def getNumEdge(self):
        return self.numEdge
    
    def getNumVertex(self):
        return self.numVertex

    def getVertexList(self):
        return self.VertexList.values()
    
    def addVertex(self, vertex):
        self.numVertex += 1
        self.VertexList[vertex.id] = vertex

    def addEdge(self, fromVertex, toVertex, weight):
        if fromVertex.id not in self.VertexList:
            self.addVertex(fromVertex)
        if toVertex.id not in self.VertexList:
            self.addVertex(toVertex)
        self.VertexList[fromVertex.id].addNeighbor(toVertex, weight)
        self.VertexList[toVertex.id].addNeighbor(fromVertex, weight)  #双向边
        self.numEdge += 1

    def saveGraph(self, file_name):
        with open(file_name, 'wb') as f:  #序列化存储图结构
            pickle.dump(self, f)

    def loadGraph(self, file_name):
        with open(file_name, 'rb') as f:  #从序列化文件加载图结构
            return pickle.load(f)