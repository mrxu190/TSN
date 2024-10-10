# -*- coding:utf-8 -*-
# file: pygraph.py
#
'''
本文算法：最短路径算法
核心方法：递归求解最短路径

'''
def searchGraph(graph, start, end):  # 搜索树
    results = []
    generatePath(graph, [start], end, results)  # 生成路径
    results.sort(key=lambda x: len(x))  # 按路径长短排序
    return results


def generatePath(graph, path, end, results):  # 生成路径
    state = path[-1]
    if state == end:
        results.append(path)
    else:
        for arc in graph[state]:
            if arc not in path:
                generatePath(graph, path + [arc], end, results)


if __name__ == '__main__':
    Graph = {'A': ['B', 'C', 'D'],  # 构建树
             'B': ['E'],
             'C': ['D', 'F'],
             'D': ['B', 'E', 'G'],
             'E': [],
             'F': ['D', 'G'],
             'G': ['E']}
    r = searchGraph(Graph, 'A', 'D')  # 搜索A到D的所有路径
    print('************************')
    print('     path A to D')
    print('************************')
    for i in r:
        print(i)
    r = searchGraph(Graph, 'A', 'E')  # 搜索A到E的所有路径
    print('************************')
    print('     path A to E')
    print('************************')
    for i in r:
        print(i)
    r = searchGraph(Graph, 'C', 'E')  # 搜索C到E的所有路径
    print('************************')
    print('     path C to E')
    print('************************')
    for i in r:
        print(i)
