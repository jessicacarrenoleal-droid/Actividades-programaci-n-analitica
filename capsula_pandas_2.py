# -*- coding: utf-8 -*-
"""Cápsula pandas 2: Filtros combinados y columnas derivadas.

Programación para Analítica de Datos 2026-2

Llegaron los datos propios del Restaurante La Analítica: 16 transacciones
de dos sedes, ahora con el canal de venta. El restaurante vende en el
salón, para llevar y por una aplicación de domicilios que cobra comisión.
La pregunta de la gerencia:

    ¿Los pedidos por la aplicación realmente dejan utilidad?


La ruta de trabajo:
    lista de diccionarios > DataFrame > filtros combinados
    > cadena de columnas derivadas: ingreso > comisión -> utilidad

Requisitos: pip install pandas
Ejecución:  python Capsula_pandas_2.py
"""

import pandas as pd


# 1. Los datos, esta vez escritos a mano
# En la Cápsula 1 los datos llegaron por una URL. Aquí nacen como una
# lista de diccionarios (la estructura que usted ya domina) y
# pd.DataFrame() los convierte en tabla en una sola línea.

ventas = [
    {"fecha": "2026-08-03", "producto": "Bowl Andino",         "categoria": "Almuerzo", "cantidad": 2, "precio_unitario": 24000, "costo_unitario": 14000, "sede": "Centro", "canal": "Salón"},
    {"fecha": "2026-08-03", "producto": "Pasta Urbana",        "categoria": "Almuerzo", "cantidad": 1, "precio_unitario": 28000, "costo_unitario": 17000, "sede": "Norte",  "canal": "Aplicación"},
    {"fecha": "2026-08-04", "producto": "Bowl Andino",         "categoria": "Almuerzo", "cantidad": 1, "precio_unitario": 24000, "costo_unitario": 14000, "sede": "Centro", "canal": "Para llevar"},
    {"fecha": "2026-08-04", "producto": "Hamburguesa Central", "categoria": "Cena",     "cantidad": 2, "precio_unitario": 30000, "costo_unitario": 19000, "sede": "Norte",  "canal": "Aplicación"},
    {"fecha": "2026-08-05", "producto": "Ensalada de la Casa", "categoria": "Almuerzo", "cantidad": 1, "precio_unitario": 22000, "costo_unitario": 12000, "sede": "Centro", "canal": "Salón"},
    {"fecha": "2026-08-05", "producto": "Limonada Natural",    "categoria": "Bebida",   "cantidad": 2, "precio_unitario": 8000,  "costo_unitario": 2500,  "sede": "Centro", "canal": "Salón"},
    {"fecha": "2026-08-06", "producto": "Pasta Urbana",        "categoria": "Almuerzo", "cantidad": 2, "precio_unitario": 28000, "costo_unitario": 17000, "sede": "Norte",  "canal": "Salón"},
    {"fecha": "2026-08-07", "producto": "Bowl Andino",         "categoria": "Almuerzo", "cantidad": 3, "precio_unitario": 24000, "costo_unitario": 14000, "sede": "Centro", "canal": "Aplicación"},
    {"fecha": "2026-08-10", "producto": "Pasta Urbana",        "categoria": "Almuerzo", "cantidad": 1, "precio_unitario": 28000, "costo_unitario": 17000, "sede": "Centro", "canal": "Para llevar"},
    {"fecha": "2026-08-10", "producto": "Hamburguesa Central", "categoria": "Cena",     "cantidad": 1, "precio_unitario": 30000, "costo_unitario": 19000, "sede": "Norte",  "canal": "Aplicación"},
    {"fecha": "2026-08-11", "producto": "Bowl Andino",         "categoria": "Almuerzo", "cantidad": 2, "precio_unitario": 24000, "costo_unitario": 14000, "sede": "Centro", "canal": "Salón"},
    {"fecha": "2026-08-11", "producto": "Ensalada de la Casa", "categoria": "Almuerzo", "cantidad": 2, "precio_unitario": 22000, "costo_unitario": 12000, "sede": "Centro", "canal": "Aplicación"},
    {"fecha": "2026-08-12", "producto": "Hamburguesa Central", "categoria": "Cena",     "cantidad": 1, "precio_unitario": 30000, "costo_unitario": 19000, "sede": "Norte",  "canal": "Aplicación"},
    {"fecha": "2026-08-12", "producto": "Limonada Natural",    "categoria": "Bebida",   "cantidad": 3, "precio_unitario": 8000,  "costo_unitario": 2500,  "sede": "Centro", "canal": "Para llevar"},
    {"fecha": "2026-08-13", "producto": "Pasta Urbana",        "categoria": "Almuerzo", "cantidad": 1, "precio_unitario": 28000, "costo_unitario": 17000, "sede": "Norte",  "canal": "Aplicación"},
    {"fecha": "2026-08-14", "producto": "Bowl Andino",         "categoria": "Almuerzo", "cantidad": 2, "precio_unitario": 24000, "costo_unitario": 14000, "sede": "Centro", "canal": "Salón"},
]

df = pd.DataFrame(ventas)
print("Tabla cargada:", df.shape[0], "filas y", df.shape[1], "columnas")
print(df.head().to_string())


# 2. Filtros combinados: & es "y", | es "o"
# En la Cápsula 1 cada filtro usó una sola condición. Dos reglas nuevas:
#   a) cada condición va entre paréntesis
#   b) & exige que se cumplan ambas, | acepta cualquiera de las dos.

