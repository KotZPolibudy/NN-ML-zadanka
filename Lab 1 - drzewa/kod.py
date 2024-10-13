import math
import treelib
import pandas


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


def prepare_pandas_df(path):
    data = pandas.read_csv(path)
    data = data.drop(['PassengerId', 'Name'], axis=1)
    return data


def possible_values(df, column_name):
    return df[column_name].unique().tolist()


def get_column_names(df):
    return df.columns.tolist()


def filtercount(df, column_name, value):
    filtered_df = df[df[column_name] == value]
    # print(filtered_df)
    return filtered_df['Survived'].sum()



print(gain_ratio([[0, 2], [1, 1], [4, 2]]))

dane = prepare_pandas_df("titanic-homework.csv")
print(dane)
print(get_column_names(dane))
print(possible_values(dane, "Pclass"))
print(filtercount(dane, "Sex", "male"))

