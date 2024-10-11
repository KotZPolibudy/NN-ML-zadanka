import math
import treelib

# entropy calculation
def entropia(lista):
    e = 0
    suma = sum(lista)
    for i in lista:
        e -= (i/suma) * math.log(i/suma, 2)
    return e

print(entropia([2, 4]))


