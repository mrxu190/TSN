from random import choice, randint

import networkx as nx
import numpy as np
from numpy.random import choice


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



row = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
col = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
G = nx.Graph()

# 添加节点，暂不考虑SW,ES分离开
node_id = 0
for i in range(0, np.size(col)):
    G.add_node(i, node_id=node_id)
    node_id += 1
print('在网络中添加带权中的边...')

# 添加边，边有属性link_id
link_id=0
for i in range(np.size(row)):
    G.add_edges_from([(row[i], col[i])], link_id=link_id)
    link_id += 1

source_list = [2, 4, 5, 8, 7, 8, 3, 6, 6, 6, 6, 3]
target_list = [7, 7, 7, 7, 3, 3, 9, 3, 7, 9, 8, 6]
shorset_path_node_list = []
for i in range(len(source_list)):
    shorset_path_node = nx.shortest_path(G, source_list[i], target_list[i])
    shorset_path_node_list.append(shorset_path_node)
print('shorest_path_node_list', shorset_path_node_list)

# 将path中的node编号转化为link_id编号
route_path_set = []
for shorset_path_node in shorset_path_node_list:
    shorest_path_link = []
    for src_node, dst_node in zip(shorset_path_node, shorset_path_node[1:]):
        path_link = G[src_node][dst_node]['link_id']
        shorest_path_link.append(path_link)
    route_path_set.append(shorest_path_link)
print('route_path_set', route_path_set)

'''得到拓扑的link_id'''
links = G.edges
# print('links',links) # links [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (1, 7), (1, 8), (1, 9)]
link_obj_set = []
speed_set = [1000]
speed = choice(speed_set)
for link in links:
    src_node = link[0]
    dst_node = link[1]
    link_id = G[src_node][dst_node]['link_id']
    link = Link(src_node=src_node,
                dst_node=dst_node,
                link_id=link_id,
                speed=speed)
    link_obj_set.append(link)
print('link_obj_set', link_obj_set)# 没有输出的必要，一个list。list里面存放的是一堆对象



'''创建数据流对象，以及包含的相关属性，创建数据流的前提是得到路由的相关信息:route_path_set'''
stream_num = 12
size_set = [1518]
peroid_set = [10000, 2000]
latency_requirement_set = [10000, 20000]
stream_obj_set = []
for (stream_id, route) in zip(range(stream_num), route_path_set):
    size = choice(size_set)
    index = randint(0, len(peroid_set) - 1)
    peroid = peroid_set[index]
    latency = latency_requirement_set[index]
    # stream的数据结构是dict字典
    stream = Stream(stream_id=stream_id,
                    size=size,
                    period=peroid,
                    latency_requirement=latency,
                    route_set=route)
    stream_obj_set.append(stream)

for stream in stream_obj_set:
    hop_id = 0
    for link_id in stream.route_set:
        link_obj_set[link_id].add_stream_to_current_link(stream.stream_id, hop_id)
        hop_id += 1





stream_num = 12
stream_id = 0
# 创建偏移量的字典
offset_list = []
for (stream_id, route) in zip(range(stream_num), route_path_set):
    # route是list
        for j in range(len(route)):
            # Frame Constraint：0<= fi.fai <= fi.period（实际上这部分是超周期还需要记性详细的修改计算，而且是传输周期-传输时间）
            # 后期需要修改的地方：stream_id值是需要改的
            offset = {'stream_id': stream_id, 'link_id': route[j], 'offset': randint(0, stream_obj_set[stream_id].period)}
            offset_list.append(offset)
print('offset_list', offset_list)

# 从中取出stream_id = 0的偏移量（决策变量）
result = [entry for entry in offset_list if entry['stream_id'] == 0]
print('result', result)

# result = [{'stream_id': 0, 'link_id': 1, 'offset': 8510},
#           {'stream_id': 0, 'link_id': 0, 'offset': 5304},
#           {'stream_id': 0, 'link_id': 6, 'offset': 4024}]
#
# # 循环遍历 result 中每一个元素，判断是否满足条件
# for i in range(len(result) - 1):
#     if result[i + 1]['offset'] > result[i]['offset']:
#         print('满足link constraint约束，pass')
#         pass  # 如果满足条件，则不做改变
#     else:
#         # 重新生成 offset 值，直到满足条件为止
#         while not (result[i + 1]['offset'] > result[i]['offset']):
#             print('不满足link constraint约束，重新生成')
#             result[i + 1]['offset'] = randint(result[i]['offset'] + 1, 10000)  # 同样为了避免无限循环，将最大值设为10000
#
# print(result)

import random

result03 = [{'stream_id': 3, 'link_id': 7, 'offset': 3174},
            {'stream_id': 3, 'link_id': 6, 'offset': 7109}]

result05 = [{'stream_id': 5, 'link_id': 7, 'offset': 7544},
            {'stream_id': 5, 'link_id': 0, 'offset': 8569},
            {'stream_id': 5, 'link_id': 2, 'offset': 13180}]

result10 = [{'stream_id': 10, 'link_id': 5, 'offset': 8033},
            {'stream_id': 10, 'link_id': 7, 'offset': 3232}]


