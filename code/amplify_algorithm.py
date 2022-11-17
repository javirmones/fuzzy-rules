from functions import *

#DONE

def get_keys_with_value(dic, value):
    key = [key for key, val in dic.items() if val == value]
    return key[0]

def ordered_tags(dic, list_to_check) -> list:
    #Primero convertir la lista de etiquetas en numeros en funcion del diccionario
    numbers_to_order = []
    final_list = []
    for x in range(0, len(list_to_check)):
        tag = list_to_check[x]
        number = dic[tag]
        numbers_to_order.append(number)

    #Ya tienes la lista de numeros 
    #Ahora aplicarle un sort
    numbers_to_order = sorted(numbers_to_order)
    #Re construimos la lista

    for y in range(0, len(numbers_to_order)):
        number = numbers_to_order[y]
        key = get_keys_with_value(dic, number)
        final_list.append(key)

    return final_list

def comprobar_ampliacion(original_rule, rule_set_to_check):
    #Creamos una copia de la regla original
    #Quitamos el elemento que estamos tratando en cuestion
    boolean = True
    total_check = []

    for x in range(0, len(rule_set_to_check)):
        check = []
        for v1, v2 in zip(original_rule, rule_set_to_check[x]):
            if v2 in v1:
                check.append(1)
            else:
                check.append(0)
        total_check.append(check)

    for x in total_check:
        if all(x) == 1:
            boolean = False
    #comprobar que para la lista de reglas existe efectivamente
    return boolean

def compare_items(element_1, element_2):
    lista_check = []
    for val_a, val_b in zip(element_1, element_2):
        if val_a == val_b:
            lista_check.append(True)
        elif val_a != val_b:    
            lista_check.append(False)
    return 1 if all(lista_check) else 0


def is_on_amplified_rule(new_rule, amplified_rule):
    check_rule = []
    for v1, v2 in zip(amplified_rule[0], new_rule):
        if v2 in v1:
            check_rule.append(True)
        else:
            check_rule.append(False)
    
    return True if all(check_rule) else False

def set_increment(amr):
    amr[1] += 1

def is_included(rule, amplified_rules):
    boolean = False
    for amr in amplified_rules:
        if is_on_amplified_rule(rule, amr):
            set_increment(amr)
            boolean = True
    return boolean

def amplify(rule_to_amplify, rule_set_to_check, labels, dict_labels, class_name):
    #La primera regla sera de la forma ['A', 'B', 'C', 'D']
    # Hay que intentar amplificarla por ello 
    # Para cada uno de los elemento 
    # Rule_set_to_check tiene que ser una lista de listas
    # con los contraejemplos
    # Comprobar que en primer lugar la regla no es un contrajemplo
    rule_to_amp = rule_to_amplify.copy()
    # y también que no está incluida
    nueva_regla = []
    for i in range(0, len(rule_to_amp)):
        sub_regla = []
        if len(sub_regla) == 0:
            sub_regla.append(rule_to_amp[i])
        for j in range(0, len(labels)):
            nueva_etiqueta = labels[j]

            if nueva_etiqueta not in sub_regla:
                sub_regla.append(nueva_etiqueta)
                rule_to_amp.pop(i)
                rule_to_amp.insert(i, sub_regla)

                if not comprobar_ampliacion(rule_to_amp, rule_set_to_check):
                    sub_regla.pop()
 
        sub_regla = ordered_tags(dict_labels, sub_regla)
        nueva_regla.append(sub_regla)
        nueva_tupla = [nueva_regla, 1, class_name]
    return nueva_tupla

def amplify_algorithm(rules_to_amplify, rule_set_to_check, labels, dict_labels, class_name):
    # Primer paso amplificar la primera regla
    amplified_rules = []
    rules_t = rules_to_amplify.copy()
    for x in range(0, len(rules_t)):
        if not is_included(rules_to_amplify[x], amplified_rules):
            regla_ampliada = amplify(rules_to_amplify[x], rule_set_to_check, labels, dict_labels, class_name)
            amplified_rules.append(regla_ampliada)
    
    return amplified_rules

