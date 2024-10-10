'''
计算链路负载以及路径长度，批量进行更新于处理的函数
ADAS_route_path_set中是以链路为链接方式的路由


'''
# 1. 得到链路数，一条链路对应一个数据流的负载。
links_num = len(ADAS_topo)
link_Payload_list = [0]*links_num

# 2. 得到所有候选路径的长度
ADAS_route_len = []
for route in num_path_list:
    cost_list = []
    for ro in route:
        cost = cal_route_cost(ro)
        cost_list.append(cost)
    ADAS_route_len.append(cost_list)
print('end')

# 3. 计算负载，最后输出的结果形式应该和上面的ADAS_route_len是一样的
'''
Q:想想函数的输入与输出是什么
'''


def find_route_payload(link_payload_list,route_p):
    '''

    :param link_payload_list: 所有链路链路负载组成的list，大小应该是16
    :param route_p: 路由所包含的链路
    :return:
    '''
    max_payload = None
    for link in route_p:
        if max_payload is None or link_payload_list[link] > max_payload:
            max_payload = link_payload_list[link]
    return max_payload


# todo:这个后续要改，因为例子里面是二维的，而ADAS中的候选路径部分是三维的
def find_route_len(route_p):
    route_len_list = []
    for route in route_p:
        route_len = len(route)
        route_len_list.append(route_len)
    return route_len_list


'''
注意：传入参数说明
payload,len
需要将负载和路径长度都作为传入的参数


'''
# 这部分返回的应该是一个值，然后反复的进行计算？或者说一下子返回也是可以的
def calc_route_cost(payload_list, len_list):# payload len 二者数组的size是一样的
    # cost_list = [0]*len(payload_list)
    cost_value_list = []
    for i in range(0,len(payload_list)):
        c1 = payload_list[i]
        c2 = len_list[i]
        cost_value = c1 + c2
        cost_value_list.append(cost_value)
    return cost_value_list


# 计算完代价函数之后，找到最小值以及相应的index
def find_mini_value(cost_value):
    min_value = min(cost_value)
    min_index = [i for i,v in enumerate(cost_value) if v==min_value]
    selected_index = random.choice(min_index)
    final_min_value = cost_value[selected_index]
    return final_min_value,selected_index


# 更新链路负载，即link_Payload_list的值会做出改变
def update_payload(selected_route):
    # 这里的link是和link_Payload_list=[0,0,0,0]的index是对应的
    for link in selected_route:
        link_Payload_list[link] += 1




# 测试案例
'''
1. 参数说明
link_Payload_list=[1,2,3,0]代表网络一共有四条链路
链路0的负载是1，链路1的负载为2，链路2的负载为3，链路3的负载为0
links=[1,2]代表网络的路由是链路1-2

2. 后续操作
确定好最大的负载之后，要进行的就是更新网络的链路负载
'''

# 1. 传入参数,所有链路组成的负载，还有路由组成的链路，两个参数组成
link_Payload_list = [0, 0, 0, 0]
links = [1, 2]
candidate_route = [[1, 2], [1, 3, 2]]  # 两条候选路径


tt_payload = 1

# 2. 计算所有候选路由的负载，是所有路由组成的链路负载的最大值
route_payload_list = []
for i in range(0,len(candidate_route)):
    link_payload = find_route_payload(link_Payload_list, candidate_route[i])
    route_payload_list.append(link_payload)

# 3. 计算所有数据流的路径长度
route_len_list = find_route_len(candidate_route)

# 4. (计算路由的评估函数)计算由路由长度与负载组成的代价函数，该部分进行封装
cost_value = calc_route_cost(route_payload_list, route_len_list)


# todo：选择其中的最优路径，然后对路径涉及到的链路进行更新，这个是单条路径的吧？就要考虑多个路径
# 5. 计算代价函数中的最小值

min_cost_value, selected_index = find_mini_value(cost_value)
selected_route = candidate_route[selected_index]

# 6. 选择最优路径之后，对网络中负载的相应情况进行更新
update_payload(selected_route)  # 注意：虽然没有返回值，但是link_Payload_list的值实际上已经变了

print('end')