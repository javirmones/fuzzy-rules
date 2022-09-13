from functions import *
from elsevier_algorithm import *
from amplify_algorithm import *
from pandas.core.common import flatten

#TODO

def calc_new_rules(data, ddv, labels):
    #El nuevo data sera un vector de la siguiente forma [[c1], [c2], [c3].... [cn]]
    #Dado un vector de esta forma x = [[x1, x2, x3, ... xn], class_name]
    #Convertir en regla
    element_lst = []
    for data_class in data:
        lst_el = []
        lst_tmp = []
        fuzzy_list = []
        test_list = []
        test = {}
        tuple_list = []

        for element in range(0, len(data_class)):
            fuzzyfied_el = fuzzyfy_data(data_class[element], ddv, labels)
            fuzzy_list.append(fuzzyfied_el)

        for j in range(0, len(fuzzy_list)):
            test_list.append(count_elements(fuzzy_list[j][0], fuzzy_list, fuzzy_list[j][1]))

        for x in test_list:
            if x not in test:
                test[x[0]] = (x[1],x[2])
        
        for k, val in test.items():
            tuple_list.append((k, val[0], val[1]))
        
        tuple_list.sort(key = lambda x: x[1], reverse=True)
        lst_tmp = [[list(tuple_list[x][0]), tuple_list[x][1], tuple_list[x][2]] for x in range(0, len(tuple_list))]
        lst_el = return_list(lst_tmp)
        element_lst.append(lst_el)
    
    return element_lst


def divide_classes_general(data_train, class_names):
    array_general_classes = []
    for class_obj in class_names:
        array_class_obj = []
        for x in range(0, len(data_train)):
            if data_train[x][2] == class_obj:
                array_class_obj.append(data_train[x])
        array_general_classes.append(array_class_obj)
    
    return array_class_obj
        
    
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


def fuzzyfy_data(element, ddv, labels, str_el):

    elem = element[0]
    tags_lst = []
    for x in range(0, len(elem)):
        #Recorrer el elemento
        access_key = str_el+str(x)
        tag = calc_tags(elem[x], access_key, ddv, labels)
        tags_lst.append(tag)
    
    return [tags_lst, element[1]]

def fuzzy_single(list, ddv, index, labels, str_el):
    tags_lst = []
    for x in range(0, len(list)):
        #Recorrer el elemento
        access_key = str_el+str(index)
        tag = calc_tags(list[x], access_key, ddv, labels)
        tags_lst.append(tag)
    
    return tags_lst


def fuzzyfy(data, division, ddv, labels, n_vars, class_names, option):
    
    general_classes_array = []
    data_train = []
    
    general_data_train = []
    general_data_test = []
    if option == 1:
    
        general_data_train, general_data_test = divide_train_test_general(data, division[0], division[1])
        
        general_data_train = divide_classes_general(general_data_train, class_names)
        
        print(general_data_train)
        
    elif option == 2:
        general_classes_array = divide_classes_general(data_train, class_names)
        general_data_train, general_data_test = divide_train_test_general(general_classes_array, division[0], division[1])
        data_tests = list(flatten(general_data_test))
    
    for class_data in data:
    
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
