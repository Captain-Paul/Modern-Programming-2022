class Node:
    '''
    Illustrate nodes in the network.
    Attributes:
        id, view, is_mature, life_time, create_time, update_time, is_dead, language, affiliate
    '''
    def __init__(self, views, ismature, lifetime, createtime, updatetime, id, isdead, language, affiliate):
        #实例变量
        self.views = views
        self.is_mature = ismature
        self.life_time = lifetime
        self.create_time = createtime
        self.update_time = updatetime
        self.id = id
        self.is_dead = isdead
        self.language = language
        self.affiliate = affiliate
        self.degree = 0   #节点的度
        self.adjacency = {}  #邻接表存储图结构

    def Attributes(self):
        # attributes = inspect.getmembers(Node, lambda x: not inspect.isfunction(x))
        # attributes = list(filter(lambda x: not x[0].startwith('__'), attributes))
        return self.__dict__  #以字典形式返回所有成员属性的值
    
    def getId(self):
        return self.id

    def getNeighbors(self):
        return self.adjacency.keys()  #返回与该节点相连的节点
    
    def addNeighbor(self, neighbor, weight):
        self.adjacency[neighbor] = weight
        self.degree += 1

    def delNeighbor(self, neighbor):
        if neighbor in self.adjacency:
            del self.adjacency[neighbor]