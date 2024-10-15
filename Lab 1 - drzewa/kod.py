import math
from treelib import Tree
import pandas


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
    gr = ig / ii if ii != 0 else 0
    return gr


def prepare_pandas_df(path):
    data = pandas.read_csv(path)
    data = data.drop(['PassengerId', 'Name'], axis=1)
    return data


def prepare_pandas_df_for_basic_problem(path):
    data = pandas.read_csv(path)
    data = data.drop(['PassengerId', 'Name'], axis=1)
    data['Age'] = pandas.cut(data['Age'], bins=[0, 20, 40, 100], labels=['young', 'middle', 'old'], right=True)
    return data


def possible_values(df, column_name):
    return sorted(df[column_name].unique().tolist())


def get_column_names(df):
    return [col for col in df.columns if col != "Survived"]


def filter_count(df, column_name, value):
    filtered_df = df[df[column_name] == value]
    # print(filtered_df)
    # print(len(filtered_df))
    p = int(filtered_df['Survived'].sum())
    ile_wszystkich = len(filtered_df)
    # zawsze zwraca parę [przeżyło, nie-przeżyło]
    return [p, ile_wszystkich - p]


def split(df, column_name):
    l = []
    for val in possible_values(df, column_name):
        l.append(filter_count(df, column_name, val))
    return l


def build_tree(df, tree, columns, parent=None, parent_id="root"):
    best_gain = 0.0
    best_column = None

    for column in columns:
        ig = information_gain(split(df, column))
        if ig > best_gain:
            best_gain = ig
            best_column = column

    # print(best_gain, columns)
    # no-infinite-recursion-pls
    if best_gain == 0 or len(columns) == 0:
        return

    remaining_columns = columns.copy()
    remaining_columns.remove(best_column)

    # dawalem best_column jako id, ale robilo duplikaty, co ma sens, wiec musi tak żeby robić unikalne id
    node_id = f"{best_column}_{parent_id}"

    # Tu dodaje node do drzewa
    tree.create_node(best_column, node_id, parent=parent)

    # A tu rekurencja
    for val in possible_values(df, best_column):
        filtered_df = df[df[best_column] == val]
        child_id = f"{node_id}_{val}"
        build_tree(filtered_df, tree, remaining_columns, node_id, child_id)


def build_tree_with_decision(df, tree, columns, parent=None, parent_id="root"):
    # Jeżeli mamy pewną decyzję, to dodajemy liść z tą decyzją
    if len(df['Survived'].unique()) == 1:
        count_survived = len(df[df['Survived'] == 1])
        count_dead = len(df[df['Survived'] == 0])
        if df['Survived'].values[0] == 1:
            tree.create_node(f"Survived: {count_survived}", parent_id, parent=parent)
        else:
            tree.create_node(f"Dead: {count_dead}", parent_id, parent=parent)
        return

    # Liczymy info-gain dla każdego możliwego w tym momencie podziału
    best_gain = 0.0
    best_column = None
    for column in columns:
        ig = information_gain(split(df, column))
        if ig > best_gain:
            best_gain = ig
            best_column = column

    # Dodatkowy warunek stopu rekurencji (nigdy nie powinien zajść przy braku sprzecznych danych, ale chroni przed błędami)
    if best_gain == 0 or len(columns) == 0:
        count_survived = len(df[df['Survived'] == 1])
        count_dead = len(df[df['Survived'] == 0])
        # Tworzy liść z wynikiem
        tree.create_node(f"Survived: ? (Survived: {count_survived}, Dead: {count_dead})", parent_id, parent=parent)
        return

    # kolumnę na podstawię której właśnie dzielimy, usuwamy, przekazując do węzła-dziecka
    remaining_columns = columns.copy()
    remaining_columns.remove(best_column)
    # Nadajemy unikalne node_id, składające się z nazwy atrybutu, na podstawie którego dzielimy (best_column), oraz id węzła-rodzica, tak aby zapewnić unikalność w całym drzewie
    node_id = f"{best_column}_{parent_id}"

    # Zliczamy parametry w danym węźle i dodajemy go do drzewa
    count_survived = len(df[df['Survived'] == 1])
    count_dead = len(df[df['Survived'] == 0])

    # Tutaj dodajemy do drzewa właśnie przetwarzany węzeł
    param = parent_id.split('_')[-1]
    tree.create_node(f"{param} - {best_column} (Survived: {count_survived}, Dead: {count_dead})", node_id, parent=parent)

    # Rekurencyjnie budujemy dalej całe drzewo, przekazując do węzła-dziekca parametry pomniejszone o zużyty już parametr, oraz odpowiednio odfiltrowane dane (df i kolumn) oraz swoje id, które użyje do nadania sobie id.
    for val in possible_values(df, best_column):
        filtered_df = df[df[best_column] == val]
        id_for_child = f"{node_id}_{val}"
        build_tree_with_decision(filtered_df, tree, remaining_columns, node_id, id_for_child)


# Driver code, do testowania
dane = prepare_pandas_df_for_basic_problem("titanic-homework.csv")
decision_tree = Tree()
columns = get_column_names(dane)
build_tree_with_decision(dane, decision_tree, columns)

a = decision_tree.show(stdout=False)
print(a)


