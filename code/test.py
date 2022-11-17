import pandas as pd

from functions import load_data, divide_in_segments
from classifier import classify
FILE_CONFIG = '../files/config.json'
WINE_CONFIG = '../files/config_wine.json'
DATA = '../files/iris.csv'
WINE = '../files/new_wine.csv'
OUTPUT_JSON = 'output'

algorithm = ["amplify", "elsevier"]
author = ["Castro, Castro-schez, zurita", "Albusac, Monescillo"]

exit_var = False
option = 0
# Fuzzyfy process - we read the file with the main config
print("Ejecutando fuzzy-rules")

df = pd.read_csv(WINE, sep=",")
json_object, data = load_data(df, WINE_CONFIG)
ddv_d = json_object["ddv_d"]
flag = 0
if not ddv_d:
    print("Dominio de definicion de variable no encontrado")
    print("Creando uno nuevo a partir de los datos")
    new_ddv_d = divide_in_segments(df, json_object["labels"])
    json_object["ddv_d"] = new_ddv_d
classify(json_object, data, OUTPUT_JSON, author[0], algorithm[0], 1)
