from os import mkdir, stat
from classifier import *
from pdf_generator import *
from functions import *

import pandas as pd
import json


BASE_DIR = './files/'
DIR_AMP = 'amp/'
DIR_ELSEVIER = 'elsevier/'
FILE_CONFIG = 'config.json'
NAME_PDF = 'final_report.pdf'
NAME_PDF_E = 'elsevier.pdf'
DATA = 'iris.csv'


PATH_ELSEVIER = BASE_DIR + DIR_ELSEVIER
PATH_AMP = BASE_DIR + DIR_AMP

PATH_CONFIG = BASE_DIR + FILE_CONFIG
PATH_DATA = BASE_DIR + DATA
PATH_PDF = BASE_DIR + NAME_PDF
PATH_PDF_ELSE = BASE_DIR + NAME_PDF_E

labels = ""
train_set = None
test_set = None
pdf_mode = 1
inference = 0


def ask_option():
 
    correcto = False
    num = 0
    while(not correcto):
        try:
            num = int(input("Introduce un numero entero: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
     
    return num

def main():
    try:
        stat(BASE_DIR)
    except FileNotFoundError as e:
        mkdir(BASE_DIR)
    # Fuzzyfy process - we read the file with the main config
    df = pd.read_csv(PATH_DATA)
    execut, n_vars, ddv, labels, data, division, class_names = load_data(df)
    global pdf_mode, inference
    algorithm = ["Amplify", "Elsevier"]
    author = ["Castro, Castro-schez, zurita", "author2"]
    path_pdf = PATH_PDF    

    exit_var = False
    option = 0

    while not exit_var:
        print("1. Ejecutar con distribucion aleatoria")
        print("2. Ejecutar con distribucion similar")
        print("3. Menu de PDFs")
        print("4. Inferencia")
        print("5. Salir")
        option = ask_option()
    
        if option == 1:

            classify(execut, class_names, algorithm, data, labels, n_vars, division, ddv, path_pdf, author, option, pdf_mode)
        elif option == 2:
           
            classify(execut, class_names, algorithm, data, labels, n_vars, division, ddv, path_pdf, author, option, pdf_mode)
        elif option == 3:
            
            exit_men = False
            while not exit_men:
                print("Seleccione el modo de crear el PDF")
                print("1. Algoritmos en el mismo PDF (Por defecto)")
                print("2. Algoritmo Amplify")
                print("3. Algoritmo Elsevier")
                print("4. Salir")
                option_men = ask_option()
                if option_men == 1:
                    exit_men = True
                elif option_men == 2:
                    pdf_mode = 2
                    exit_men = True
                elif option_men == 3:
                    pdf_mode = 3
                    exit_men = True
                elif option_men == 4:
                    exit_men = True
                else:
                    print("Introduce un numero entre 1 y 4")
        elif option == 4:
            exit_mem = False
            while not exit_mem:
                print("Seleccione el modo de inferencia")
                print("1. Inferencia sin anexos")
                print("2. Inferencia con anexos")
                print("3. Salir")
                option_men = ask_option()
                if option_men == 1:
                    inference = 0
                    exit_mem = True
                elif option_men == 2:
                    inference = 1
                    exit_mem = True
                elif option_men == 3:
                    exit_mem = True
                else:
                    print("Introduce un numero entre 1 y 3")
        elif option == 5:
            exit_var = True

        else:
            print("Introduce un numero entre 1 y 5")



if __name__=="__main__":
    
    main()