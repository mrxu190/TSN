import argparse
import copy
import math
import random
from random import choice, randint
import numpy as np
import networkx as nx
import csv
import pylab
from matplotlib import pyplot as plt
from exercise.DataStruct.Data_Struct import Link, Stream, Stream_Instance
from exercise.Routing.call1 import call


class Link:
    def __init__(self, link_id, src_node, dst_node,speed):
        self.link_id = link_id  # 链路id就是链路集合数组的下标
        self.src_node = src_node
        self.dst_node = dst_node
        self.speed = speed
        self.stream_set = []

    def add_stream_to_current_link(self, stream_id, hop_id):
        self.stream_set.append({'stream_id': stream_id, 'hop_id': hop_id})

class Stream:
    def __init__(self, stream_id, size, period, latency_requirement, route_set):
        self.stream_id = stream_id
        self.size = size
        self.period = period
        self.latency_requirement = latency_requirement
        # 这条流的路由信息
        self.route_set = route_set

def decode(x):
    """解码，即基因型到表现型,
    x：要解码的数组或者是对象
    a:变量范围的下界
    b:变量范围的上界
    """
    xt = 0
    for i in range(len(x)):
        xt = xt + x[i] * np.power(2, DNA_SIZE-i-1)
    return xt
# 计算超周期的函数

def compute_hyper_period(*args):
    hyper_period=1
    for period in args:
        # 注意：下面的除号都是得转化成为int的
        hyper_period = int(hyper_period) * int(period)/math.gcd(int(hyper_period), int(period))

    # 返回值也要转化为int
    return int(hyper_period)

########  一部分公共函数的封装    ##########
def count_ones(nums):
    count = 0
    for num in nums:
        if num == 1:
            count += 1
    return count

'''*****************************************************************************************************************
第一部分：生成网络拓扑，数据流，以及链路等相关信息
'''

node_num = 20

row = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
col = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
G = nx.Graph()

ADAS_topo = nx.Graph()
row01 = np.array([0,0,0,0,  1,1,1,1,  2,2,2,2,  3,3,3,3,   4,4,4,4,4,   5,5,5,  6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
col01 = np.array([1,3,6,7,  0,2,4,10, 1,5,13,14, 0,4,8,9,  1,3,5,11,12, 2,4,15, 0, 0, 3, 3, 1,  4,  4,  2,  2,  5])

unique_row01 = np.array([0,0,0,0,0,  1,1,1,  2,2,2,2,  3,3,3,3,  4,4,4,  5,5])
unique_col01 = np.array([1,3,6,7,8,  2,4,19,  5,16,17,18,  4,9,10,11,  5,12,13,  14,15])

# 添加节点，暂不考虑SW,ES分离开
node_id = 0
for i in range(0, np.size(row)):
    G.add_node(i, node_id=node_id)
    node_id += 1
print('在网络中添加带权中的边...')

# 添加边，边有属性link_id
link_id = 0
for i in range(np.size(row)):
    G.add_edges_from([(row[i], col[i])], link_id=link_id)
    link_id += 1


############   构建图01   ############
ADAS_node_id = 0
# 下面需要注意的是，添加的node数等于node_num，而不是np.size(row01)，否则会出错
for i in range(0, node_num):
    ADAS_topo.add_node(i, node_id=ADAS_node_id)
    node_id += 1

ADAS_link_id = 0
for i in range(0, np.size(unique_row01)):
    # ADAS_topo.add_edges_from([(row01[i], col01[i])], link_id=ADAS_link_id)
    ADAS_topo.add_edges_from([(unique_row01[i], unique_col01[i])], link_id=ADAS_link_id)
    ADAS_link_id += 1

plt.show()  # 函数，将拓扑表现出来
# nx.draw(G, with_labels=True)
plt.show()
print('end')

ADAS_link_num = len(ADAS_topo.edges)
ADAS_link_Payload_list = [0]*ADAS_link_num

# ADAS的源地址和目的地址组成的list
source_list = [2, 4, 5, 8, 7, 8, 3, 6, 6, 6, 6, 3]
target_list = [7, 7, 7, 7, 3, 3, 9, 3, 7, 9, 8, 6]

ADAS_source_list = [13, 9, 6, 17, 15, 12, 19, 10, 16]
ADAS_target_list = [8, 13, 13, 13, 13, 13, 13, 13, 13]



# 1. 用nx.shortest_path求解得到最短路径（数据流链路连接而成）:shorset_path_link_list
shorset_path_node_list = []
for i in range(len(ADAS_target_list)):
    shorset_path_node = nx.shortest_path(ADAS_topo, ADAS_source_list[i], ADAS_target_list[i])
    shorset_path_node_list.append(shorset_path_node)
print('shorest_path_node_list', shorset_path_node_list)

shorset_path_link_list = []
for path in shorset_path_node_list:
    ADAS_shorset_path_link = []
    for src_node, dst_node in zip(path, path[1:]):
        path_link = ADAS_topo[src_node][dst_node]['link_id']
        ADAS_shorset_path_link.append(path_link)
    shorset_path_link_list.append(ADAS_shorset_path_link)
print('end')


##########################  part1:路由函数部分  ##########################
def update_2d_link_payload(candidate_route):
    for route in candidate_route:
        for link in route:
            TestCas01_link_Payload_list[link]+=1

ADAS_link_num = len(ADAS_topo.edges)
TestCas01_link_Payload_list = [0]*ADAS_link_num
TestCase01_TT_num = 24
TestCase01_AVB_num = 16

# TT流与AVB流候选路径
TT_route_candidate_list = shorset_path_link_list[0]
AVB_route_candidate_list = shorset_path_link_list[1:]

# AVB流确定路由+更新负载
TestCase01_AVB_route = random.choices(AVB_route_candidate_list, k=TestCase01_AVB_num)
update_2d_link_payload(TestCase01_AVB_route)

# TT流确定路由+更新负载
TestCase01_TT_route = [[x for x in list(TT_route_candidate_list)] for _ in range(TestCase01_TT_num)]
update_2d_link_payload(TestCase01_TT_route)

payload_std = np.std(TestCas01_link_Payload_list)
print('payload_std',payload_std)

SPR_route = []
SPR_route.extend(TestCase01_TT_route)
SPR_route.extend(TestCase01_AVB_route)

print('end')




############  创建link对象，从g里面得到link的属性，然后转化到自己创建的数据结构Link当中  ###############
# links = G.edges
links = ADAS_topo.edges
# 统计一共有多少链路
total_link = len(links)
print('end')

# print('links',links) # links [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (1, 7), (1, 8), (1, 9)]
link_obj_set = []
speed_set = [1000]
speed = choice(speed_set)
for link in links:
    src_node = link[0]
    dst_node = link[1]
    link_id = ADAS_topo[src_node][dst_node]['link_id']
    link = Link(src_node=src_node,
                dst_node=dst_node,
                link_id=link_id,
                speed=speed)
    link_obj_set.append(link)
print('link_obj_set', link_obj_set)# 没有输出的必要，一个list。list里面存放的是一堆对象



