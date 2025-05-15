# Análisis Exploratorio de Datos: Online Retail

## Bootcamp en Inteligencia artificial (Talento Tech)
## Nivel: Explorador - Básico-2025-5-L2-G47
## Realizado por:  Víctor C. Vladimir Cortés A.

Este proyecto realiza un análisis exploratorio de datos completo de un conjunto de datos de ventas minoristas en línea. El análisis incluye limpieza de datos, visualizaciones, análisis estadístico y segmentación de clientes mediante la técnica RFM (Recency, Frequency, Monetary).

## Contenido del Repositorio

- `main.py`: Script principal de Python que contiene todo el análisis
- `Online Retail.xlsx`: Conjunto de datos original
- `README.md`: Descripción del proyecto (este archivo)
- Imágenes generadas durante el análisis:
  - Distribuciones
  - Series temporales
  - Segmentación de clientes
  - Correlaciones
  - Y más...

## Conjunto de Datos

El conjunto de datos contiene transacciones de un minorista en línea con sede en el Reino Unido. Cada registro representa una venta de un producto específico e incluye:

- **InvoiceNo**: Número de factura (único para cada transacción)
- **StockCode**: Código del producto 
- **Description**: Descripción del producto
- **Quantity**: Cantidad de productos vendidos
- **InvoiceDate**: Fecha y hora de la transacción
- **UnitPrice**: Precio unitario del producto
- **CustomerID**: Identificador único del cliente
- **Country**: País donde se realizó la venta

## Estructura del Análisis

El análisis está estructurado en las siguientes secciones:

1. **Carga y Vista Previa de Datos**
   - Dimensiones del dataset
   - Información de las columnas
   - Estadísticas descriptivas
   - Valores nulos

2. **Limpieza de Datos**
   - Eliminación de valores nulos
   - Filtrado de facturas de cancelación
   - Filtrado de cantidades negativas
   - Extracción de componentes temporales
   - Cálculo del monto total

3. **Análisis Univariado**
   - Variables categóricas (País, StockCode)
   - Variables numéricas (Quantity, UnitPrice, TotalAmount)
   - Variables temporales (Mes, Día de la semana, Hora)

4. **Análisis Bivariado**
   - Relación entre País y Ventas
   - Relación entre Mes y Cantidad
   - Correlaciones entre variables

5. **Análisis de Clientes**
   - Transacciones por cliente
   - Gasto total por cliente
   - Análisis RFM (Recency, Frequency, Monetary)

6. **Análisis de Productos**
   - Productos más vendidos por cantidad
   - Productos más vendidos por ingresos

7. **Análisis de Patrones de Compra**
   - Tamaño promedio de la orden
   - Valor promedio de la orden

8. **Series Temporales y Análisis de Tendencias**
   - Ventas diarias
   - Tendencias y estacionalidad

9. **Segmentación de Clientes**
   - Segmentación basada en RFM
   - Categorización de clientes

10. **Conclusiones**
    - Hallazgos principales
    - Recomendaciones

## Requisitos

Para ejecutar este análisis, se requieren las siguientes bibliotecas de Python:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
```

## Cómo Ejecutar

1. Asegúrate de tener Python instalado (3.7+)
2. Instala las dependencias: `pip install pandas numpy matplotlib seaborn`
3. Coloca el archivo `Online Retail.xlsx` en el mismo directorio que el script
4. Ejecuta el script: `python main.py`

## Resultados Principales

### Perfil de Datos
- El dataset contiene información de transacciones minoristas en línea con 8 variables principales.
- Hay un porcentaje significativo de valores faltantes en CustomerID.
- Se identificaron transacciones de cancelación y valores negativos que fueron tratados en la limpieza.

### Perfil de Ventas
- Reino Unido es el país dominante en términos de transacciones y ventas totales.
- Existe una clara estacionalidad con picos de ventas en ciertos meses (particularmente hacia fin de año).
- Los días de semana muestran mayor actividad de ventas que los fines de semana.
- Las horas con mayor actividad de ventas son durante la mañana y media tarde.

### Perfil de Clientes
- La distribución de compras por cliente es altamente sesgada, con pocos clientes generando la mayoría de ingresos.
- La segmentación RFM permitió identificar distintos grupos de clientes según su comportamiento de compra.
- Se identificaron cinco segmentos de clientes: Champions, Loyal Customers, Potential Loyalists, At Risk Customers y Need Attention.

### Perfil de Productos
- Existe un grupo pequeño de productos que generan la mayor parte de los ingresos.
- Los productos más vendidos por cantidad no siempre coinciden con los más rentables.

## Solución al Error de Segmentación RFM

Si encuentras un error al ejecutar la segmentación de clientes debido a valores duplicados en los bordes de los bins (`ValueError: Bin edges must be unique`), la solución implementada es:

1. Agregar el parámetro `duplicates='drop'` a las llamadas `pd.qcut()`
2. En caso de persistir el error, usar un enfoque alternativo con bins personalizados:

```python
# Para frequency, manejamos los duplicados con 'drop' o usamos rangos manuales si es necesario
try:
    rfm['F_Segment'] = pd.qcut(rfm['Frequency'].clip(1, 200), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
except ValueError:
    # Alternativa: crear bins manualmente basados en los percentiles
    freq_bins = [0, 1, 2, 4, 10, float('inf')]
    rfm['F_Segment'] = pd.cut(rfm['Frequency'].clip(1, 200), bins=freq_bins, labels=[1, 2, 3, 4, 5], right=True, include_lowest=True)
```


## Licencia

Este proyecto está bajo la Licencia "Apache License 2.0".