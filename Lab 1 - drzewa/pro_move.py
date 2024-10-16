from itertools import combinations
import pandas
import math
# from treelib import Tree

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


# Wgranie danych do dataframe'u, tym razem bez mapowania Age na sztucznie nałożone granice, ale z sortowaniem po "Age" oraz "Survived"
def prepare_pandas_df(path):
    data = pandas.read_csv(path)
    data = data.drop(['PassengerId', 'Name'], axis=1)
    data = data.sort_values(by=['Age', 'Survived']).reset_index(drop=True)
    return data


def map_splits_on_data(df, splits):
    # Funkcja pomocnicza do przypisania klasy na podstawie progów podziału
    def assign_class(age):
        for i, split in enumerate(splits):
            if age <= split:
                return i
        return len(splits)  # Jeśli większy niż ostatni próg, przypisz ostatnią klasę

    # Zastępujemy wartości w kolumnie "Age" przypisanymi klasami (ich numerami)
    df['Age'] = df['Age'].apply(assign_class)

    return df


# Funkcja wyliczająca najlepsze progi podziało dla ciągłej zmiennej "Age"
def find_best_splits_for_continuous(df, num_classes):
    if num_classes <= 1:
        return []

    # Określenie potencjalnych progów podziału (średnie wartości między punktami gdzie zmienia się klasa)
    potential_splits = []
    for i in range(len(df) - 1):
        if df['Survived'][i] != df['Survived'][i + 1]:
            potential_split = (df['Age'][i] + df['Age'][i + 1]) / 2
            potential_splits.append(potential_split)

    # Przygotowanie do znalezienia najlepszych progów podziału
    best_splits = []
    best_gain = -1

    # Kombinacje potencjalnych progów (do sprawdzenia brute-force najlepszej kombinacji)
    possible_splits = list(combinations(potential_splits, num_classes - 1))
    for split_combination in possible_splits:
        splits = []
        prev_split = 0.0

        # Podział na grupy zgodnie z kombinacją progów
        for split in split_combination:
            current_split = df[(df['Age'] > prev_split) & (df['Age'] <= split)]
            counts = [len(current_split[current_split['Survived'] == cls]) for cls in df['Survived'].unique()]
            splits.append(counts)
            prev_split = split

        # Dodanie ostatniego przedziału
        last_split = df[df['Age'] > split_combination[-1]]
        counts = [len(last_split[last_split['Survived'] == cls]) for cls in df['Survived'].unique()]
        splits.append(counts)

        # Znalezienie najlepszej kombinacji progów
        ig = information_gain(splits)
        if ig > best_gain:
            best_gain = ig
            best_splits = split_combination

    return sorted(best_splits)



dane = prepare_pandas_df("titanic-homework.csv")

best_splits = find_best_splits_for_continuous(dane, 1)
print(f"Najlepsze progi podziału: {best_splits}")

with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dane)
dane = map_splits_on_data(dane, best_splits)

with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dane)