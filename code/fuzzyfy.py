from functions import *
from elsevier_algorithm import *
from amplify_algorithm import *


def calc_new_rules(data, ddv, labels):

    #Dado un vector de esta forma x = [[x1, x2, x3, ... xn], class_name]
    #Convertir en regla
    fuzzy_list = []
    test_list = []
    test = {}
    tuple_list = []

    for element in range(0, len(data)):
        fuzzyfied_el = fuzzyfy_data(data[element], ddv, labels)
        fuzzy_list.append(fuzzyfied_el)

    for j in range(0, len(fuzzy_list)):
        test_list.append(count_elements(fuzzy_list[j][0], fuzzy_list, fuzzy_list[j][1]))

    for x in test_list:
        if x not in test:
            test[x[0]] = (x[1],x[2])
    
    for k, val in test.items():
        tuple_list.append((k, val[0], val[1]))
    
    tuple_list.sort(key = lambda x: x[1], reverse=True)

    return [[list(tuple_list[x][0]), tuple_list[x][1], tuple_list[x][2]] for x in range(0, len(tuple_list))]


def divide_classes(data_train):
    setosa = []
    versicolor = []
    virginica = []
    print(data_train)
    for x in range(0, len(data_train)):
        if data_train[x][1] == 'Setosa':
            setosa.append(data_train[x])
        elif data_train[x][1] == 'Versicolor':
            versicolor.append(data_train[x])
        elif data_train[x][1] == 'Virginica':
            virginica.append(data_train[x])
    return setosa, versicolor, virginica

def divide_classes_new(data_train):
    setosa = []
    versicolor = []
    virginica = []
    print(data_train)
    for x in range(0, len(data_train)):
        if data_train[x][2] == 'Setosa':
            setosa.append(data_train[x])
        elif data_train[x][2] == 'Versicolor':
            versicolor.append(data_train[x])
        elif data_train[x][2] == 'Virginica':
            virginica.append(data_train[x])
    return setosa, versicolor, virginica


def fuzzyfy_test(data_test, ddv, labels):
    fuzzy_list = []
    for element in range(0, len(data_test)):
        fuzzyfied_el = fuzzyfy_data(data_test[element], ddv, labels)
        fuzzy_list.append(fuzzyfied_el)
    return return_list(fuzzy_list)
 
def calc_tags(num_el, key, ddv, labels):
    #primero obtener el diccionario para recorrerlo
    list_of_vals = []
    dict_re = ddv[key]

    for k, val in dict_re.items():
        list_of_vals.append(go_membership_function(num_el, val))
    #Devuelvo la etiqueta con mayor valor calculado
    index = list_of_vals.index(max(list_of_vals))
    return labels[index]   


def fuzzyfy_data(element, ddv, labels):

    elem = element[0]
    tags_lst = []
    for x in range(0, len(elem)):
        #Recorrer el elemento
        access_key = "x"+str(x)
        tag = calc_tags(elem[x], access_key, ddv, labels)
        tags_lst.append(tag)
    
    return [tags_lst, element[1]]

def fuzzy_single(list, ddv, index, labels):
    tags_lst = []
    for x in range(0, len(list)):
        #Recorrer el elemento
        access_key = "x"+str(index)
        tag = calc_tags(list[x], access_key, ddv, labels)
        tags_lst.append(tag)
    
    return tags_lst



def fuzzyfy(data, division, ddv, labels, n_vars, class_names, option):
    if option == 1:
    
        data_train, data_tests = divide_train_test(data, division[0], division[1])
        
        setosa_data, versi_data, virgi_data = divide_classes(data_train)
        print(setosa_data)
    elif option == 2:
        s_data, v_data, vir_data = divide_classes(data)
        setosa_data, test_setosa = divide_train_test(s_data, division[0], division[1])
        versi_data, test_versi = divide_train_test(v_data, division[0], division[1])
        virgi_data, test_virgi = divide_train_test(vir_data, division[0], division[1])
        data_tests = test_setosa + test_versi + test_virgi
    
    list_setosa = return_list(calc_new_rules(setosa_data, ddv, labels))
    lista_versi  = return_list(calc_new_rules(versi_data, ddv, labels))
    lista_virginica = return_list(calc_new_rules(virgi_data, ddv, labels))

    rule_check_versi_virgi = lista_versi + lista_virginica
    rule_check_setosa_virgi = list_setosa + lista_virginica
    rule_check_versi_setosa = list_setosa + lista_versi
    dict_labels = create_label_order(labels)
    
    reglas_setosa_amp = amplify_algorithm(list_setosa, rule_check_versi_virgi, labels, dict_labels, class_names[0])
    reglas_versi_amp = amplify_algorithm(lista_versi, rule_check_setosa_virgi , labels, dict_labels, class_names[1])
    reglas_virginica_amp = amplify_algorithm(lista_virginica, rule_check_versi_setosa, labels, dict_labels, class_names[2])

    regs_amp = reestructure_rules(reglas_setosa_amp, labels)
    regv_amp = reestructure_rules(reglas_versi_amp, labels)
    regvi_amp = reestructure_rules(reglas_virginica_amp, labels)

    reglas_setosa = elsevier_algorithm(list_setosa, rule_check_versi_virgi, n_vars, class_names[0])
    reglas_versi = elsevier_algorithm(lista_versi, rule_check_setosa_virgi, n_vars, class_names[1])
    reglas_virgi = elsevier_algorithm(lista_virginica, rule_check_versi_setosa, n_vars, class_names[2])


    elsevier_rules = reglas_setosa + reglas_versi + reglas_virgi
    amp_rules = regs_amp + regv_amp + regvi_amp


    return amp_rules, elsevier_rules, data_tests
