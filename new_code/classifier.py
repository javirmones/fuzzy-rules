from functions import *
from fuzzyfy import *
from amplify_algorithm import *
from pdf_generator import *
import time

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
    
    if algorithm == "Amplify":
        return shot_amplified_rule(example, rules, ddv)
    elif algorithm == "Elsevier":
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


def ejecutar_clasificacion(data_tests, algorithm, rules, ddv, labels):
    tuple_list = []
    fail = 0
    counter = 0
    elements_no_classified = 0
    first_element = ('Ejemplo', 'Ejemplo fuzzy', 'Nº Regla', 'Activacion', 'Clase ejemplo', 'Prediccion', 'Resultado')
    data_test_fuzzy = fuzzyfy_test(data_tests, ddv, labels)
    dict_rules = create_dict_rules(rules)
    tuple_list.append(first_element)
    

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
  

def classify(ex, class_names, algorithm, data, labels, n_vars, division, ddv, path, author, option, pdf_mode):
    inicio = time.time()
    avg_amp = []
    avg_else = []
    ej_list = []
    len_total_amp = []
    len_total_else = []
    dict_list = []
    dict_else = []
    tuple_list_amp_f = []
    tuple_list_els_f = []

    for ej in range(1, ex+1):

        ramp, relse, data_tests = fuzzyfy(data, division, ddv, labels, n_vars, class_names, option)
        ramp1, ramp2, ramp3 = divide_classes_new(ramp)
        relse1, relse2, relse3 = divide_classes_new(relse)
        average_amp, tuple_list_amp, dict_rules_amp = ejecutar_clasificacion(data_tests, algorithm[0], ramp, ddv, labels)
        average_else, tuple_list_els, dict_rules_els = ejecutar_clasificacion(data_tests, algorithm[1], relse, ddv, labels)

        dict_list.append(dict_rules_amp)
        dict_else.append(dict_rules_els)

        avg_amp.append(average_amp)
        avg_else.append(average_else)
        tuple_list_amp_f.append(tuple_list_amp)
        tuple_list_els_f.append(tuple_list_els)
        

        
        len_amp = [len(ramp1), len(ramp2), len(ramp3)]
        len_else = [len(relse1), len(relse2), len(relse3)]
        len_total_amp.append(len_amp)
        len_total_else.append(len_else)
        ej_list.append(ej)

    
       
    
    average_mean = calculate_average(avg_amp)
    average_mean_else = calculate_average(avg_else)
    n_examples = len(data)
    n_examples_train = n_examples - len(data_tests)
    n_examples_test = n_examples - n_examples_train
    examples_len = [n_examples, n_examples_train, n_examples_test]
    #rules = [ramp, relse]
    fin = time.time()
    tiempo = round(fin-inicio,1)

    if pdf_mode == 1:
        text_amp, data_amp = create_text(tiempo, avg_amp, average_mean, dict_list, class_names, ej_list, algorithm[0], division, len_total_amp, n_vars, examples_len, tuple_list_amp_f, author[0])
        text_else, data_else = create_text(tiempo, avg_else, average_mean_else, dict_else, class_names, ej_list, algorithm[1], division, len_total_else, n_vars, examples_len, tuple_list_els_f, author[1])

        data_final_table = []
        header = ['P', 'NRSe', 'NRVe', 'NRVi', 'Tot', 'Acc', 'NC', 'E', 'NRSe', 'NRVe', 'NRVi', 'Tot', 'Acc', 'NC', 'E']
        legend = "<b> P: </b> Prueba <br/>"
        legend += "<b> NRSe: </b> Numero de Reglas Setosa <br/>"
        legend += "<b> NRVe: </b> Numero de Reglas Versicolor <br/>"
        legend += "<b> NRSe: </b> Numero de Reglas Virginica <br/>"
        legend += "<b> Tot: </b> Total <br/>"
        legend += "<b> Acc: </b> Porcentaje de Acierto <br/>"
        legend += "<b> NC: </b> Porcentaje de No Clasificados  <br/>"
        legend += "<b> F: </b> Porcentaje de Fallo <br/>"

        data_final_table.append(header)
        for x in range(1, len(data_amp)):
            element_else = data_else[x]
            element_amp = data_amp[x]
            resultant_element = element_amp + element_else[1:]
            
            data_final_table.append(resultant_element)
        build_pdf(text_amp, data_amp, text_else, data_else, data_final_table, legend, path)
    elif pdf_mode == 2:
        text_amp, data_amp = create_text(tiempo, avg_amp, average_mean, dict_list, class_names, ej_list, algorithm[0], division, len_total_amp, n_vars, examples_len, tuple_list_amp_f, author[0])
        build_amp_pdf(text_amp, data_amp, path)
    elif pdf_mode == 3:
        text_else, data_else = create_text(tiempo, avg_else, average_mean_else, dict_else, class_names, ej_list, algorithm[1], division, len_total_else, n_vars, examples_len, tuple_list_els_f, author[1])
        build_els_pdf(text_else, data_else, path)