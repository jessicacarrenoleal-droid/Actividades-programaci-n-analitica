# -*- coding: utf-8 -*-
"""Cápsula pandas 1: Un CSV, un KPI, una función.

Programación para Analítica de Datos 2026-2

Mientras llegan los datos propios del Restaurante La Analítica, la gerencia
practica con un conjunto público: 244 cuentas reales de un restaurante, con
el valor de la cuenta, la propina y el momento del día. La pregunta:

    ¿En qué momento del día se deja mejor propina?

La ruta de trabajo:
    leer un CSV desde una URL -> inspeccionar -> transformar -> KPI con una función

Requisitos: pip install pandas
Ejecución:  python Capsula_pandas_1.py
"""

import pandas as pd


# 1. Leer los datos desde una URL
# Una sola línea reemplaza todo el trabajo de escribir los datos a mano:
# read_csv() descarga el archivo y lo convierte en una tabla (DataFrame).

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"


df = pd.read_csv(URL)
print("Tabla cargada:", df.shape[0], "filas y", df.shape[1], "columnas")


# 2. Inspeccionar antes de analizar
# Nunca analice una tabla que no ha inspeccionado.

print("\nPrimeras filas:")
print(df.head().to_string())

print("\nTipos de dato por columna:")
print(df.dtypes)


# 3. Transformaciones básicas
# Los datos vienen en inglés. Tres transformaciones los dejan listos:
#   a) renombrar las columnas al español;
#   b) traducir los valores de la columna momento;
#   c) crear la columna del porcentaje de propina, que es la que responde
#      la pregunta. La división opera sobre las columnas completas, sin
#      ciclos ni acumuladores.

df = df.rename(columns={
    "total_bill": "cuenta",
    "tip": "propina",
    "sex": "sexo",
    "smoker": "fumador",
    "day": "dia",
    "time": "momento",
    "size": "personas",
})

df["momento"] = df["momento"].replace({"Lunch": "Almuerzo", "Dinner": "Cena"})

df["porcentaje_propina"] = df["propina"] / df["cuenta"] * 100

print("\nTabla transformada:")
print(df.head().to_string())


# 4. El KPI como una función simple
# Este es el puente con el tema central de la Sesión 7: el cálculo se
# escribe una vez, dentro de una función, y se reutiliza cuantas veces
# haga falta.

def propina_promedio(tabla):
    """KPI: porcentaje de propina promedio de la tabla, en %."""
    return round(tabla["porcentaje_propina"].mean(), 1)


print("\nKPI general:", propina_promedio(df), "%")


# 5. Reutilizar la función: la respuesta a la pregunta
# Una condición dentro de corchetes filtra filas (máscara booleana).
# La misma función, aplicada a cada subconjunto, responde la pregunta.

cenas = df[df["momento"] == "Cena"]
almuerzos = df[df["momento"] == "Almuerzo"]


print("\nPropina promedio en la cena:    ", propina_promedio(cenas), "%")
print("Propina promedio en el almuerzo:", propina_promedio(almuerzos), "%")

# Lectura del resultado: la intuición dice que en la cena se deja mejor
# propina; los datos dicen que es prácticamente igual (16,0 % frente a
# 16,4 %) y que el almuerzo incluso gana por poco. Para eso sirve el KPI:
# para corregir la intuición con evidencia.


# 6. Su turno: tres retos
# Los tres se resuelven con el mismo patrón de la sección 5:
# filtrar y llamar propina_promedio().




# Reto 1 - Fin de semana. Compare el porcentaje de propina de sábado y
#   domingo frente al resto de la semana. Pista: los días vienen como
#   "Thur", "Fri", "Sat" y "Sun", y el filtro puede ser
#   df[df["dia"].isin(["Sat", "Sun"])].

fin_de_semana=df[df["dia"].isin(["Sat", "Sun"])]
resto_de_semana=df[~df["dia"].isin(["Sat", "Sun"])]
#resto_de_semana=df[df["dia"].isin(["Mon", "Tue", "Wed", "Thur", "Fri"])]

print("\nPropina promedio fin de semana:  ", propina_promedio(fin_de_semana), "%")
print("Propina promedio resto de semana:", propina_promedio(resto_de_semana), "%")

#
# Reto 2 - Mesas grandes. ¿Las mesas de 4 o más personas dejan mejor o
#   peor porcentaje que las de 1 o 2? El filtro usa una desigualdad:
#   df[df["personas"] >= 4].

mesas_grandes= df[df["personas"] >= 4]
resto_de_mesas= df[df["personas"] <= 2]                

print("\nPropina promedio mesas grandes:", propina_promedio(mesas_grandes), "%")
print("Propina promedio resto de mesas:", propina_promedio(resto_de_mesas), "%")


# Reto 3 - Su propia función. Escriba cuenta_promedio(tabla), que calcule
#   el valor promedio de la cuenta, y úsela para comparar cena y almuerzo.


# Reto 3: su código aquí
def cuenta_promedio(tabla):
    return round(tabla["cuenta"].mean(), 2)

cena = df[df["momento"] == "Cena"]
almuerzo = df[df["momento"] == "Almuerzo"]

print("Promedio cena:", cuenta_promedio(cena), "$")
print("Promedio almuerzo:", cuenta_promedio(almuerzo), "$")

# 7. Cierre
# Con una URL, tres transformaciones y una función usted calculó un KPI
# sobre 244 registros reales, sin escribir un solo ciclo.
#
# Cápsula pandas 2: filtros combinados y columnas derivadas, con los
# datos del Restaurante La Analítica.




