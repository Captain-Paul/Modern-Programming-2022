import networkx as nx
import matplotlib.pyplot as plt

def plot_ego(graph, node):
    adjacency_dic = {}
    for vertex in graph.getVertexList():
        adjacency_dic[vertex.getId()] = [neighbor.getId() for neighbor in vertex.getNeighbors()]
    G = nx.from_dict_of_lists(adjacency_dic)  #将自建图转化为networkx网络图以便于可视化
    
    edge_list = []
    for neighbor in node.getNeighbors():
        edge_list.append((node.getId(), neighbor.getId()))
    H = G.edge_subgraph(edge_list)  #利用边的集合取出子图
    nx.draw_networkx(H)
    plt.show()