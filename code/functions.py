import random

def create_dict_rules(rules):
    dict_rules = {}
    for x in range(0, len(rules)):
        key = "R"+str(x)
        element = rules[x]
        dict_rules[key] = element
    return dict_rules

def check_anexes(labels_list, label_to_check):
    test = []
    for x in range(0, len(label_to_check)):
        if x == len(label_to_check)-1:
            test.append(0)
            break
        test.append(check_elements(label_to_check[x], label_to_check[x+1], labels_list))
    return test

def check_elements(tag_a, tag_b, labels_list):
    for x in range(0, len(labels_list)):
        if tag_a == labels_list[x]:
            if labels_list[x+1] == tag_b:
                return 1
            else:
                return 0

def check_accuracy(rule_class_name, example_classname):
    return 1 if rule_class_name == example_classname else 0

def entry_none_vals(list):
    return [x for x in list if x != None]

def calculate_mean(lst):
    return sum(lst)/len(lst)

def calculate_average(list_avg):
    acc = []
    nc = []
    fail = []
    for i in range(0, len(list_avg)):
        element = list_avg[i]
        acc.append(element[0])
        nc.append(element[1])
        fail.append(element[2])
    mean_acc = round(calculate_mean(acc),1)
    mean_nc = round(calculate_mean(nc),1)
    mean_fail = round(calculate_mean(fail),1)
    return [mean_acc, mean_nc, mean_fail]

def return_list_tuples(list, index):
    return [x[index] for x in list]

def element_function(x_element, index, ddv, labels):
    list_labels = []
    for k, val in ddv.items():
        list_labels.append(go_membership_function(x_element, val[index]))

    index = list_labels.index(max(list_labels))
    return labels[index]

def return_label_element(element, ddv, labels):
    return [element_function(x, element.index(x), ddv, labels) for x in element]

def go_membership_function(x, elements):
    return membership_function(x, elements[0], elements[1], elements[2], elements[3])

def create_label_order(labels):
    ordered_label_set = {}
    for tag in range(0, len(labels)):
        ordered_label_set[labels[tag]] = tag 
    return ordered_label_set

def reestructure_rules(rules, labels):
    
    new_list = []
    for el in range(0, len(rules)):
        new_rule = []
        element = rules[el][0]
        for y in element:
            if y == labels:
                new_rule.append(0)
            else:
                new_rule.append(y)
        new_rule = [new_rule, rules[el][1], rules[el][2]]
        new_list.append(new_rule)
    return new_list

def return_pos_element(element, list_items):
    list_r = []
    for x in range(0, len(list_items)):
        if compare_items(element, list_items[x]) == 1:
            list_r.append(1)
        else:
            list_r.append(0)
    return list_r

def count_elements(element, list_items):
    counter = 0
    list_occ_element = return_pos_element(element, list_items)
    for j in range(0, len(list_occ_element)):
        if list_occ_element[j] == 1:
            counter += 1
    return (tuple(element), counter) 
    
def count_elements(element, list_items, number_class_items):
    counter = 0
    
    list_items = return_list(list_items)
    list_occ_element = return_pos_element(element, list_items)

    for j in range(0, len(list_occ_element)):
        if list_occ_element[j] == 1:
            counter += 1
    return (tuple(element), counter, number_class_items) 

def compare_items(element_1, element_2):
    lista_check = []
    for val_a, val_b in zip(element_1, element_2):
        if val_a == val_b:
            lista_check.append(True)
        elif val_a != val_b:    
            lista_check.append(False)
    return 1 if all(lista_check) else 0

def return_list(element):
    return [element[x][0] for x in range(0,len(element))]

def return_index(element):
    return [[element[x][0], element[x][2]] for x in range(0,len(element))]


def get_keys_with_value(dic, value):
    key = [key for key, val in dic.items() if val == value]
    return key[0]

def divide_train_test(data, train_set, test_set):
    sample = random.sample(range(0, len(data)), len(data))
    
    data_l = []
    for x in range(0, len(data)):
        data_l.insert(sample[x], data[x])
    
    number_of_elements_train = int(round(len(data_l) * train_set, 0))
    train_sample = data_l[:number_of_elements_train]
    test_sample = data_l[number_of_elements_train:]
    return train_sample, test_sample if train_set + test_set == 1 else print("Error en los porcentajes")

def bi_function(u, alpha, beta):
    if u < alpha:
        return 1
    elif alpha <= u and u <= beta:
        return round((beta - u)/(beta - alpha),1)
    elif u > beta:
        return 0

def trapezoidal_function(u, alpha, beta, gamma):
    if u < alpha:
        return 0
    elif alpha <= u and u <= beta:
        return round((u - alpha)/(beta - alpha), 1)
    elif beta <= u and u <= gamma:
        return round((gamma - u)/(gamma - beta), 1)
    elif u > gamma:
        return 0
    
def membership_function(x, a, b, c, d):
    if x < a:
        return 0
    elif a <= x and x < b :
        return round((x - a)/(b - a), 1)
    elif b <= x and x <= c:
        return 1
    elif c < x and x <= d:
        return round((d - x)/(d - c), 1)
    elif x > d:
        return 0

def escribir_archivo(data, string, path):
    with open(path, 'w+') as f:
        f.seek(0)
        f.write("\t\t---Resultados---"+"\n")
        f.write("Para "+string+ " hay un total de " +str(len(data)) +"\n")
        f.write("Etiquetas \t\t\t\t Ocurrencias\n")
        for item in data:
            f.write(str(item[0])+": \t\t"+str(item[1])+"\n")
