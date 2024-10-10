import argparse
import copy
import math
import random
from random import choice, randint
import numpy as np
import csv
# import pandas as pd
import pylab
import matplotlib.pyplot as plt
import networkx as nx
# from Data_Struct import Link, Stream, Stream_Instance
from exercise.Routing.call1 import call



"""


20  code



"""



## 网络特有的结构与类link,stream
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




## 部分封装好的函数，包含compute_hyper_period,count_ones,is_increasing,all_less_than_period
# 计算超周期函数
def compute_hyper_period(*args):
    hyper_period=1
    for period in args:
        # 注意：下面的除号都是得转化成为int的
        hyper_period = int(hyper_period) * int(period)/math.gcd(int(hyper_period), int(period))
    return int(hyper_period)

def count_ones(nums):
    count = 0
    for num in nums:
        if num == 1:
            count += 1
    return count

def is_increasing(seq):
    return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))

def all_less_than_period(arr, period):
    return all(item < period for item in arr)





############## 构建网络拓扑，以及初始化对应的属性  #########
node_num=20
row = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
col = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

G = nx.Graph()
ADAS_topo = nx.Graph()

row01 = np.array([0,0,0,0,  1,1,1,1,  2,2,2,2,  3,3,3,3,   4,4,4,4,4,   5,5,5,  6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
col01 = np.array([1,3,6,7,  0,2,4,10, 1,5,13,14, 0,4,8,9,  1,3,5,11,12, 2,4,15, 0, 0, 3, 3, 1,  4,  4,  2,  2,  5])

# unique_row01 = np.array([0,0,0,0,  1,1,1,   2,2,2,   3,3,3,   4,4,4,   5])
# unique_col01 = np.array([1,3,6,7,  2,4,10,  5,13,14, 4,8,9,   5,11,12, 15])
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


links = ADAS_topo.edges
total_link = len(links)

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


# plt.show()  # 函数，将拓扑表现出来
# nx.draw(G, with_labels=True)
# plt.show()
# print('end')
# # 绘制网络拓扑图





##############   数据流路由部分  ##################
# ADAS的源地址和目的地址组成的list
source_list = [2, 4, 5, 8, 7, 8, 3, 6, 6, 6, 6, 3]
target_list = [7, 7, 7, 7, 3, 3, 9, 3, 7, 9, 8, 6]

ADAS_source_list = [13, 9, 6, 17, 15, 12, 19, 10, 16]
ADAS_target_list = [8, 13, 13, 13, 13, 13, 13, 13, 13]
# ADAS_source_list = [12, 8, 6, 13, 15, 11, 10, 9, 14, 12, 8, 6, 13, 15, 11, 10, 9, 14]
# ADAS_target_list = [7, 12, 12, 12, 12, 12, 12, 12, 12, 7, 12, 12, 12, 12, 12, 12, 12, 12 ]




# 1. 用nx.shortest_path得到数据流传输的最短路径：shorset_path_link_list
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


## 2. call函数用KSP算法得到所有的候选路径
num_path_list = call()
print('call')


# 3.将call调用的结果num_path_list中以节点连接的方式转化为以链路链接的方式
ADAS_route_path_set = []
for path_list in num_path_list:
    path_list01 = []
    for path in path_list:
        ADAS_path_link = []
        for src_node, dst_node in zip(path, path[1:]):
            path_link = ADAS_topo[src_node][dst_node]['link_id']
            ADAS_path_link.append(path_link)
        path_list01.append(ADAS_path_link)
    ADAS_route_path_set.append(path_list01)
print('end')



def calc_route_len(candidate_route_list):
    route_len_list = []
    for route in candidate_route_list:
        route_len = len(route)
        route_len_list.append(route_len)
    return route_len_list

def calc_route_payload(link_Payload_list, candidate_route_list):
    route_payload_list = []
    for route01 in candidate_route_list:
        max_payload = None
        total_payload = 0
        for link in route01:
            total_payload += link_Payload_list[link]
        route_payload_list.append(total_payload)
    return route_payload_list


''''''
#仅考虑代价函数为len（可能是AVB流的代价函数）
def calc_route_cost(route_len_list):
    route_cost_list = []
    for route_len in route_len_list:
        cost_value = route_len  # 只使用路径长度作为代价
        route_cost_list.append(cost_value)
    return route_cost_list
''''''


# 选择最小代价的路径
def select_min_route_cost(single_route_cost):
    min_value = min(single_route_cost)
    # min_index只要其值等于最小值，就返回索引index，然后从多个数组最小的index里随机选一个
    min_index = [i for i, v in enumerate(single_route_cost) if v == min_value]
    selected_index = random.choice(min_index)
    min_cost = single_route_cost[selected_index]
    return min_cost, selected_index

# 更新链路负载
def update_route_payload(selected_index ,single_ADAS_route_path):
    selected_path = single_ADAS_route_path[selected_index]
    for link in selected_path:
        ADAS_link_Payload_list[link] += 1



ADAS_link_num = len(ADAS_topo.edges)
ADAS_link_Payload_list = [0]*ADAS_link_num

final_best_route = []
total_route_cost = []
total_route_len = []
total_route_payload = []
final_index = []
for i in range(0, len(ADAS_route_path_set)):
    # 1.计算路由
    single_route_len_result = calc_route_len(ADAS_route_path_set[i])
    total_route_len.append(single_route_len_result)
    # 2. 计算负载。   计算负载时传入的是两个参数，负载列表，候选路由列表
    single_payload_result = calc_route_payload(ADAS_link_Payload_list, ADAS_route_path_set[i])
    total_route_payload.append(single_payload_result)
    # 3.计算代价函数
    ''''''
    route_cost_list01 = calc_route_cost(single_route_len_result)
    ''''''
    total_route_cost.append(route_cost_list01)
    # 4.选择最小的代价函数与其对应的index,并得到最终的最优路径
    # 但是下面返回值的最小值代价函数值好像没有什么用，因为要的是具体的路由
    min_cost_value, selected_index = select_min_route_cost(route_cost_list01)
    final_index.append(selected_index)
    # 5.得到了最终的最优路由
    final_best_route.append(ADAS_route_path_set[i][selected_index])  # 最终的最优路由部分
    # 5.更新负载
    update_route_payload(selected_index, ADAS_route_path_set[i])
print('end')




############################ 路由算法部分     ############################

def calc_TT_route_len(TT_route):
    TT_route_len_list = []
    for route in TT_route:
        route_len = len(route)
        TT_route_len_list.append(route_len)
    return TT_route_len_list

def calc_TT_route_payload(TT_route):
    TT_route_payload_list = []
    for route in TT_route:
        total_payload = 0
        for link in route:
            # 计算的链路负载是路由所包含链路所有的负载值之和
            total_payload += TestCas01_link_Payload_list[link]
        TT_route_payload_list.append(total_payload)
    return TT_route_payload_list

''''''
# 仅考虑代价函数为len的TT流
def calc_TT_route_cost(TT_route_len_list):
    route_cost_list = []
    for route_len in TT_route_len_list:
        cost_value = route_len  # 只使用路径长度作为代价
        route_cost_list.append(cost_value)
    return route_cost_list
''''''




'''这里的目的是找到最终的路由！最后输出的是一个路由！'''


# 选择最小代价的路径
def select_min_cost_route(route_cost_list):
    final_cost = 0
    min_cost_value = min(route_cost_list)
    # 下面两行作用：当有两个相同的值的时候随机选择
    min_index = [i for i, v in enumerate(route_cost_list) if v == min_cost_value]
    if len(min_index) == 1:
        final_cost = min_cost_value
        selected_index = min_index[0]
    else:
        selected_index = random.choice(min_index)
        final_cost = route_cost_list[selected_index]
    return selected_index

def update_1d_link_payload(route):
    for link in route:
        TestCas01_link_Payload_list[link] += 1

def update_2d_link_payload(candidate_route):
    for route in candidate_route:
        for link in route:
            TestCas01_link_Payload_list[link] += 1




###############   本文实验的路由函数部分     ####################
TestCas01_link_Payload_list = [0]*ADAS_link_num


# 如果用到LB-KPR的话，值是需要改的，并且和下面的stream_num作对应
TestCase01_TT_num = 24  # 此部分的值是需要修改的
TestCase01_AVB_num = 12# 此部分的值是需要修改的

TT_route_candidate_list = ADAS_route_path_set[0]# TT流的候选路径集合，是从KSP算法中进行挑选出来的
AVB_route_candidate_list = ADAS_route_path_set[1:]# AVB流的候选路径集合

# 将AVB流候选列表展成一维的
expanding_AVB_route_candidate_list = []
for item in AVB_route_candidate_list:
    for route in item:
        expanding_AVB_route_candidate_list.append(route)

print('end')

## 主体的函数部分
TestCase01_AVB_route = []

# 一、AVB采用本文提出算法部分
for i in range(0, TestCase01_AVB_num):

    # 1.计算得到路由的代价函数
    AVB_route_len_list = calc_TT_route_len(expanding_AVB_route_candidate_list)
    AVB_route_payload_list = calc_TT_route_payload(expanding_AVB_route_candidate_list)
    route_cost_list03 = calc_TT_route_cost(AVB_route_len_list)


    # 2.选择代价函数最小的index
    selected_index01 = select_min_cost_route(route_cost_list03)
    AVB_route = expanding_AVB_route_candidate_list[selected_index01]

    # 3.对负载进行更新,因为本身已经在循环里，所以一次给的事一条路径，就有以一维的更新
    update_1d_link_payload(AVB_route)

    # 4.将最终的AVB流的路由加入到final_AVB_route_list中
    TestCase01_AVB_route.append(AVB_route)
print('end')

# 二、AVB采用随机路由的部分
# TestCase01_AVB_route = random.choices(expanding_AVB_route_candidate_list, k=TestCase01_AVB_num)
# update_2d_link_payload(TestCase01_AVB_route)

TestcaseCase01_TT_route = []

# 一、TT采用本文路由
for i in range(0, TestCase01_TT_num):
    TT_route_len_list = calc_TT_route_len(TT_route_candidate_list)
    TT_route_payload_list = calc_TT_route_payload(TT_route_candidate_list)
    route_cost_list02 = calc_TT_route_cost(TT_route_len_list)

    selected_index = select_min_cost_route(route_cost_list02)
    TT_route = TT_route_candidate_list[selected_index]
    update_1d_link_payload(TT_route)  # 最后改变的是TestCas01_link_Payload_list的值，但是没有看到
    TestcaseCase01_TT_route.append(TT_route)
print('end')

# 二、TT采用随机路由
# TestcaseCase01_TT_route = random.choices(TT_route_candidate_list, k=TestCase01_TT_num)
# update_2d_link_payload(TestcaseCase01_TT_route)

# # 计算负载的标准差，最后出的数据部分从这里看！
# payload_std = np.std(TestCas01_link_Payload_list)# np.std(link_payload_list) 使用 NumPy 库来计算该列表的标准差，就是文中公式的实现
# print('end')
# Standard deviation of payloads across all links in the ADAS topology
payload_std = np.std(TestCas01_link_Payload_list)
print(f"Standard deviation of link payloads: {payload_std}")