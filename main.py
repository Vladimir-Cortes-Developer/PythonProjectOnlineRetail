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

    # 2. Limpieza de datos
    # -------------------
    print("\n\n2. LIMPIEZA DE DATOS")
    print("-" * 50)

    # Hacemos una copia para no modificar los datos originales
    df_clean = df.copy()

    # Eliminamos filas con valores nulos en Description
    df_clean = df_clean.dropna(subset=['Description'])

    # Filtrar valores negativos en Quantity (posibles devoluciones)
    print(f"Registros con cantidad negativa (posibles devoluciones): {(df_clean['Quantity'] < 0).sum()}")

    # Filtramos facturas de cancelación (comienzan con C)
    print(f"Facturas de cancelación: {df_clean['InvoiceNo'].astype(str).str.startswith('C').sum()}")

    # Creamos un dataframe de trabajo para análisis (eliminar cancelaciones y cantidades negativas)
    df_analysis = df_clean[(~df_clean['InvoiceNo'].astype(str).str.startswith('C')) &
                           (df_clean['Quantity'] > 0) &
                           (df_clean['UnitPrice'] > 0)]

    print(f"Dimensiones después de la limpieza: {df_analysis.shape[0]} filas y {df_analysis.shape[1]} columnas")

    # Convertimos la fecha a datetime si no lo está
    if not pd.api.types.is_datetime64_any_dtype(df_analysis['InvoiceDate']):
        df_analysis['InvoiceDate'] = pd.to_datetime(df_analysis['InvoiceDate'])

    # Extraemos componentes de la fecha
    df_analysis['Year'] = df_analysis['InvoiceDate'].dt.year
    df_analysis['Month'] = df_analysis['InvoiceDate'].dt.month
    df_analysis['Day'] = df_analysis['InvoiceDate'].dt.day
    df_analysis['DayOfWeek'] = df_analysis['InvoiceDate'].dt.dayofweek
    df_analysis['Hour'] = df_analysis['InvoiceDate'].dt.hour

    # Calculamos el valor total de cada transacción
    df_analysis['TotalAmount'] = df_analysis['Quantity'] * df_analysis['UnitPrice']



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/