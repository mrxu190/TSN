
import numpy as np



def decode(x, a, b):
    """解码，即基因型到表现型,
    x：要解码的数组或者是对象
    a:变量范围的下界
    b:变量范围的上界
    """
    xt = 0
    for i in range(len(x)):
        xt = xt + x[i] * np.power(2, i)
    return a + xt * (b - a) / (np.power(2, len(x)) - 1)





def decode_X(pop: np.array, lb, ub):
    """
    对整个种群的基因解码，上面的decode是对某个染色体的某个变量进行解码
    pop:种群(二进制基因)
    lb: 变量的下限列表
    ub: 变量的上限列表
    """
    X = np.zeros((NP, n_dim))  # 解码后的种群的变量值存储,(5,2)
    # 编码是编两次的，因此，一次循环里面运行一次
    indivi = np.zeros(n_dim)
    for i in range(NP):
        for j in range(n_dim):
            # 编码的时候代入的对象并不直接是pop，而是pop[0, 0*10:1*10]
            x = decode(pop[i, DNA_SIZE * j:DNA_SIZE * (j + 1)], lb[j], ub[j])
            x01 = decode(pop[i, DNA_SIZE * 0:DNA_SIZE * 1], lb[j], ub[j])
            y01 = decode(pop[i, DNA_SIZE * 1:DNA_SIZE * 2], lb[j], ub[j])
            # xi = decode(pop[i, :20], -5, 5)
            indivi[j] = x

        X[i, :] = indivi
    print('x01',x01)
    print('y01',y01)
    print('pop[0, DNA_SIZE * 0:DNA_SIZE * 1]:', pop[0, DNA_SIZE * 0:DNA_SIZE * 1])
    return X



NP=5
DNA_SIZE=10#设为20
n_dim=2
pop= np.random.randint(0, 2, (NP, DNA_SIZE*n_dim))
print('pop',pop)
lb=[-5,-5]
ub=[5,5]
X = decode_X(pop,lb,ub)
print(X)

