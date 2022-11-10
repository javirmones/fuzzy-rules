from os import mkdir, stat
from classifier import *
from pdf_generator import *
from functions import ask_option, load_data

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


def main():
    global pdf_mode, inference
    try:
        stat(BASE_DIR)
    except FileNotFoundError as e:
        mkdir(BASE_DIR)
    # Fuzzyfy process - we read the file with the main config
    df = pd.read_csv(PATH_DATA)
    json_object, data = load_data(df, PATH_CONFIG)
    
    algorithm = ["Amplify", "Elsevier"]
    author = ["Castro, Castro-schez, zurita", "Monescillo and company"]
    path_pdf = PATH_PDF    

    exit_var = False
    option = 0

    while not exit_var:
        print("1. Ejecutar con distribucion similar")
        print("2. Menu de PDFs")
        print("3. Salir")
        option = ask_option()
        if option == 1:
            classify(json_object, data, path_pdf, author, pdf_mode, algorithm)
        elif option == 2:
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

        elif option == 3:
            exit_var = True

        else:
            print("Introduce un numero entre 1 y 3")



if __name__=="__main__":
    
    main()