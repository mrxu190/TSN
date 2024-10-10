
'''
对应的博客链接：https://blog.csdn.net/weixin_45906434/article/details/115486146
建议参照博客来看

'''


import numpy as np

pop_size = 10  # 种群数量
PC = 0.6 # 交叉概率
PM = 0.01 #变异概率
X_max = 5    #最大值
X_min = 0     #最小值
DNA_SIZE = 10  #DNA长度与保留位数有关,2**10 当前保留3位小数点
N_GENERATIONS = 10  # 将循环的轮次数修改为10轮

"""
求解的目标表达式为：
y = 10 * math.sin(5 * x) + 7 * math.cos(4 * x)
x=[0,5]
"""
def aim(x):return 10*np.sin(5*x)+7*np.cos(4*x)

'''解码函数
将pop这个DNA_SIZE的基因对（DNA_SIZE位的二进制的值）变成在[X_min,X_max]区间中的十进制的值
'''
def decode(pop):
   return   pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) *(X_max-X_min)/ float(2**DNA_SIZE-1) +X_min


'''适应度函数'''
def fitnessget(pred):
    return pred + 1e-3 - np.min(pred)

'''自然选择函数'''
def select(pop, fitness):
    # print(abs(fitness))
    # print(fitness.sum())
    idx = np.random.choice(np.arange(pop_size), size=pop_size, replace=True, p=fitness/fitness.sum()) #一轮随机生成的数[9 8 1 5 2 1 8 9 1 1]
    # print(idx)
    return pop[idx]

'''交叉函数
交叉应该是有一个corss_point，这个croscc_point与本身parent二者的交叉操作到底如何？
'''
def change(parent, pop):
    if np.random.rand() < PC:    #交叉
        # 这个的最小是0，最大值是pop_size size=1和下面的做好区分，而不是说说最大值是0
        i_ = np.random.randint(0, pop_size, size=1)
        # print(parent)
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        cross_points02 = np.random.randint(0, 2, size=DNA_SIZE)  # 随机输出的值[0 0 1 0 0 0 0 1 1 1]和上面的值不一样，因为是随机生成的
        # print(np.where(cross_points==True))
        # print(cross_points)
        parent[cross_points] = pop[i_, cross_points]
        print('pop', pop)
        print('i,cross_point02',i,cross_points02)
        print('pop[i_,corss_points]', pop[i_, cross_points])
        print('parent',parent)
        # print(parent)
    return parent


'''变异函数'''
def variation(child,pm):                  #变异
    for point in range(DNA_SIZE):
        if np.random.rand() < pm:
            # 这部分实际上是 if child[point]==0 child[point]=1  其他的情况对应的是if 后面的条件，非0即1，child[point] == 1 child[point]=0, 也就是判断条件与修改的地方都是它本身
            child[point] = 1 if child[point] == 0 else 0
    # print(child)
    return child





'''main'''
pop = np.random.randint(2, size=(pop_size, DNA_SIZE))

# print(pop)
for i in range(N_GENERATIONS):
    # 解码
    # print(pop)
    X_value = decode(pop)

    # 获取目标函数值
    F_values = aim(X_value)

    # 获取适应值
    # return pred + 1e-3 - np.min(pred)
    fitness = fitnessget(F_values)
    # print(fitness)
    # 第一次做初始赋值
    if (i == 0):
        max = np.max(F_values)
        max_DNA = pop[np.argmax(F_values), :]
    # 非第一次的时候，
    if (max < np.max(F_values)):
        max = np.max(F_values)
        # np.argmax(F_values)得到的是最大值的值的下标，通过[下标，:]的形式就可以取得值，很类似于matalb的数组操作
        max_DNA = pop[np.argmax(F_values), :]

    # 每隔10次进行一次输出
    if (i % 10 == 0):
        print("Most fitted value and X: \n",
              np.max(F_values), decode(pop[np.argmax(F_values), :]),i)
    # 选择
    pop = select(pop, fitness)
    print('pop',pop)
    # 本身自带的函数
    pop_copy = pop.copy()
    print('pop_copy', pop_copy)
    for parent in pop:
        # print(parent)
        child = change(parent, pop_copy)
        child = variation(child, PM)
        # print(child)
        parent[:] = child
print("目标函数最大值为：", max)
print("其DNA值为：", max_DNA)
print("其X值为：", decode(max_DNA))

