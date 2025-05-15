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

    # 3. Análisis Univariado
    # ----------------------
    print("\n\n3. ANÁLISIS UNIVARIADO")
    print("-" * 50)

    # 3.1 Variables Categóricas
    print("\n3.1 ANÁLISIS DE VARIABLES CATEGÓRICAS")

    # País
    print("\nDistribución por país:")
    country_counts = df_analysis['Country'].value_counts()
    print(country_counts.head(10))
    print(f"Número total de países: {len(country_counts)}")

    plt.figure(figsize=(14, 8))
    country_plot = country_counts.head(10).plot(kind='bar')
    plt.title('Top 10 Países por Número de Transacciones')
    plt.xlabel('País')
    plt.ylabel('Número de Transacciones')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./imagenes/top_10_paises.png')

    # StockCode
    print("\nProductos más comunes:")
    stock_counts = df_analysis['StockCode'].value_counts()
    print(stock_counts.head(10))

    # 3.2 Variables Numéricas
    print("\n3.2 ANÁLISIS DE VARIABLES NUMÉRICAS")

    # Quantity
    print("\nEstadísticas de Quantity:")
    print(df_analysis['Quantity'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['Quantity'].clip(0, 50), bins=50, kde=True)
    plt.title('Distribución de Cantidad (limitado a 50)')
    plt.xlabel('Cantidad')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['Quantity'].clip(0, 50))
    plt.title('Boxplot de Cantidad (limitado a 50)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_cantidad.png')

    # UnitPrice
    print("\nEstadísticas de UnitPrice:")
    print(df_analysis['UnitPrice'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['UnitPrice'].clip(0, 100), bins=50, kde=True)
    plt.title('Distribución de Precio Unitario (limitado a 100)')
    plt.xlabel('Precio Unitario')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['UnitPrice'].clip(0, 100))
    plt.title('Boxplot de Precio Unitario (limitado a 100)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_precio.png')

    # TotalAmount
    print("\nEstadísticas de TotalAmount:")
    print(df_analysis['TotalAmount'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['TotalAmount'].clip(0, 500), bins=50, kde=True)
    plt.title('Distribución de Monto Total (limitado a 500)')
    plt.xlabel('Monto Total')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['TotalAmount'].clip(0, 500))
    plt.title('Boxplot de Monto Total (limitado a 500)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_monto_total.png')

    # 3.3 Variables Temporales
    print("\n3.3 ANÁLISIS DE VARIABLES TEMPORALES")

    # Ventas por mes
    monthly_sales = df_analysis.groupby('Month')['TotalAmount'].sum().reindex(range(1, 13))
    print("\nVentas totales por mes:")
    print(monthly_sales)

    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind='bar')
    plt.title('Ventas Totales por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Ventas Totales')
    plt.xticks(range(12), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_mes.png')

    # Ventas por día de la semana
    weekday_sales = df_analysis.groupby('DayOfWeek')['TotalAmount'].sum()
    print("\nVentas totales por día de la semana:")
    print(weekday_sales)

    plt.figure(figsize=(12, 6))
    weekday_sales.plot(kind='bar')
    plt.title('Ventas Totales por Día de la Semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Ventas Totales')
    plt.xticks(range(7), ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_dia_semana.png')

    # Ventas por hora
    hourly_sales = df_analysis.groupby('Hour')['TotalAmount'].sum()
    print("\nVentas totales por hora del día:")
    print(hourly_sales)

    plt.figure(figsize=(12, 6))
    hourly_sales.plot(kind='bar')
    plt.title('Ventas Totales por Hora del Día')
    plt.xlabel('Hora')
    plt.ylabel('Ventas Totales')
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_hora.png')

    # 3. Análisis Univariado
    # ----------------------
    print("\n\n3. ANÁLISIS UNIVARIADO")
    print("-" * 50)

    # 3.1 Variables Categóricas
    print("\n3.1 ANÁLISIS DE VARIABLES CATEGÓRICAS")

    # País
    print("\nDistribución por país:")
    country_counts = df_analysis['Country'].value_counts()
    print(country_counts.head(10))
    print(f"Número total de países: {len(country_counts)}")

    plt.figure(figsize=(14, 8))
    country_plot = country_counts.head(10).plot(kind='bar')
    plt.title('Top 10 Países por Número de Transacciones')
    plt.xlabel('País')
    plt.ylabel('Número de Transacciones')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./imagenes/top_10_paises.png')

    # StockCode
    print("\nProductos más comunes:")
    stock_counts = df_analysis['StockCode'].value_counts()
    print(stock_counts.head(10))

    # 3.2 Variables Numéricas
    print("\n3.2 ANÁLISIS DE VARIABLES NUMÉRICAS")

    # Quantity
    print("\nEstadísticas de Quantity:")
    print(df_analysis['Quantity'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['Quantity'].clip(0, 50), bins=50, kde=True)
    plt.title('Distribución de Cantidad (limitado a 50)')
    plt.xlabel('Cantidad')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['Quantity'].clip(0, 50))
    plt.title('Boxplot de Cantidad (limitado a 50)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_cantidad.png')

    # UnitPrice
    print("\nEstadísticas de UnitPrice:")
    print(df_analysis['UnitPrice'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['UnitPrice'].clip(0, 100), bins=50, kde=True)
    plt.title('Distribución de Precio Unitario (limitado a 100)')
    plt.xlabel('Precio Unitario')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['UnitPrice'].clip(0, 100))
    plt.title('Boxplot de Precio Unitario (limitado a 100)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_precio.png')

    # TotalAmount
    print("\nEstadísticas de TotalAmount:")
    print(df_analysis['TotalAmount'].describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(df_analysis['TotalAmount'].clip(0, 500), bins=50, kde=True)
    plt.title('Distribución de Monto Total (limitado a 500)')
    plt.xlabel('Monto Total')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=df_analysis['TotalAmount'].clip(0, 500))
    plt.title('Boxplot de Monto Total (limitado a 500)')
    plt.tight_layout()
    plt.savefig('./imagenes/distribucion_monto_total.png')

    # 3.3 Variables Temporales
    print("\n3.3 ANÁLISIS DE VARIABLES TEMPORALES")

    # Ventas por mes
    monthly_sales = df_analysis.groupby('Month')['TotalAmount'].sum().reindex(range(1, 13))
    print("\nVentas totales por mes:")
    print(monthly_sales)

    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind='bar')
    plt.title('Ventas Totales por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Ventas Totales')
    plt.xticks(range(12), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_mes.png')

    # Ventas por día de la semana
    weekday_sales = df_analysis.groupby('DayOfWeek')['TotalAmount'].sum()
    print("\nVentas totales por día de la semana:")
    print(weekday_sales)

    plt.figure(figsize=(12, 6))
    weekday_sales.plot(kind='bar')
    plt.title('Ventas Totales por Día de la Semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Ventas Totales')
    plt.xticks(range(7), ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'])
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_dia_semana.png')

    # Ventas por hora
    hourly_sales = df_analysis.groupby('Hour')['TotalAmount'].sum()
    print("\nVentas totales por hora del día:")
    print(hourly_sales)

    plt.figure(figsize=(12, 6))
    hourly_sales.plot(kind='bar')
    plt.title('Ventas Totales por Hora del Día')
    plt.xlabel('Hora')
    plt.ylabel('Ventas Totales')
    plt.tight_layout()
    plt.savefig('./imagenes/ventas_por_hora.png')

    # 4. Análisis Bivariado
    # ---------------------
    print("\n\n4. ANÁLISIS BIVARIADO")
    print("-" * 50)

    # 4.1 Relación entre País y Ventas
    country_sales = df_analysis.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False)
    print("\n4.1 Top 10 países por ventas totales:")
    print(country_sales.head(10))

    plt.figure(figsize=(14, 8))
    country_sales.head(10).plot(kind='bar')
    plt.title('Top 10 Países por Ventas Totales')
    plt.xlabel('País')
    plt.ylabel('Ventas Totales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./imagenes/top_10_paises_ventas.png')

    # 4.2 Relación entre Mes y Cantidad vendida
    monthly_quantity = df_analysis.groupby('Month')['Quantity'].sum().reindex(range(1, 13))
    print("\n4.2 Cantidad total vendida por mes:")
    print(monthly_quantity)

    plt.figure(figsize=(12, 6))
    monthly_quantity.plot(kind='line', marker='o')
    plt.title('Cantidad Total Vendida por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad Total')
    plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./imagenes/cantidad_por_mes.png')

    # 4.3 Heatmap de correlación
    print("\n4.3 Matriz de correlación entre variables numéricas:")
    numeric_cols = ['Quantity', 'UnitPrice', 'TotalAmount', 'Year', 'Month', 'Day', 'DayOfWeek', 'Hour']
    correlation = df_analysis[numeric_cols].corr()
    print(correlation)

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlación')
    plt.tight_layout()
    plt.savefig('./imagenes/matriz_correlacion.png')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/