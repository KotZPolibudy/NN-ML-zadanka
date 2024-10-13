import math
import treelib


# entropy calculation
def entropy(lista):
    e = 0
    suma = sum(lista)
    for i in lista:
        if i != 0:
            e -= (i / suma) * math.log(i / suma, 2)
    return e


# • conditional entropy calculation
def conditional_entropy(dane):
    ce = 0
    ile = 0
    for i in dane:
        ile += sum(i)
    for i in dane:
        e = entropy(i)
        ce += e * sum(i) / ile
    return ce

# information gain calculation
def information_gain(dane):
    y = 0
    n = 0
    for i in dane:
        y += i[0]
        n += i[1]
    ig = entropy([y, n]) - conditional_entropy(dane)

    return ig

# gain ratio calculation
def gain_ratio(dane):
    ig = information_gain(dane)
    ii = 0
    ile = 0
    for i in dane:
        ile += sum(i)
    for i in dane:
        ii -= (sum(i) / ile) * math.log(sum(i) / ile, 2)
    gr = ig/ii
    return gr



print(gain_ratio([[0, 2], [1, 1], [4, 2]]))
