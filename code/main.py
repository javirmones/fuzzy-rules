from os import mkdir, stat
from classifier import *
from functions import ask_option, load_data, divide_in_segments
import pandas as pd


FILE_CONFIG = '../files/config.json'
WINE_CONFIG = '../files/config_wine.json'
IRIS = '../files/iris.csv'
WINE = '../files/new_wine.csv'
OUTPUT_JSON = 'output'

labels = ""
train_set = None
test_set = None


def main():
    algorithm = ["amplify", "elsevier"]
    author = ["Castro, Castro-schez, zurita", "Albusac, Castro, Monescillo"]
    
    exit_var = False
    option = 0
    # Fuzzyfy process - we read the file with the main config
    print("Ejecutando fuzzy-rules")
    df = pd.read_csv(WINE, sep=',')
    json_object, data = load_data(df, WINE_CONFIG)
    ddv_d = json_object["ddv_d"]

    if not ddv_d:
        print("Dominio de definicion de variable no encontrado")
        print("Creando uno nuevo a partir de los datos")
        new_ddv_d = divide_in_segments(df, json_object["labels"])
        json_object["ddv_d"] = new_ddv_d

    while not exit_var:
        print("1. Ejecutar ambos algoritmos")
        print("2. Ejecutar algoritmo amplificación (", author[0], ")")
        print("3. Ejecutar algoritmo nuevo (", author[1],")")
        print("4. Salir")
        option = ask_option()
        if option == 1:
            classify(json_object, data, OUTPUT_JSON, author[0], algorithm[0])
            classify(json_object, data, OUTPUT_JSON, author[1], algorithm[1])
        elif option == 2:
            classify(json_object, data, OUTPUT_JSON, author[0], algorithm[0])
        elif option == 3: 
            classify(json_object, data, OUTPUT_JSON, author[1], algorithm[1])
        elif option == 4:
            exit_var = True

        else:
            print("Introduce un numero entre 1 y 4")


#    si indicas vacio ddv -> crear automaticamente
if __name__=="__main__":
    
    main()