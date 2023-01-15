from functions import *
from elsevier_algorithm import *
from amplify_algorithm import *


def calc_new_rules(data, ddv):
    #El nuevo data sera un vector de la siguiente forma [[c1], [c2], [c3].... [cn]]
    #Dado un vector de esta forma x = [[x1, x2, x3, ... xn], class_name]
    #Convertir en regla
    
    lst_el = []
    lst_tmp = []
    fuzzy_list = []
    test_list = []
    test = {}
    tuple_list = []

    for single_element in data:
        #Cambiar funcion fuzzyfy_data
        fuzzyfied_el = fuzzyfy_data(single_element, ddv)
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
    return lst_el

  
def fuzzyfy_test(data_test, ddv):
    fuzzy_list = []
    for element in range(0, len(data_test)):
        fuzzyfied_el = fuzzyfy_data(data_test[element], ddv)
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


def fuzzyfy_data(element, ddv):
    elem = element[0]
    tags_lst = []
    for x in range(0, len(elem)):
        #Recorrer el elemento
        access_key = "x"+str(x)
        # Calc tags
        labels = list(ddv[access_key].keys())     
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


def fuzzyfy(data, division, ddv, n_vars, class_names, algorithm):
    general_classes_array = []
    data_test = []
    general_data_test = []
    rule_set = []
    rules = []

    #dict_labels = create_label_order(labels)

    general_classes_array = divide_classes_general(data, class_names)
    general_data_train, general_data_test = divide_train_test_general(general_classes_array, division[0], division[1])
    

    for x in general_data_test:
        for y in x:
            data_test.append(y)

    for data in general_data_train:
        list_class_rules = calc_new_rules(data, ddv)
        rule_set.append(list_class_rules)
    
    if algorithm == 'amplify':
        for x in range(0, len(class_names)):
            rule_check = give_list_of_list(rule_set, x)
            rls = amplify_algorithm(rule_set[x], rule_check, ddv, class_names[x])
            rls_res = reestructure_rules(rls, ddv)
            rules.append(rls_res)

    elif algorithm == 'elsevier':
        for x in range(0, len(class_names)):
            rule_check = give_list_of_list(rule_set, x)
            regs_else = elsevier_algorithm(rule_set[x], rule_check, n_vars, class_names[x])
            rules.append(regs_else)
    
    return rules, data_test
