import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

fig = plt.figure()

#создание списка матриц
facie_cube = input("УКАЖИТЕ ТОЧНЫЙ ПУТЬ К ДАННЫМ: ")
data1 = pd.read_table(facie_cube, sep=' ', header=None, names=['i','j','k','a','f'], skiprows=5)
data1 = data1.drop(columns='a')
matrices = []
for k in data1['k'].unique():
    matrix_k = data1[data1['k'] == k].pivot_table(index='j', columns='i', values='f')
    matrices.append(matrix_k)

#создание пустого тензора данных
uniq = data1['f'].unique()
shapes  = [matrix.shape for matrix in matrices]
shape = max(shapes)
index = 0
for i in enumerate(matrices):
    if i[1].shape == shape:
        index+=i[0]
        break
tensor = matrices[index].copy()
tensor.replace(to_replace=tensor.values, value=0, inplace=True)

#создание функции, которая возвращает вектор вероятности и энтропию для соответствующего узла
def tensorator(o, p):
    vector = {}
    sum = 0
    for k in range(len(matrices)):
        value = matrices[k].loc[p,o]
        if value in vector:
            vector[value] += 1
            sum+=1
        else:
            vector[value] = 1
            sum+=1
    if len(vector)!=0:
        for key in vector:
            vector[key] = vector[key]/sum
    el_tensor = [vector.get(key,0) for key in uniq]
    if len(el_tensor)==0:
        return 0
    else:     
        entropy = 0
        for p in el_tensor:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy


#проход по каждому узлу
for i in range(1,shape[1]+1):
    for j in range(1,shape[0]+1):
        tensor.loc[j,i] = tensorator(i,j)

#создание тепловой карты
sns.heatmap(tensor)
plt.title('Карта энтропии')
plt.show()
# в функции tensorator оставлен вектор вероятности el_tensor. 
# Изменив вывод данных можно получить закон распределения случайной величины, 
# описывающий вероятность появления того или иного литологического события для каждой точки.
# Это может понадобиться для более детального анализа местности.