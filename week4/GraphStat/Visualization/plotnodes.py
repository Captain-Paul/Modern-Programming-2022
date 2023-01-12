import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  #正常显示汉字
plt.rcParams['axes.unicode_minus'] = False  #正常显示负号

def plot_attribute(graph, attr):
    list = []
    if attr == 'language':
        for vertex in graph.getVertexList():
            list.append(vertex.language)
        sns.displot(list)
    elif attr == 'views':
        for vertex in graph.getVertexList():
            if vertex.views != 0:
                list.append(vertex.views)
        sns.displot(list, log_scale=10)

    plt.title('网络中' + attr + '属性的分布')
    plt.savefig('attribute_' + attr + '.svg', format='svg', dpi=300)  #输出为矢量图
    plt.show()