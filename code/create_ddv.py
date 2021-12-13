from fuzzyfy import *
from functions import *
import pandas as pd


def create_ddv(max_v, min_v, labels):
    n_parts = len(labels) +2
    step = round((max_v - min_v) / n_parts, 2)
    dict_test = {}
    lista_int = []
    intervalo = [min_v]

    for i in range(0, len(labels)):
        val = intervalo[i]
        val_aprx = round(val + step, 2)
        intervalo.append(val_aprx)
    intervalo.append(max_v)

    
    for x in range(0, len(intervalo)):
        if x == 0:
            lista_int.append([intervalo[x], intervalo[x], intervalo[x+1], intervalo[x+2]])
        elif x > 0 and x < len(intervalo) - 3:
            lista_int.append([intervalo[x], intervalo[x+1], intervalo[x+1], intervalo[x+2]])
        elif x == len(intervalo) -1:
            lista_int.append([intervalo[x-2], intervalo[x-1], intervalo[x], intervalo[x]])

    for x in range(0, len(labels)):
        dict_test[labels[x]] = lista_int[x]

    return dict_test


def divide_in_segments(df, labels):
    dict_ddv = {}
    cols = list(df.columns)
    
    for x in range(0, len(cols)-1):
        #print(cols[x])
        vals = list(df[cols[x]])
        max_v = max(vals)
        min_v = min(vals)
        dict_var = create_ddv(max_v, min_v, labels)

        str_item = "x"+str(x)
        dict_ddv[str_item] = dict_var
    return dict_ddv

def divide_in_classes(df):
    size = df.shape[1]

    fail_class = []
    pass_class = []
    notable_class = []
    for row in df.itertuples():
        list_el = list(row)[1:]
        if list_el[size-1] <= 4:
            fail_class.append([list_el[:len(list_el)-1], list_el[size-1]])
        elif list_el[size-1] > 4 and list_el[size-1] <= 6:
            pass_class.append([list_el[:len(list_el)-1], list_el[size-1]])
        elif list_el[size-1] > 6:
            notable_class.append([list_el[:len(list_el)-1], list_el[size-1]])
    return fail_class, pass_class, notable_class


