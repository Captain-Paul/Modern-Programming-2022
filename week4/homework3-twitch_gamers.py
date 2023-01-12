import sys
import pandas as pd
from tqdm import tqdm
from GraphStat.NetworkBuilder import stat
from GraphStat.NetworkBuilder.node import Node
from GraphStat.NetworkBuilder.graph import Graph
from GraphStat.Visualization import plotgraph, plotnodes

# print(sys.getrecursionlimit())
sys.setrecursionlimit(100000)

node_file = pd.read_csv('E:\\BUAA\\大三上\\程设\\week4\\twitch_gamers\\large_twitch_features.csv')
edge_file = pd.read_csv('E:\\BUAA\\大三上\\程设\\week4\\twitch_gamers\\large_twitch_edges.csv')

nodes = []
for index, row in node_file.iterrows():
    nodes.append(Node(*list(row)))
print(nodes[0].Attributes())

g = Graph()
a = list(edge_file['numeric_id_1'])
b = list(edge_file['numeric_id_2'])
for i in tqdm(range(len(a))):
    g.addEdge(nodes[a[i]], nodes[b[i]], 1)
# for index, row in tqdm(edge_file.iterrows()):  #生成器速度慢于迭代器
    # g.addEdge(nodes[row['numeric_id_1']], nodes[row['numeric_id_2']], 1)
print(stat.get_average_degree(g))  #计算平均度
stat.plot_degree_distribution(g)  #绘制度的分布
plotgraph.plot_ego(g, nodes[0])  #绘制以节点0为中心的子图
plotnodes.plot_attribute(g, 'views')
plotnodes.plot_attribute(g, 'language')

g.saveGraph('demo.db')
g1 = Graph()
g1 = g1.loadGraph('demo.db')