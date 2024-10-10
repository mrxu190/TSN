import heapq
'''
涉及到的函数：
1. heappush(heap,item)建立大、小根堆
2 heapify(heap)建立大、小根堆（将线性列表转化为小根堆）

'''



a = []   #创建一个空堆
# 下面得到的是建立的小根堆，每次取出的时候都是取的最小的值
'''
依据后面值的大小，建立小根堆
'''
heapq.heappush(a, 18)
heapq.heappush(a, 1)
heapq.heappush(a, 20)
heapq.heappush(a, 10)
heapq.heappush(a, 5)
heapq.heappush(a, 200)
print(a)


# heapq.heappop()是从堆中弹出并返回最小的值
c=heapq.heappop(a)
print(a)
print(c)

# heapq.heapfy()是以线性时间讲一个列表转化为小根堆
a = [1, 5, 20, 18, 10, 200]
heapq.heapify(a)
print(a)
