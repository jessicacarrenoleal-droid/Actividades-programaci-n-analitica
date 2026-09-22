#Ejercicios practica Pandas 1
import pandas as pd
import numpy as np
url = "https://raw.githubusercontent.com/plotly/datasets/master/supermarket_Sales.csv"
data = pd.read_csv(url)

data = data.rename(columns={'Tax 5%': 'Tax',
 'Cost of goods sold': 'Cogs',
 'Gross margin percentage': 'Gross margin pct',
 'Customer stratification rating': 'Rating'})
data.columns = (data.columns
 .str.strip()
 .str.lower()
 .str.replace(' ', '_'))

#A.Dimensiones del DataFrame
print(data.shape)   
# (filas, columnas)

# 2. Columnas, tipos y primeras filas 
print(data.columns)
print(data.dtypes)
data.head(3)

#3.Seleccionar varias columnas
resultado = data[["product_line", "quantity", "total"]]
resultado.head()
print(resultado)   

#4.¿Series o DataFrame?
print(type(data['total']))
print(type(data[['total']]))

#5.loc y iloc sobre la misma celda
print(data.loc[7, 'product_line'])
print(data.iloc[7, 5])

#6. Una sola condición
mascara = data['quantity'] >8
resultado = data[mascara]
print(resultado.shape[0])

# 7.Dos condiciones al tiempo
mascara = (data['branch'] == 'C' ) & (data['total'] > 300)
resultado = data[mascara]
print(resultado.shape)

# 8. Corregir un filtro por categorías 
# Instruccion incorrecta:
# mascara = data['product_line'] == 'Food and beverages'
# or 'Fashion accessories'
mascara = data['product_line'].isin(['Food and beverages', 'Fashion accessories'])
print(data[mascara].shape[0])

#9.Rango de valores y columnas elegidas 
mascara = (data['branch'].isin(['A', 'C'])) & (data['total'].between(200, 500))
resultado = data.loc[mascara, ['branch','product_line','quantity','total']]
resultado.head()
print(mascara)
print(resultado)

#10.Valor de cada unidad vendida 
data['valor_unitario'] = data['total'] / data['quantity']
print(data['valor_unitario'].head(3).round(2))

#11.Clasificar cada venta
data['tipo_compra'] = np.where(data['quantity'] >= 6, 'volumen', 'menor')
print(data['tipo_compra'].value_counts())

#12. ¿Cuánto ingreso genera cada sucursal?
resumen = (data
.groupby('branch')['total']
.sum())
print(resumen.round(2))

 #13.¿Cuántas facturas registra cada método de pago?
resumen = (data
.groupby('payment')['invoice_id']
.count())
print(resumen)

#14.Varias métricas por método de pago 
resumen = (
data
.groupby('payment')
.agg(facturas=('invoice_id', 'size'),
unidades=('quantity', 'sum'),
ingreso=('total', 'sum'),)
.reset_index())
print(resumen.round(2))
print(resumen.loc[resumen['ingreso'].idxmax()]) #mayor ingreso
print(resumen.loc[resumen['ingreso'].idxmax(), 'payment'])
print(resumen.sort_values('ingreso', ascending=False))


#15. Agregar la zona de cada sucursal 
sucursales = pd.DataFrame({
    'branch': ['A', 'B', 'C'],
    'zona': ['Centro', 'Norte', 'Sur']
})

resultado = data.merge(
    sucursales,
    on='branch',
    how='left')

print(resultado.shape)
resultado[['branch', 'city', 'zona', 'total']].head()