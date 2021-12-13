
import pandas as pd
import warnings
import pprint
from fuzzyfy import *
from functions import *
from create_ddv import *

warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from order_features import create_new_order_vars
from classifier import *
array_sep = [ "A", "B", "C", "D", "E", "F", "G"]

def load_data():
    cancer = load_breast_cancer()
    df_features = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    df_target = pd.DataFrame(cancer.target, columns=['target'])
    df_target['target'].value_counts()
    df = pd.concat([df_features, df_target], axis=1)
    df['target'] = df['target'].apply(lambda x: "Benign"
                                  if x == 1 else "Malignant")

    return df, df_features, df_target


def dist_features(df, df_features):
    scaler = StandardScaler()
    scaler.fit(df_features)
    features_scaled = scaler.transform(df_features)
    features_scaled = pd.DataFrame(data=features_scaled,
                                columns=df_features.columns)
    df_scaled = pd.concat([features_scaled, df['target']], axis=1)    

    df_scaled_melt = pd.melt(df_scaled, id_vars='target',
                            var_name='features', value_name='value')
    print(df_scaled_melt.head(3))
    return df_scaled_melt


def feature_selection(df_features, df_target):
    feature_selection = SelectKBest(chi2, k=5)
    feature_selection.fit(df_features, df_target)
    selected_features = df_features.columns[feature_selection.get_support()]
    return feature_selection, list(selected_features)   

def divide_classes(list_t):
    maligno = []
    benigno = []
    for x in range(0,len(list_t)):
        if list_t[x][1] == 'Malignant':
            maligno.append(list_t[x])
        elif list_t[x][1] == 'Benign':
            benigno.append(list_t[x])
    return maligno, benigno

def main():
    list_class = []

    n_it = 10
    class_names = ['Benign', 'Malignant']
    df, df_features, df_target = load_data()
    n_features = 5
    feature_sel, selected_features = feature_selection(df_features, df_target)

    print(feature_sel)


    x = pd.DataFrame(feature_sel.transform(df_features), columns=selected_features)
    target = pd.concat([x, df['target']], axis=1)
    dic_fuzzy, new_features = create_new_order_vars(array_sep)
    size = target.shape[1]
    new_features.append("target")
    new_df = target.reindex(columns=new_features)


    for row in new_df.itertuples():
        lista = list(row)
        list_class.append([lista[1:size], str(lista[size:size+1][0])])

    
    
    avg_amp = []
    avg_else = []

    for x in range(1, n_it+1):
        print("Iteracion" +str(x))
        mal, beg = divide_classes(list_class)
        print("maligno")
        print(len(mal))
        print("benigno")
        print(len(beg))
        t_mal, test_mal = divide_train_test(mal, 0.8, 0.2)
        t_beg, test_beg = divide_train_test(beg, 0.8, 0.2)

        ddv = divide_in_segments(new_df, array_sep)
    
        rules_mal = calc_new_rules(t_mal, ddv, array_sep)
        rules_beg = calc_new_rules(t_beg, ddv, array_sep)
        

        list_mal= return_list(rules_mal)
        list_beg = return_list(rules_beg)

        dict_labels = create_label_order(array_sep)

        reglas_malamp = amplify_algorithm(list_mal, list_beg, array_sep, dict_labels, 'Malignant')
        reglas_begamp = amplify_algorithm(list_beg, list_mal, array_sep, dict_labels, 'Benign')


        rules_amp_mal = reestructure_rules(reglas_malamp, array_sep)
        rules_amp_beg = reestructure_rules(reglas_begamp, array_sep)

        reglas_else_mal = elsevier_algorithm(list_mal, list_beg, n_features, 'Malignant')
        reglas_else_benign = elsevier_algorithm(list_beg, list_mal, n_features, 'Benign')


        test_data = test_mal + test_beg
        rules_amp = rules_amp_mal + rules_amp_beg
        rules_else = reglas_else_mal + reglas_else_benign

        print("Ejemplos entrenamiento: " +str(len(t_mal)+len(t_beg)))
        print("Ejemplos prueba: " +str(len(test_data)))
        #print("Alg amplify")
        percent, tuple_list, rules = ejecutar_clasificacion(test_data, "Amplify", rules_amp, ddv, array_sep)
        #print("Acierto/NC/Fallo")
        #print(percent)

        #for x in tuple_list:
         #   print(x)
        
        #print("Reglas amp")
        #pprint.pprint(rules)
        print("Alg Elsevier")
        percent_else, tuple_list_else, rules_else = ejecutar_clasificacion(test_data, "Elsevier", rules_else, ddv, array_sep)
        print("Ejemplos maligno")
        print(len(list_mal))
        pprint.pprint(list_mal)
        print("Ejemplos benigno")
        pprint.pprint(list_beg)
        print(len(list_beg))
        #print("Acierto/ NC/ Fallo")
        #print(percent_else)

        #for x in tuple_list_else:
        #    print(x)

        print("Reglas elsevier")
        pprint.pprint(rules_else)

        avg_amp.append(percent)
        avg_else.append(percent_else)

    average_mean = calculate_average(avg_amp)
    average_mean_else = calculate_average(avg_else)

    print("Media AMP:" +str(average_mean))
    print("Media Else: " +str(average_mean_else))
    
main()
