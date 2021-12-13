#libreria para representar graficamente los datos
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
from functions import membership_function
from functions import go_membership_function

def exploratory_data_analysis(df):
    sns.set_style('darkgrid')
    print(df['target'].value_counts())
    plt.figure(figsize=(8, 6))
    sns.countplot(df['target'])
    plt.xlabel("Diagnosis")
    plt.title("Count Plot of Diagnosis")   
    plt.show()


def violin_plot(features, name, df_scaled_melt):
    """
    This function creates violin plots of features given in the argument.
    """
    # Create query
    query = ''
    for x in features:
        query += "features == '" + str(x) + "' or "
    query = query[0:-4]

    # Create data for visualization
    data = df_scaled_melt.query(query)

    # Plot figure
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='features',
                   y='value',
                   hue='target',
                   data=data,
                   split=True,
                   inner="quart")
    plt.xticks(rotation=45)
    plt.title(name)
    plt.xlabel("Features")
    plt.ylabel("Standardize Value")
    plt.show()

def swarm_plot(features, name, df_scaled_melt):
    """
    This function creates swarm plots of features given in the argument.
    """
    # Create query
    query = ''
    for x in features:
        query += "features == '" + str(x) + "' or "
    query = query[0:-4]

    # Create data for visualization
    data = df_scaled_melt.query(query)

    # Plot figure
    plt.figure(figsize=(12, 6))
    sns.swarmplot(x='features', y='value', hue='target', data=data)
    plt.xticks(rotation=45)
    plt.title(name)
    plt.xlabel("Features")
    plt.ylabel("Standardize Value")
    plt.show()


def box_plot(features, name, df_scaled_melt):
    """
    This function creates box plots of features given in the argument.
    """
    # Create query
    query = ''
    for x in features:
        query += "features == '" + str(x) + "' or "
    query = query[0:-4]

    # Create data for visualization
    data = df_scaled_melt.query(query)

    # Plot figure
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='features', y='value', hue='target', data=data)
    plt.xticks(rotation=45)
    plt.title(name)
    plt.xlabel("Features")
    plt.ylabel("Standardize Value")
    plt.show()

def correlation(var, df):
    """
    1. Print correlation
    2. Create jointplot
    """
    # Print correlation
    print("Correlation: ", df[[var[0], var[1]]].corr().iloc[1, 0])

    # Create jointplot
    plt.figure(figsize=(6, 6))
    sns.jointplot(df[(var[0])], df[(var[1])], kind='reg')
    plt.show()

def correlation_matrix(df):
    # Create correlation matrix
    corr_mat = df.corr()

    # Create mask
    mask = np.zeros_like(corr_mat, dtype=np.bool)
    mask[np.triu_indices_from(mask, k=1)] = True

    # Plot heatmap
    plt.figure(figsize=(15, 10))
    sns.heatmap(corr_mat, annot=True, fmt='.1f',
                cmap='RdBu_r', vmin=-1, vmax=1,
                mask=mask)
    plt.show()
    plt.figure(figsize=(15, 10))
    sns.heatmap(corr_mat[corr_mat > 0.8], annot=True,
                fmt='.1f', cmap=sns.cubehelix_palette(200), mask=mask)
    plt.show()

    #exploratory_data_analysis(df)
    #df_scaled = dist_features(df, df_features)
    #violin_plot(df.columns[0:10], "Violin Plot of the First 10 Features", df_scaled)
    #swarm_plot(df.columns[10:20], "Swarm Plot of the Next 10 Features", df_scaled)
    #box_plot(df.columns[20:30], "Box Plot of the Last 10 Features", df_scaled)
    #correlation(['mean perimeter', 'mean area'], df)
    #correlation(['mean concavity', 'mean concave points'], df)
    #correlation(['worst symmetry', 'worst fractal dimension'], df) 
    #correlation_matrix(df)

def calculate_imgs(ddv_dict_item):
    img_val = []
    
    for x in range(0,len(ddv_dict_item)):
        element = ddv_dict_item[x]
        img_val.append(go_membership_function(element, ddv_dict_item))

    return img_val

def plot_ddv(ddv_dict, var):

    #x = [2, 2, 2.3, 2.6]
    #y = [1, 1, 1, 0]
    colors = ['b', 'g', 'r', 'c', 'm', 'y','b','r','k']
    values = []
    i = 0

    

    fig= plt.figure(figsize=(7,7))
    fig.tight_layout()
    ticks = range(0,4)
    for key, valor in ddv_dict.items():
        y = calculate_imgs(valor)
        plt.plot(valor, y, colors[i], label=key)
        i+=1
    
    legend = plt.legend(loc="upper right", shadow=True, fontsize=14)
    plt.xlabel(var)
    legend.get_frame().set_facecolor('white')
    
    plt.yticks(ticks)
    plt.grid()
    plt.show()