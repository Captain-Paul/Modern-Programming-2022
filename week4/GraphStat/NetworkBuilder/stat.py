import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  #正常显示汉字
plt.rcParams['axes.unicode_minus'] = False  #正常显示负号

def get_average_degree(graph):
    tot = 0
    for vertex in graph.getVertexList():
        tot += vertex.degree
    return tot / graph.numVertex

def plot_degree_distribution(graph):
    nums = {}
    for vertex in graph.getVertexList():
        nums[vertex.degree] = nums.get(vertex.degree, 0) + 1

    plt.title('网络中各节点度的分布')
    # print(min(nums.keys()), max(nums.keys())) #度的范围[1, 35279] 但超出800的节点数量很少可忽略
    plt.xlim(min(nums.keys()), 500)
    plt.bar(nums.keys(), nums.values())
    plt.show()