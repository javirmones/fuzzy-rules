import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.feature_selection import SelectKBest, chi2
from new_code.fuzzyfy import fuzzy_single
from new_code.create_ddv import *
from new_code.functions import get_keys_with_value


#La idea principal de este script es ordenar las etiquetas para que
# se consiga determinar cual debe ser el orden de estas características:
def feature_selection(df_features, df_target):
    feature_selection = SelectKBest(chi2, k=5)
    feature_selection.fit(df_features, df_target)
    selected_features = df_features.columns[feature_selection.get_support()]
    return feature_selection, list(selected_features)   

#Lo primero es cargar los datos lo idoneo es trabajar con una lista en la que tengan los valores a fuzzificar 
def load_data():
    cancer = load_breast_cancer()
    df_features = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    df_target = pd.DataFrame(cancer.target, columns=['target'])
    df_target['target'].value_counts()
    df = pd.concat([df_features, df_target], axis=1)
    df['target'] = df['target'].apply(lambda x: "Benign"
                                  if x == 1 else "Malignant")

    return df, df_features, df_target

def give_new_dict(list, labels):
    new_dict = {}
    counter = 0
    for label in labels:
        if label in list:
            if label not in new_dict.keys():
                counter = 0
                for x in list:
                    if x == label:
                        counter += 1
                new_dict[label] = counter
    return new_dict
                

def create_new_order_vars(array_sep):
    dict_test = {}
    new_dictt = {}
    new_features = []
    lista = []
    df, df_features, df_target = load_data()
    feature_sel, selected_features = feature_selection(df_features, df_target)
    x = pd.DataFrame(feature_sel.transform(df_features), columns=selected_features)
    target = pd.concat([x, df['target']], axis=1)
    col_no_ordered = []

    for column in target:
        if column != 'target':
            col_no_ordered.append(target[column].values)

    ddv = divide_in_segments(target, array_sep)


    for x in range(0, len(col_no_ordered)):
        dict_test[selected_features[x]] = fuzzy_single(col_no_ordered[x], ddv, x, array_sep)


    for key, val in dict_test.items():
        dict_no_sorted = give_new_dict(val, array_sep)
        dict_sorted = sorted(dict_no_sorted.items(), key=lambda d: d[1], reverse=True)
        lista.append(dict(dict_sorted))
        dict_test[key] = dict_no_sorted

    newlist_sorted = sorted(lista, key=lambda d: d['A'], reverse=True)


    for x in newlist_sorted:
        key = get_keys_with_value(dict_test, x)
        new_features.append(key)
        new_dictt[key] = x

    print(new_dictt)

    return new_dictt, new_features
