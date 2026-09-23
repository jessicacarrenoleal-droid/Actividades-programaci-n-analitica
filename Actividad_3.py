import numpy as np
import pandas as pd

url ='https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv'
dataini = pd.read_csv(url)
print(dataini.head())
print(dataini.shape)

data = dataini.copy()
data.shape

data.columns
data.dtypes
data.info()

print("Registros y variables:", dataini.shape)

variables = ['customerID', 'Contract', 'Churn', 'tenure', 'MonthlyCharges', 'PaymentMethod']
print("Variables usadas:", variables)
print(dataini[variables].dtypes)


tabla_resumen = (dataini.assign(cancelo=dataini['Churn'].eq('Yes'))   # bool True/False
    .groupby('Contract')
    .agg(clientes=('customerID', 'count'),
         pct_cancelacion=('cancelo', 'mean'),
         cargo_mensual_prom=('MonthlyCharges', 'mean'))
    .sort_values('pct_cancelacion', ascending=False))
tabla_resumen['pct_cancelacion'] = (tabla_resumen['pct_cancelacion'] * 100).round(2)
tabla_resumen['cargo_mensual_prom'] = tabla_resumen['cargo_mensual_prom'].round(2)
print(tabla_resumen)

mediana = dataini['MonthlyCharges'].median()   # mediana se calcula sore todo el conjunto no el subconjunto filtrado 70.35

prioritarios = dataini[(dataini['Churn'] == 'No') & (dataini['Contract'] == 'Month-to-month')
    & (dataini['tenure'] <= 12) & (dataini['MonthlyCharges'] > mediana)].copy()

print("Clientes en el grupo:", len(prioritarios))
print("Método de pago más frecuente:", prioritarios['PaymentMethod'].mode()[0])
print(prioritarios['PaymentMethod'].value_counts())
print("Cargo mensual promedio:", round(prioritarios['MonthlyCharges'].mean(), 2))


#1. ¿Qué tipo de contrato presenta el mayor porcentaje de cancelación?
# El contrato mes a mes presenta el mayor porcentanje de cancelacion (42.71%)
#2. ¿Qué diferencias relevantes observa en el cargo mensual promedio según el tipo de contrato?
#Es el contrato que mas clientes tienen pero con el promedio de cancelacion mas alto.
#3. ¿Cuántos clientes conforman el grupo definido para revisión prioritaria y cuál es el método de pago más frecuente?
#244 clientes  revision prioritaria  y el metodo de pago mas frecuente es el Electronic Check 158
#4. A partir de los resultados calculados, ¿qué aspecto debería revisar primero el área de retención?
#El area de retencion deberia revisar primero los clinetes con pago por cheque electronico ofreciendodes un contrato de mayor plazo.