# Análisis Exploratorio de Datos (EDA) - Online Retail
# ------------------------------------------------------

# Importamos las bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # Configuramos el estilo de las visualizaciones
    plt.style.use('ggplot')
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

    # 1. Carga de datos
    # -----------------
    print("1. CARGA Y VISTA PREVIA DE DATOS")
    print("-" * 50)

    # Cargamos el archivo Excel
    df = pd.read_excel('./dataset/Online_Retail.xlsx')

    # Mostramos información básica del dataset
    print(f"Dimensiones del dataset: {df.shape[0]} filas y {df.shape[1]} columnas")
    print("\nPrimeras 5 filas:")
    print(df.head())

    print("\nInformación de las columnas:")
    print(df.info())

    print("\nEstadísticas descriptivas:")
    print(df.describe())

    print("\nValores nulos por columna:")
    print(df.isnull().sum())
    print(f"Porcentaje de valores nulos en CustomerID: {df['CustomerID'].isnull().mean() * 100:.2f}%")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/