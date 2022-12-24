from functions import *
from fuzzyfy import *
from amplify_algorithm import *
from datetime import datetime

import json
import time

PATH = '../files/'


def calculate_activation_amplified(element, index, label_list, ddv):

    activation_mem = []

    if label_list != 0:
        for label in label_list:
            access_key = "x"+str(index)
            dict_access = ddv[access_key]
            calculate_list = dict_access[label]
            activation_mem.append(go_membership_function(element, calculate_list))

        #Seguir trabajando con activation_mem
    else:
        activation_mem.append(1)

    counter = 0
    for x in activation_mem:
        if x > 0:
            counter += 1

    return 1 if counter == 2 else max(activation_mem)

def calculate_activation(x, index, label, ddv):
    if label != 0:
        access_key = "x"+str(index)
        dict_access = ddv[access_key]
        calculate_list = dict_access[label]

        return go_membership_function(x, calculate_list)
    else:
        return None    
            
            
def shot_rules(example, rules, dict_a):

    cas_t = []
    for rule in range(0, len(rules)):
        cas = []
        rule_element = rules[rule][0]

        for element in range(0, len(example)):
            cas.append(calculate_activation(example[element], element, rule_element[element], dict_a))
        list_c = entry_none_vals(cas)
        minm = min(list_c)
        cas_t.append(minm)

    pos = [(x, cas_t[x]) for x in range(0, len(cas_t))]
    list_rules = [(rules[x[0]], x[1]) for x in pos]
    list_rules.sort(key = lambda x: x[1], reverse=True)
    list_element_rules = return_list_tuples(list_rules, 1)
    pos_max = list_element_rules.index(max(list_element_rules))
    return list_rules[pos_max]

def shot_amplified_rule(example, rules, ddv):

    cas_t = []
    #Cada regla sera una lista de listas
    for r in range(0, len(rules)):
        cas = []
        rule_element = rules[r][0]
        for element in range(0, len(example)):
            cas.append(calculate_activation_amplified(example[element], element, rule_element[element], ddv))
        minm = min(cas)
        cas_t.append(minm)

    pos = [(x, cas_t[x]) for x in range(0, len(cas_t))]
    list_rules = [(rules[x[0]], x[1]) for x in pos]
    list_rules.sort(key = lambda x: x[1], reverse=True)
    list_element_rules = return_list_tuples(list_rules, 1)
    pos_max = list_element_rules.index(max(list_element_rules))
    return list_rules[pos_max]


def calculate_shot(example, algorithm, rules, ddv):
    
    if algorithm == "amplify":
        return shot_amplified_rule(example, rules, ddv)
    elif algorithm == "elsevier":
        return shot_rules(example, rules, ddv)
    

def determine_shot_rules(example, algorithm, rules, ddv):
    compare_list = []
    compare_list.append(calculate_shot(example, algorithm, rules, ddv))
    #Hay que devolver la regla que mayor activacion tenga, ademas hay que devolverla de la siguiente forma:
    # Regla, activacion, clase a la que pertenece
    #Obtenemos lista de activaciones
    list_element_rules = return_list_tuples(compare_list, 1)
    pos_max = list_element_rules.index(max(list_element_rules))
    return compare_list[pos_max]


def ejecutar_clasificacion(data_tests, algorithm, rules, ddv, labels, labels_dct):
    tuple_list = []
    fail = 0
    counter = 0
    elements_no_classified = 0
    #first_element = ('Ejemplo', 'Ejemplo fuzzy', 'Nº Regla', 'Activacion', 'Clase ejemplo', 'Prediccion', 'Resultado')
    data_test_fuzzy = fuzzyfy_test(data_tests, ddv, labels)
    dict_rules = create_dict_rules(rules)
    #tuple_list.append(first_element)
    

    for n in range(0, len(data_tests)):
        example = data_tests[n]
    
        max_rule = determine_shot_rules(example[0], algorithm, rules, ddv)

        rule_class_name = max_rule[0][2]
        #Comprobar que efectivamente la activacion es > 0
        if max_rule[1] > 0:
            
            key = get_keys_with_value(dict_rules, max_rule[0])
            
            if check_accuracy(rule_class_name, example[1]) == 1:
                acc = "Acierto"
            elif check_accuracy(rule_class_name, example[1]) == 0:
                acc = "Fallo"
                fail +=1
            tuple_element = (example[0], data_test_fuzzy[n], key, max_rule[1], example[1], rule_class_name, acc)
            counter += check_accuracy(rule_class_name, example[1])
            tuple_list.append(tuple_element)
        else:
            key = "-"
            elements_no_classified += 1
            rule_class_name = "-"
            acc = "No clasificado"
            act = "-"
            tuple_element = (example[0], data_test_fuzzy[n], key, act, example[1], rule_class_name, acc)
            tuple_list.append(tuple_element)

    accuracy = round(counter / len(data_tests) * 100, 1)
    no_classified = round(elements_no_classified / len(data_tests) *100, 1)
    fail_per = round(fail / len(data_tests) * 100, 1)
    percents = [accuracy, no_classified, fail_per]
    return percents, tuple_list, dict_rules
  

