import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


'''
相关说明：
本文件里面的拓扑得到的结构是吴源论文里面的拓扑结构
2个交换机，8个端节点的拓扑结构

'''
#
# row = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
# col = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

row = np.array([0,0,0,0, 1,1,1,  2,2,2,   3,3,3, 4,4,4,  5])
col = np.array([1,3,6,7, 2,4,10, 5,13,14, 4,8,9, 5,11,12, 15])

lenght = len(row)
G = nx.Graph()  # 这个拓扑是吴源论文里面的拓扑结构

# 添加节点，暂不考虑SW,ES分离开
node_id = 0
for i in range(0, np.size(col)):
    G.add_node(i, node_id=node_id)
    node_id += 1
print('在网络中添加带权中的边...')

# 删除掉多余节点，多余的节点的数量是从(15+1,len(row))
for extra_node_id in range(16, len(row)):
    G.remove_node(extra_node_id)

# 添加边，边有属性link_id
link_id = 0
for i in range(np.size(row)):
    # 这里面就说明是有三个属性的了
    G.add_edges_from([(row[i], col[i])], link_id=link_id)
    link_id += 1


# 对topo中图进行显示与调用
links = G.edges

link_id_list = []
topo_set = [] #  list是可以进行缓存的，而下面的link是不可以进行缓存的，因此是在同一层的for循环里面
for per_link in links:
    src_node = per_link[0]
    dst_node = per_link[1]
    link_id = G[src_node][dst_node]['link_id']
    link_id_list.append(link_id)
    # 每次运行，下面一行的值都会进行更新
    link = {'link_id': link_id, 'src_node': src_node, 'dst_node': dst_node}
    topo_set.append(link)
    # 最后得到的topo_set是长度是17的list
print('end')





pos = nx.spring_layout(G)
# 注意：因为draw_networkx_edge_labels需要pos,所以上面的nx.draw也得要pos，不然就会出现错位的情况
nx.draw(G, pos=pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'link_id')
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
plt.show()