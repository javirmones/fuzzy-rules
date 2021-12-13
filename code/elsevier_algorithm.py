import operator
from os import terminal_size
import uuid
from pandas.core.accessor import register_dataframe_accessor
from itertools import combinations
import pdb

def calculate_tags(rule) -> int:
    count = 0
    for x in range(0, len(rule)):
        if rule[x] != 0:
            count +=1
    return count
    

def comprobar_contraejemplo(rule, rules_check) -> (bool):
    #Devuelve true si hay contraejemplo
    boolean = False
    n_tags = calculate_tags(rule)
    for i in range(0, len(rules_check)):
        list_check = []
        counter = 0
        for val_a, val_b in zip(rule, rules_check[i]):
            if val_a == 0:
                list_check.append(False)
            elif val_a == val_b:
                list_check.append(True)
                counter +=1
            elif val_a != val_b:
                list_check.append(False)

        if counter == n_tags:
            boolean = True
            break
    return boolean



def eliminar_elemento(remove_examples, set_of_examples):
    examples_copy = set_of_examples.copy()

    for x in examples_copy:
        for y in remove_examples:
            if x == y:
                set_of_examples.remove(y)

    return set_of_examples

def comprobar_regla_igual(rule, conjunto):
    list_check = []

    for x in range(0, len(conjunto)):
        rule_def = conjunto[x][0]
        # primero comprobar si hay alguna igual

        if rule_def == rule:
            list_check.append(True)
        elif rule_def != rule:
            list_check.append(False)
    return True if any(list_check) else False

def remove_zeros(list_check):
    new_list = []
    for x in list_check:
        if x != 0:
            new_list.append(x)

    return new_list

def es_cubierta(regla_check, regla_set):
    array_check = []


    r1 = remove_zeros(regla_check)
    r2 = remove_zeros(regla_set)

    for x in r1:
        if x in r2:
            array_check.append(True)
        else:
           array_check.append(False) 

    return True if any(array_check) else False
    
   
def comprobar_regla_cubierta(rule, conjunto):
    check_list = []

    if len(conjunto) > 0:
        for x in range(0, len(conjunto)):
            
            rule_def = conjunto[x][0]
            check_list.append(es_cubierta(rule, rule_def))
 
        return True if any(check_list) else False
    else:
        return False

def pos_combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(i for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(i for i in indices)

def obtener_lista(set_tuples):
    return [list(set_tuples[x]) for x in range(0, len(set_tuples))]

def recompose_rule(rule_to_compose: list, pos: list, n_vars: int) -> list:
    rule = [0 for x in range(0, n_vars)]
    for v1, v2 in zip(rule_to_compose, pos):
        rule[v2] = v1
    return rule

def combo_vars(rule, comb) -> list: 
    combs = list(combinations(rule, comb))
    pos = list(pos_combinations(rule, comb))
    return combs, pos

def create_combo_vars(rules, iterador) -> (list):
    final_list = []

    for x in range(0, len(rules)):
        rule = rules[x]

        combos, pos = combo_vars(rule, iterador)
        combos = obtener_lista(combos)
        pos = obtener_lista(pos)

        for v1, v2 in zip(combos, pos):
            if v1 not in final_list:
                final_list.append(recompose_rule(v1, v2, len(rule)))

    return final_list

def create_combo_var(rule, iterador) -> (list):
    final_list = []
    combos, pos = combo_vars(rule, iterador)
    combos = obtener_lista(combos)
    pos = obtener_lista(pos)

    for v1, v2 in zip(combos, pos):
        if v1 not in final_list:
            final_list.append(recompose_rule(v1, v2, len(rule)))

    return final_list


def reglas_contraejemplo(candidates_rules, rules_check):
    reglas_sin_contraejemplo = []
    for x in range(0, len(candidates_rules)):
        regla_actual = candidates_rules[x]
        
        if not comprobar_contraejemplo(regla_actual, rules_check):
            reglas_sin_contraejemplo.append(regla_actual)
            break

    return reglas_sin_contraejemplo

def devolver_ejemplos(rule_c, set_of_examples):
    #Devuelve los ejemplos que se pueden eliminar dada una regla
    list_of_examples_to_remove = []
    n_tags = calculate_tags(rule_c)
    for i in range(0, len(set_of_examples)):
        example = set_of_examples[i]
        list_check = []
        counter = 0
        for val_a, val_b in zip(rule_c, example):
            if val_a == 0:
                list_check.append(False)
            elif val_a == val_b:
                list_check.append(True)
                counter +=1
            elif val_a != val_b:
                list_check.append(False)
        if counter == n_tags:
            list_of_examples_to_remove.append(example)

    return list_of_examples_to_remove

def elsevier_algorith_plus(rules, rules_check, n_vars, class_n, start):
    pass

def elsevier_algorithm(rules, rules_check, n_vars, class_n):
    set_of_examples = rules.copy()
    reglas_finales = []
    print(rules)
    for i in range(1, n_vars+1):

        for r in range(0, len(set_of_examples)):
            if len(set_of_examples) > 0:
                rule = rules[r]
                candidates_rules = []
                candidates_rules = create_combo_var(rule, i)
                reglas_sin_contraejemplo = reglas_contraejemplo(candidates_rules, rules_check)

                if len(reglas_sin_contraejemplo) > 0:

                    for x in range(0, len(reglas_sin_contraejemplo)):
                        regla_sin_cont = reglas_sin_contraejemplo[x]

                        if not comprobar_regla_igual(regla_sin_cont, reglas_finales) and not comprobar_regla_cubierta(regla_sin_cont, reglas_finales):
                            list_of_remove = devolver_ejemplos(regla_sin_cont, set_of_examples)
                            if len(list_of_remove) > 0:
                                set_of_examples = eliminar_elemento(list_of_remove, set_of_examples)
                                rule_deft = [regla_sin_cont, len(list_of_remove), class_n]
                                reglas_finales.append(rule_deft)
                    

                
    return reglas_finales