def classify(json_object, data, filename_json, author, algorithm):
    inicio = time.time()
    date = datetime.now()
    path_json = PATH + filename_json + '_' + algorithm +'.json'
    division = [json_object["train"], json_object["test"]]
    ddv = json_object["ddv_d"]
    vars = json_object["vars"]
    vars.pop(-1)
    n_vars = len(vars)
    labels_dct = json_object["labels_dct"]
    class_names = json_object["class_names"]
    labels = json_object["labels"]

    avg = []
    ej_list = []
    len_total = []
    tuple_list = []
    dict_list = []

    
    for ej in range(1, json_object["execs"]+1):
        rules = []
        len_iter = []
        rls, data_tests = fuzzyfy(data, division, ddv, labels, n_vars, class_names, algorithm)
        rules = list(itertools.chain(*rls))
        len_iter = calc_len_rules(rules, class_names)
        average_amp, tuple_list_amp, dict_rules_amp = ejecutar_clasificacion(data_tests, algorithm, rules, ddv, labels, labels_dct)
        
        dict_list.append(dict_rules_amp)
        avg.append(average_amp)
        tuple_list.append(tuple_list_amp)
        len_total.append(len_iter)
        ej_list.append(ej)

    average_mean = calculate_average(avg)

    n_examples = len(data)
    n_examples_train = n_examples - len(data_tests)
    n_examples_test = n_examples - n_examples_train
    
    fin = time.time()
    tiempo = round(fin-inicio,1)

    final_dict = {}
  

    for ej in range(0, len(ej_list)):
        dict_class_name = {}
        avg_n = avg[ej]
        for class_n in range(0, len(class_names)):
            counter = 0
            counter_test = 0
            tuple_class = {}
            dict_rules = {}
            class_name = class_names[class_n]
            dict_class_name["class_name_"+str(class_n)] = class_name
            element = dict_list[ej]
            for key, rule in element.items():
                if rule[2] == class_name:
                    counter += 1
                    rule_to = readable_rule(rule)
                    dict_rules[key] = rule_to
            ne_tuple_list = tuple_list[ej]
            for el in range(0, len(ne_tuple_list)):
                
                if ne_tuple_list[el][-3] == class_name:
                    tuple_class["P"+str(el)] = str(ne_tuple_list[el])
                    counter_test += 1
        
            dict_class_name["n_rules_"+str(class_n)] = counter
            dict_class_name["rules_"+str(class_n)] = dict_rules
            dict_class_name["n_tests_"+str(class_n)] = counter_test
            dict_class_name["tests_"+str(class_n)] = tuple_class

        dict_class_name["accuracy"] = str(avg_n[0])   
        dict_class_name["no_classified"] = str(avg_n[1])
        dict_class_name["fail"] = str(avg_n[2])
        final_dict["it_"+str(ej)]=dict_class_name
    #if flag == 1:
    #    final_dict["ddv"] = ddv 
    final_dict["total_examples"] = n_examples
    final_dict["vars"] = vars
    final_dict["labels"] = labels
    final_dict["number_labels"] = len(labels)
    final_dict["target_var"] = json_object["target_var"]
    final_dict["number_vars"] = n_vars
    final_dict["n_examples_train"] = n_examples_train
    final_dict["n_examples_test"] = n_examples_test
    final_dict["avg_acc"] = average_mean[0]
    final_dict["avg_no_class"] = average_mean[1]
    final_dict["avg_fail"] = average_mean[2]
    final_dict["time"] = tiempo
    final_dict["n_executions"] = json_object["execs"]
    final_dict["date"] = str(date)
    final_dict["algorithm"] = algorithm
    final_dict["author"] = author
    with open(path_json, 'w') as fp:
        json.dump(final_dict, fp, indent=4)
    #print(final_dict)
  
    print("Ejecutado correctamente!")
    print("Resultado en ->" + path_json)