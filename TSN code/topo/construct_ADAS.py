import math
from random import choice, randint, random
from tkinter import _flatten

from z3 import And, Solver, sat, unsat, unknown

import networkx as nx
import matplotlib.pyplot as plt


from lib.z3_constraints_solver import _parse_z3_model
from z3 import *
'''
构建吴源论文里面的ADAS拓扑，其中有两个交换机，每个交换机有4个端系统
仿照|open-planner构造相应的拓扑

'''
G=nx.DiGraph()
sw_id = 0
es_id = 0
sw_num = 2
es_num_of_current_per_sw_set=[4]
sw_set = []# 交换机的集合
es_set = []# 端系统的集合

# 一、构造交换机节点
for sw in range(sw_num):
    G.add_node(sw_id, node_id=sw_id, type='SW', es_set=[])
    sw_id+=1


# 二、构造端系统节点，
# tips:在构造终端节点的时候就把es_set的集合得到了
es_id=es_id+sw_num
for sw in range(sw_num):
    for es in range(choice(es_num_of_current_per_sw_set)):
        G.add_node(es_id, node_id=es_id, type='ES')
        es_id+=1

# 三、构造交换机之间的连线
link_id=0
sw_id_set = range(0, sw_num)
for sw in sw_id_set[0:-1]:
    G.add_edge(sw,sw+1,link_id=link_id)
    link_id+=1
    G.add_edge(sw+1,sw,link_id=link_id)
    link_id+=1


# 四、构造交换机与端系统之间的连线
# 报错:node只是一个index，是中间变量不能够直接用的
# 1.确定交换机的集合
for node in G.nodes:
    if G.nodes[node]['type']=='SW':
    # if node['type']=='SW':  错误原因，node是一个index,而不是相关的变量
        sw_set.append(node)
print(sw_set)




nx.draw(G, with_labels=True)
plt.show()