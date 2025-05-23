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

    # 5. Análisis de Clientes
    # -----------------------
    print("\n\n5. ANÁLISIS DE CLIENTES")
    print("-" * 50)

    # Solo analizamos clientes con CustomerID válido
    df_customers = df_analysis.dropna(subset=['CustomerID'])
    df_customers['CustomerID'] = df_customers['CustomerID'].astype(int)

    # 5.1 Número de transacciones por cliente
    customer_transactions = df_customers.groupby('CustomerID')['InvoiceNo'].nunique()
    print("\n5.1 Estadísticas de transacciones por cliente:")
    print(customer_transactions.describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(customer_transactions.clip(0, 50), bins=50, kde=True)
    plt.title('Distribución de Transacciones por Cliente')
    plt.xlabel('Número de Transacciones')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=customer_transactions.clip(0, 50))
    plt.title('Boxplot de Transacciones por Cliente')
    plt.tight_layout()
    plt.savefig('./imagenes/transacciones_por_cliente.png')

    # 5.2 Total gastado por cliente
    customer_spending = df_customers.groupby('CustomerID')['TotalAmount'].sum()
    print("\n5.2 Estadísticas de gasto total por cliente:")
    print(customer_spending.describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(customer_spending.clip(0, 10000), bins=50, kde=True)
    plt.title('Distribución de Gasto Total por Cliente')
    plt.xlabel('Gasto Total')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=customer_spending.clip(0, 10000))
    plt.title('Boxplot de Gasto Total por Cliente')
    plt.tight_layout()
    plt.savefig('./imagenes/gasto_por_cliente.png')

    # 5.3 RFM (Recency, Frequency, Monetary) Analysis
    # Determinamos la fecha más reciente en el dataset
    max_date = df_customers['InvoiceDate'].max()

    # Para cada cliente calculamos:
    # - Recency: días desde la última compra
    # - Frequency: número de transacciones
    # - Monetary: gasto total

    rfm = df_customers.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (max_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',  # Frequency
        'TotalAmount': 'sum'  # Monetary
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalAmount': 'Monetary'
    })

    print("\n5.3 Análisis RFM - Primeros 10 clientes:")
    print(rfm.head(10))

    # Visualizar distribución de RFM
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    sns.histplot(rfm['Recency'].clip(0, 365), bins=50, kde=True)
    plt.title('Distribución de Recency (días)')
    plt.xlabel('Días desde última compra')

    plt.subplot(1, 3, 2)
    sns.histplot(rfm['Frequency'].clip(0, 100), bins=50, kde=True)
    plt.title('Distribución de Frequency')
    plt.xlabel('Número de Transacciones')

    plt.subplot(1, 3, 3)
    sns.histplot(rfm['Monetary'].clip(0, 10000), bins=50, kde=True)
    plt.title('Distribución de Monetary')
    plt.xlabel('Gasto Total')

    plt.tight_layout()
    plt.savefig('./imagenes/analisis_rfm.png')

    # 6. Análisis de Productos
    # ------------------------
    print("\n\n6. ANÁLISIS DE PRODUCTOS")
    print("-" * 50)

    # 6.1 Productos más vendidos por cantidad
    top_products_quantity = df_analysis.groupby(['StockCode', 'Description'])['Quantity'].sum().sort_values(
        ascending=False)
    print("\n6.1 Top 10 productos más vendidos por cantidad:")
    print(top_products_quantity.head(10))

    # 6.2 Productos más vendidos por ingresos totales
    top_products_revenue = df_analysis.groupby(['StockCode', 'Description'])['TotalAmount'].sum().sort_values(
        ascending=False)
    print("\n6.2 Top 10 productos más vendidos por ingresos:")
    print(top_products_revenue.head(10))

    # Visualizar top productos por ingresos
    plt.figure(figsize=(14, 8))
    top_products_revenue.head(10).plot(kind='bar')
    plt.title('Top 10 Productos por Ingresos Totales')
    plt.xlabel('(StockCode, Descripción)')
    plt.ylabel('Ingresos Totales')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('./imagenes/top_10_productos_ingresos.png')

    # 7. Análisis de Patrones de Compra
    # ---------------------------------
    print("\n\n7. ANÁLISIS DE PATRONES DE COMPRA")
    print("-" * 50)

    # 7.1 Tamaño promedio de la orden (items por factura)
    order_size = df_analysis.groupby('InvoiceNo')['Quantity'].sum()
    print("\n7.1 Estadísticas de tamaño de orden (items por factura):")
    print(order_size.describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(order_size.clip(0, 100), bins=50, kde=True)
    plt.title('Distribución de Tamaño de Orden')
    plt.xlabel('Cantidad de Items')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=order_size.clip(0, 100))
    plt.title('Boxplot de Tamaño de Orden')
    plt.tight_layout()
    plt.savefig('./imagenes/tamaño_orden.png')

    # 7.2 Valor promedio de la orden
    order_value = df_analysis.groupby('InvoiceNo')['TotalAmount'].sum()
    print("\n7.2 Estadísticas de valor de orden:")
    print(order_value.describe())

    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(order_value.clip(0, 1000), bins=50, kde=True)
    plt.title('Distribución de Valor de Orden')
    plt.xlabel('Valor Total')

    plt.subplot(1, 2, 2)
    sns.boxplot(y=order_value.clip(0, 1000))
    plt.title('Boxplot de Valor de Orden')
    plt.tight_layout()
    plt.savefig('./imagenes/valor_orden.png')

    # 8. Series temporales y análisis de tendencias
    # --------------------------------------------
    print("\n\n8. ANÁLISIS DE SERIES TEMPORALES")
    print("-" * 50)

    # Agrupamos por fecha completa
    df_analysis['Date'] = df_analysis['InvoiceDate'].dt.date
    daily_sales = df_analysis.groupby('Date')['TotalAmount'].sum()

    print("\n8.1 Estadísticas de ventas diarias:")
    print(daily_sales.describe())

    # Gráfico de serie temporal
    plt.figure(figsize=(16, 8))
    daily_sales.plot(kind='line')
    plt.title('Ventas Diarias a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Ventas Totales')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('./imagenes/serie_temporal_ventas.png')

    # 9. Segmentación de Clientes
    # --------------------------
    print("\n\n9. SEGMENTACIÓN DE CLIENTES")
    print("-" * 50)

    # Creamos segmentos basados en RFM
    # Dividimos cada métrica RFM en 5 segmentos
    rfm['R_Segment'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1],
                               duplicates='drop')  # 5 es lo mejor (compra reciente)

    # Para frequency, manejamos los duplicados con 'drop' o usamos rangos manuales si es necesario
    try:
        rfm['F_Segment'] = pd.qcut(rfm['Frequency'].clip(1, 200), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    except ValueError:
        # Alternativa: crear bins manualmente basados en los percentiles
        freq_bins = [0, 1, 2, 4, 10, float('inf')]
        rfm['F_Segment'] = pd.cut(rfm['Frequency'].clip(1, 200), bins=freq_bins, labels=[1, 2, 3, 4, 5], right=True,
                                  include_lowest=True)

    rfm['M_Segment'] = pd.qcut(rfm['Monetary'].clip(0, 50000), 5, labels=[1, 2, 3, 4, 5],
                               duplicates='drop')  # 5 es lo mejor (alto valor)

    # Calculamos RFM Score
    rfm['RFM_Score'] = rfm['R_Segment'].astype(int) + rfm['F_Segment'].astype(int) + rfm['M_Segment'].astype(int)

    # Creamos categorías de clientes
    def categorize_customer(rfm_score):
        if rfm_score >= 13:
            return 'Champions'
        elif 10 <= rfm_score < 13:
            return 'Loyal Customers'
        elif 7 <= rfm_score < 10:
            return 'Potential Loyalists'
        elif 5 <= rfm_score < 7:
            return 'At Risk Customers'
        else:
            return 'Need Attention'

    rfm['Customer_Category'] = rfm['RFM_Score'].apply(categorize_customer)

    # Contamos clientes por categoría
    customer_categories = rfm['Customer_Category'].value_counts()
    print("\n9.1 Segmentación de clientes por categoría RFM:")
    print(customer_categories)

    # Visualizamos la segmentación
    plt.figure(figsize=(12, 8))
    customer_categories.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribución de Segmentos de Clientes')
    plt.ylabel('')  # Quitamos la etiqueta del eje y
    plt.tight_layout()
    plt.savefig('./imagenes/segmentacion_clientes.png')

    # 10. Conclusiones
    # ---------------
    print("\n\n10. CONCLUSIONES DEL ANÁLISIS EXPLORATORIO")
    print("-" * 50)

    print("""
    Conclusiones principales del análisis exploratorio de datos:

    1. Perfil de Datos:
       - El dataset contiene información de transacciones minoristas en línea con 8 variables principales.
       - Hay un porcentaje significativo de valores faltantes en CustomerID ({}%).
       - Se identificaron transacciones de cancelación y valores negativos que fueron tratados en la limpieza.

    2. Perfil de Ventas:
       - Reino Unido es el país dominante en términos de transacciones y ventas totales.
       - Existe una clara estacionalidad con picos de ventas en ciertos meses (particularmente hacia fin de año).
       - Los días de semana muestran mayor actividad de ventas que los fines de semana.
       - Las horas con mayor actividad de ventas son durante la mañana y media tarde.

    3. Perfil de Clientes:
       - La distribución de compras por cliente es altamente sesgada, con pocos clientes generando la mayoría de ingresos.
       - La segmentación RFM permitió identificar distintos grupos de clientes según su comportamiento de compra.
       - Aproximadamente {}% de los clientes son de alta valor (Champions y Loyal Customers).

    4. Perfil de Productos:
       - Existe un grupo pequeño de productos que generan la mayor parte de los ingresos.
       - Los productos más vendidos por cantidad no siempre coinciden con los más rentables.

    5. Patrones de Compra:
       - El tamaño promedio de orden es de aproximadamente {} items.
       - El valor promedio de orden es de aproximadamente £{:.2f}.
       - Hay una tendencia general {} en las ventas a lo largo del período analizado.

    6. Recomendaciones:
       - Mejorar la captura de datos de CustomerID para reducir valores faltantes.
       - Implementar estrategias de marketing específicas para los distintos segmentos de clientes.
       - Optimizar inventario priorizando productos de alta rotación y rentabilidad.
       - Considerar promociones especiales en períodos de menor actividad para equilibrar ventas.
    """.format(
        df['CustomerID'].isnull().mean() * 100,
        len(rfm[rfm['RFM_Score'] >= 10]) / len(rfm) * 100,
        order_size.mean(),
        order_value.mean(),
        "creciente" if (daily_sales.iloc[-20:].mean() > daily_sales.iloc[:20].mean()) else "decreciente"
    ))

    print("\nAnálisis Exploratorio de Datos completado!")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/