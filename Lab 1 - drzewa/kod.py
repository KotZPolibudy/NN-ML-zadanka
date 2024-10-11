import math
import treelib

# entropy calculation
def entropia(lista):
    e = 0
    suma = 0
    for i in lista:
        suma += i
    sum2 = sum(lista)
    print(sum2)
    for i in lista:
        e -= (i/suma) * math.log(i/suma, 2)
    return e

print(entropia([2, 4]))
