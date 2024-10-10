import random

def tsp_mutation(path, mutation_rate):
    mutated_path = path.copy()
    for i in range(len(mutated_path)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(mutated_path) - 1)
            mutated_path[i], mutated_path[j] = mutated_path[j], mutated_path[i]
    return mutated_path

def tsp_solver(num_cities, num_generations, population_size, mutation_rate):
    # 初始化种群
    population = []
    for _ in range(population_size):
        path = list(range(num_cities))
        random.shuffle(path)
        population.append(path)

    # 进化过程
    for _ in range(num_generations):
        # 变异
        for i in range(population_size):
            mutated_path = tsp_mutation(population[i], mutation_rate)
            population[i] = mutated_path

        # 其他操作（交叉、选择等）

    # 返回最优路径
    best_path = min(population, key=lambda x: fitness(x))  # 假设有自定义的适应度函数fitness()
    return best_path

# 示例调用
num_cities = 10  # 城市数量
num_generations = 100  # 进化代数
population_size = 50  # 种群大小
mutation_rate = 0.2  # 变异概率

best_path = tsp_solver(num_cities, num_generations, population_size, mutation_rate)
print("Best path:", best_path)
