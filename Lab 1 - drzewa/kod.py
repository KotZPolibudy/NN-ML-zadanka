import math
import treelib

# entropy calculation
def entropia(lista):
    e = 0
    sum = 0
    for i in lista:
        sum += i
    for i in lista:
        e -= (i/sum) * math.log(i/sum, 2)
    return e

print(entropia([2, 4]))
