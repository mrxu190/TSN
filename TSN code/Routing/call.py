from exercise.Routing.new_version_ksp04 import Graph

# from exercise.Routing.GA_schedling import *

g = Graph()


"""

24code

"""



###### 注意：这部创建的拓扑实际上是我自己的拓扑########
g.add_vertex('a', {'b': 1, 'd': 1, 'g': 1, 'i': 1, 'h': 1, 'u':1})
g.add_vertex('b', {'a': 1, 'c': 1, 'e': 1, 't': 1})
g.add_vertex('c', {'b': 1, 'f': 1, 'q': 1, 'r': 1, 's': 1, 'x':1})
g.add_vertex('d', {'a': 1, 'e': 1, 'k': 1, 'j': 1, 'l': 1, 'v':1})
g.add_vertex('e', {'f': 1, 'd': 1, 'b': 1, 'n': 1, 'm': 1})
g.add_vertex('f', {'c': 1, 'e': 1, 'p': 1, 'o': 1, 'w':1})
g.add_vertex('g', {'a': 1})
g.add_vertex('h', {'a': 1})
g.add_vertex('i', {'a': 1})
g.add_vertex('j', {'d': 1})
g.add_vertex('k', {'d': 1})
g.add_vertex('l', {'d': 1})
g.add_vertex('m', {'e': 1})
g.add_vertex('n', {'e': 1})
g.add_vertex('o', {'f': 1})
g.add_vertex('p', {'f': 1})
g.add_vertex('q', {'c': 1})
g.add_vertex('r', {'c': 1})
g.add_vertex('s', {'c': 1})
g.add_vertex('t', {'b': 1})
g.add_vertex('u', {'a': 1})
g.add_vertex('v', {'d': 1})
g.add_vertex('w', {'f': 1})
g.add_vertex('x', {'c': 1})

start = 'i'
end = 'm'

start_list = ['n', 'j', 'g', 'r', 'p', 'm', 't', 'k', 'q']
end_list = ['i', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
# start_list = ['m', 'i', 'g', 'n', 'p', 'l', 'k', 'j', 'o']
# end_list = ['h', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm']

'''
20231222一次修改的尝试
对网络中数据流的数量进行修改，源地址和目的地址都不变
只是在此基础上进行加倍
'''
# start_list = ['m', 'i', 'g', 'n', 'p', 'l', 'k', 'j', 'o', 'm', 'i', 'g', 'n', 'p', 'l', 'k', 'j', 'o']
# end_list = ['h', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'h', 'm', 'm', 'm', 'm', 'm', 'm', 'm', 'm']

'''
存在这样一个问题：
那就是只能够采用这样的方式进行计算吗？
都要手动的输入start_list,end_list的列表

'''

k = 10

paths_list = []

# TT流与AVB流的相关属性
# TT_stream_num = 24
# TT_period = 1000 # 周期的为1000ms
# TT_size = 64 # 64B
# TT_latency_requirement = 1000 # 先定义截止时间等于周期
# TT_src_set=[]
# TT_dest_set=[]
# # TT_route_set =
# AVB_stream_num = 8


'''
函数执行流程：
1. 批量化进行最短路径算法调用  def batch_k_shorest_path(start_list,end_list,k):
——调new_version_ksp04中的g.k_shortest_paths函数

2. 去掉重复的
——采用set的属性来去掉重复的

3. def convert_char_to_num(final_paths_list):
——ascii码转化


【注】：相应流程
paths_list——unique_paths_list——num_path_list


paths_list = batch_k_shorest_path(start_list, end_list, 10)
unique_paths_list = get_unique_path(paths_list)
num_path_list = convert_char_to_num(unique_paths_list)

'''


############## 【begin:函数01】batch_k_shorest_path，批量化生成最短路径     ################
def batch_k_shorest_path(start_list, end_list, k):
    for i in range(len(start_list)):
        # 实际上是嗲用了new_version_ksp里面的函数
        paths = g.k_shortest_paths(start_list[i], end_list[i], k)
        paths_list.append(paths)
    return paths_list


# 测试函数：调用k_shorest_path
paths_list = batch_k_shorest_path(start_list, end_list, 10)
print('end')


############## 【begin:函数02】get_unique_path，去掉往回走的路径     ################
def get_unique_path(paths_list):
    unique_paths_list = []
    for i01 in range(len(start_list)):
        unique_paths = []
        for path01 in paths_list[i01].keys():
            # 需要弄清楚什么时候是需要清空的
            # unique_paths = []
            # 如果unique_paths = []在循环外边的话，那么里面进行循环结束是一定会有值的
            # 下面的这行是实现的核心函数
            if len(path01) == len(set(path01)):
                unique_paths.append(path01)
        unique_paths_list.append(unique_paths)
    return unique_paths_list


# 测试函数：调用get_unique_path函数，将unique_paths_list->final_paths_list 将重复出现的路径删除掉
unique_paths_list = get_unique_path(paths_list)
print('end')


############## 【begin:函数02】convert_char_to_num，将网络中的字母节点转化为数字     ################
def convert_char_to_num(unique_paths_list):
    num_path_list = []
    for i02 in range(len(unique_paths_list)):
        num_list_01 = []
        for path02 in unique_paths_list[i02]:
            num_list = []
            for c01 in path02:  # num_list每次都是for c01 in path02这样的一组元素作为添加的基本单位
                ascii_code = ord(c01)
                ascii_code_to_num = ascii_code - 97
                num_list.append(ascii_code_to_num)
            num_list_01.append(num_list)
        num_path_list.append(num_list_01)
    return num_path_list


# todo:num_path_list得到的就是全部的可行的路由的集合了
num_path_list = convert_char_to_num(unique_paths_list)
print('num_path_list', num_path_list)
print('end')


def call():
    # 1. 首先批量获得ksp路径
    paths_list = batch_k_shorest_path(start_list, end_list, 5)
    # 2. 将重复的路径去除
    unique_paths_list = get_unique_path(paths_list)
    # 3. 将字母的路径转化为数字的路径
    num_path_list = convert_char_to_num(unique_paths_list)
    return num_path_list
