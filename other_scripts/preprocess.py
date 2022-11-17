from functions import load_data
import pandas as pd
def divide_in_classes(df):
    size = df.shape[1]

    fail_class = []
    pass_class = []
    notable_class = []

    

    for i, row in df.iterrows():
        
        
        if row[-1] <= 4:
            #fail_class.append([list_el[:len(list_el)-1], list_el[size-1]])
            df.at[i, 'quality2'] = "fail"
        elif row[-1] > 4 and row[-1] <= 6:
            #pass_class.append([list_el[:len(list_el)-1], list_el[size-1]])
            df.at[i, 'quality2'] = "pass"
        elif row[-1] > 6:
            df.at[i, 'quality2'] = "notable"
            #notable_class.append([list_el[:len(list_el)-1], list_el[size-1]])
    return df

WINE = '../files/wine.csv'
WINE_CONFIG = '../files/config_wine.json'
df = pd.read_csv(WINE, sep=";")
json_object, data = load_data(df, WINE_CONFIG)

df = divide_in_classes(df)
print(df.head())

df.to_csv("../files/new_wine.csv", index=False)