# Flow Transmission Constraint,当违背了约束条件的时候，需要重新生成新的offset的值
def judge_flow_Transmission_Constraint(result):
    for i in range(len(result) - 1):
        if result[i + 1]['offset'] > result[i]['offset']:
            print('满足flow_Transmission_Constraint条件，pass')
            pass  # 如果满足条件，则不做改变
        else:
            # 重新生成 offset 值，直到满足条件为止
            while not (result[i + 1]['offset'] > result[i]['offset']):
                print('不满足条件，重新生成')
                result[i + 1]['offset'] = random.randint(result[i]['offset'] + 1, 10000)  # 同样为了避免无限循环，将最大值设为10000
    return result


result03_new = judge_flow_Transmission_Constraint(result03)
result05_new = judge_flow_Transmission_Constraint(result05)
result10_new = judge_flow_Transmission_Constraint(result10)


print(result03_new)
print(result05_new)
print(result10_new)

# 得到MakeSpan的值
def find_the_last_finish_time(result):
    MakeSpan = result[-1]['offset']
    return MakeSpan

def calculate_makespan(arg):
    MaxMakeSpan = max(item['offset'] for item in arg)
    return MaxMakeSpan

stream03_MakeSpan = find_the_last_finish_time(result03_new)
stream05_MakeSpan = find_the_last_finish_time(result05_new)
stream10_MakeSpan = find_the_last_finish_time(result10_new)

# todo:bug暂停
# MaxMakeSpan = calculate_makespan(stream03_MakeSpan, stream05_MakeSpan, stream10_MakeSpan)
# MaxMakeSpan = max(calculate_makespan(stream03_MakeSpan), calculate_makespan(stream05_MakeSpan), calculate_makespan(stream10_MakeSpan))
# print('MaxMakeSpan', MaxMakeSpan)

# todo:01 设置循环次数为100次，变化的方式为随机生成，在这100次里面找到result03，所生成的MakeSpan最小的值
# todo: 下一步的变化方式就得和遗传算法结合
G = 100
stream_id = 3
BestMakeSpan = 0
MakeSpanList = []
trans_duration = stream_obj_set[stream_id].size*8/speed


offset03_list = []
route03 = route_path_set[3]
print('route03', route03)
# 生成初始值offset03_list
# todo:后续工作：将这个封装成为一个函数，随机生成offset的函数
for i in range(len(route03)):
    offset = {'stream_id': stream_id, 'link_id': route03[i], 'offset': randint(0, stream_obj_set[stream_id].period)}
    offset03_list.append(offset)
print('offset03_list', offset03_list)

result = judge_flow_Transmission_Constraint(offset03_list)
initial_makeSpan = calculate_makespan(offset03_list)
print('judge result', result)
print('initial_makeSpan', initial_makeSpan)
# 循环100次，找到MakeSpan的最小值，生成新值的方式为随机生成randint(0, stream_obj_set[stream_id].period)
# i的作用只是循环，里面没有涉及到用i做一些别的事情


# todo:封装一个计算MakeSpan的函数
# todo:错误原因：variable_MakeSpan < BestMakeSpan都是dict，要从这个dict中计算得到makeSpan的值
# todo: 0514bug:  File "E:\+++code\open-planner-master\exercise\heredity\03 Flow Transmission Constraint and basic GA.py", line 246, in <module>
#     if variable_MakeSpan < BestMakeSpan:
# TypeError: '<' not supported between instances of 'dict' and 'dict'
'''这部分找最优值的逻辑是什么？
 ① 首先由offset03_list（初始值是在循环内部生成的还是外部生成的？）
 ② 对生成offset03_list判断是否满足约束条件（目前只有flow Trasnsmission的传输条件）
 ③ 将值进行判断是否由于最优值（MakeSpan小于已经存储的BestMakeSpan），是存储值与变量，不是继续下次循环
'''
NP = len(offset03_list)
BestMakeSpan = initial_makeSpan  # 先将初始offset的目标函数设置为最优值
BestMakeSpanlist = []
BestMakeSpanlist.append(BestMakeSpan)
best_offset_list = []
for i in range(G):
    MakeSpan_list = np.zeros((NP, 1))#存放MakeSpan的list,应该是一个steam对应一个list
    secceed_num = 0 #调度成功的数据流的数量

    variable_offset_list = []
    for i in range(len(route03)):
        # 采用随机生成的方式，在100次里面才有7次随机生成的有所改进
        variable_offset = {'stream_id': stream_id, 'link_id': route03[i], 'offset': randint(0, stream_obj_set[stream_id].period)}
        variable_offset_list.append(variable_offset)

    variable_offset01 = judge_flow_Transmission_Constraint(variable_offset_list)
    variable_MakeSpan = calculate_makespan(variable_offset01)
    if variable_MakeSpan < BestMakeSpan:
        print('最优值更新')
        BestMakeSpan = variable_MakeSpan
        best_offset_list.append(BestMakeSpan)
        BestMakeSpanlist.append(variable_MakeSpan)
print('BestMakeSpanlist', BestMakeSpanlist)
print('variable_offset01', variable_offset01)
# todo:BUG best_offset_list并不是递减的，照理说这部分应该是递减的
print('best_offset_list', best_offset_list)
print('BestMakeSpanlist', BestMakeSpanlist)
print('len of best_offset_list', len(best_offset_list))

# todo:下一步取得同一条链路上的两个数据流，做流传输约束，实际上就是两条数据流的每一个帧，在其周期内，要不在另外一个帧的开始之前传输，要不在另外一个帧结束之后传输
# todo :这部分是需要看那个程序的，有很多的帧，但是印象中的好像是两个帧之间，