almuerzos_centro = df[(df["categoria"] == "Almuerzo") & (df["sede"] == "Centro")]
print("\nAlmuerzos en la sede Centro:", len(almuerzos_centro), "transacciones")

bebidas_o_grandes = df[(df["categoria"] == "Bebida") | (df["cantidad"] >= 3)]
print("Bebidas o pedidos de 3+ unidades:", len(bebidas_o_grandes), "transacciones")

# isin() abrevia varios "o" sobre la misma columna: en lugar de
# (canal == "Salón") | (canal == "Para llevar"), una sola condición.
venta_directa = df[df["canal"].isin(["Salón", "Para llevar"])]
print("Venta directa (salón o para llevar):", len(venta_directa), "transacciones")


# 3. La cadena de columnas derivadas: ingreso > comisión > utilidad
# Cada columna nueva se apoya en la anterior. Este encadenamiento es el
# corazón del trabajo con pandas. Así, la tabla se va enriqueciendo paso a paso.

# Paso 1: el ingreso de cada transacción.
df["ingreso"] = df["cantidad"] * df["precio_unitario"]

# Paso 2: la comisión depende del canal. .map() con un diccionario
# traduce cada categoría a su tasa; es el "diccionario aplicado a toda
# una columna de una sola vez".
TASA_COMISION = {"Salón": 0.00, "Para llevar": 0.05, "Aplicación": 0.18}

df["tasa_comision"] = df["canal"].map(TASA_COMISION)
df["comision"] = df["ingreso"] * df["tasa_comision"]

# Paso 3: la utilidad descuenta el costo de los insumos y la comisión.
df["costo"] = df["cantidad"] * df["costo_unitario"]
df["utilidad"] = df["ingreso"] - df["costo"] - df["comision"]

print("\nTabla con la cadena completa:")
columnas_clave = ["producto", "canal", "ingreso", "comision", "utilidad"]
print(df[columnas_clave].head(8).to_string())


# 4. El KPI como una función
# El mismo patrón de la Cápsula 1, ahora con dos indicadores en una sola
# función.

def resumen_dinero(tabla):
    """KPI: ingreso total y utilidad total de la tabla, en pesos."""
    return {
        "ingreso": int(tabla["ingreso"].sum()),
        "utilidad": int(tabla["utilidad"].sum()),
    }


print("\nKPI general:", resumen_dinero(df))


# 5. La respuesta a la pregunta
# El patrón completo es la suma del filtro combinado y la función reutilizada.

por_aplicacion = df[df["canal"] == "Aplicación"]
directa = df[df["canal"] != "Aplicación"]

print("\nPedidos por aplicación:", resumen_dinero(por_aplicacion))
print("Venta directa:         ", resumen_dinero(directa))

# La aplicación factura casi lo mismo que la venta
# directa, pero entre la comisión del 18% y los costos, la utilidad que
# deja es bastante menor. Vender más no siempre es ganar más.


# 6. Su turno: tres retos
# Los tres se resuelven con el patrón de la sección 5: filtrar (con & , |
# o isin) y llamar resumen_dinero().
#
# Reto 1 - Cenas por aplicación. ¿Cuánta utilidad dejan las cenas
#   pedidas por la aplicación? Combine dos condiciones con &.
#
# Reto 2 - Pedidos pequeños o bebidas. La gerencia sospecha que los
#   pedidos de 1 unidad y las bebidas casi no aportan. Filtre con | y
#   compare su utilidad contra la del resto de la tabla.
#
# Reto 3 - Su propia columna derivada. Cree la columna
#   df["margen_pct"] = df["utilidad"] / df["ingreso"] * 100 y escriba
#   margen_promedio(tabla), que devuelva su promedio redondeado a 1
#   decimal. Compare el margen del canal Salón frente al de Aplicación.

# Reto 1: su código aquí

cenas_aplicacion = df[(df["categoria"] == "Cena") & (df["canal"] == "Aplicación")]
print (cenas_aplicacion)
print(resumen_dinero(cenas_aplicacion)) #con & deben cumplirse las dos cena y apolicacion  filta la cena utilidad 22.400


cenas_aplicacion = df[(df["categoria"] == "Cena") | (df["categoria"] == "Aplicacion")]
print (cenas_aplicacion)
print(resumen_dinero(cenas_aplicacion))# con  es o cena ó bebida, almuerzo o colocar con lo que quiero filtra. |

cenas_aplicacion = df[df["categoria"].isin(["Cena"])]
print (cenas_aplicacion)
print(resumen_dinero(cenas_aplicacion)) # .isin busca en todas las filas que este el producto "cena"


# Reto 2: su código aquí
pedidos_pequenos_bebidas = df[(df["cantidad"] == 1) | (df["categoria"] == "Bebida")]

resto = df[ ~((df["cantidad"] == 1) | (df["categoria"] == "Bebida"))]

print("Pedidos pequeños o bebidas:", resumen_dinero(pedidos_pequenos_bebidas))
print("Resto:", resumen_dinero(resto))

# Reto 3: su código aquí
df["margen_pct"] = df["utilidad"] / df["ingreso"] * 100

def margen_promedio(tabla):
    return round(tabla["margen_pct"].mean(), 1)

salon = df[df["canal"] == "Salón"]
aplicacion = df[df["canal"] == "Aplicación"]

print("Margen promedio Salón:", margen_promedio(salon), "%")
print("Margen promedio Aplicación:", margen_promedio(aplicacion), "%")

# 7. Cierre
# La cadena ingreso > comisión > utilidad se escribió sin un solo ciclo
# y los filtros combinados respondieron una pregunta de negocio real.
