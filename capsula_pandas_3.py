# -*- coding: utf-8 -*-
"""Cápsula pandas 3: Agrupar para decidir

Programación para Analítica de Datos 2026-2

La aplicación de domicilios factura mucho
pero su comisión se come la utilidad. Para decidir dónde poner el
esfuerzo comercial, la gerencia necesita el panorama completo:

    ¿Cuál canal vende más... y cuál deja más utilidad?

Filtrar canal por canal funcionaría, pero seríamos nosotros repitiendo el
trabajo. groupby() lo hace de una sola vez: reúne las filas que comparten
una categoría y calcula un resumen por grupo.

La ruta de trabajo:
    DataFrame > columnas derivadas > groupby > agg > ordenar > decidir

Requisitos: pip install pandas
Ejecución:  python Capsula_pandas_3.py
"""

import pandas as pd


# 1. Los mismos datos de la Cápsula 2
# Las 16 transacciones del Restaurante La Analítica, con su canal.

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

# La cadena de la Cápsula 2, condensada en cuatro líneas.
TASA_COMISION = {"Salón": 0.00, "Para llevar": 0.05, "Aplicación": 0.18}

df["ingreso"] = df["cantidad"] * df["precio_unitario"]
df["comision"] = df["ingreso"] * df["canal"].map(TASA_COMISION)
df["utilidad"] = df["ingreso"] - df["cantidad"] * df["costo_unitario"] - df["comision"]

print("Tabla lista:", df.shape[0], "filas y", df.shape[1], "columnas")


# 2. groupby en su forma más simple
# df.groupby("canal") reúne las filas de cada canal; ["ingreso"].sum()
# suma el ingreso dentro de cada grupo. Tres filtros manuales se vuelven
# una sola instrucción.

ingreso_por_canal = df.groupby("canal")["ingreso"].sum()
print("\nIngreso por canal:")
print(ingreso_por_canal.to_string())

# El resultado es una Series: los canales quedaron como índice. Para
# recuperar una tabla común y corriente, reset_index().


# 3. Varios indicadores a la vez con agg()
# agg() recibe pares nombre_nuevo=("columna", "función") y genera la tabla
# de indicadores completa en una iteración.

kpi_canal = (
    df.groupby("canal")
      .agg(
          transacciones=("producto", "count"),
          ingreso=("ingreso", "sum"),
          comision=("comision", "sum"),
          utilidad=("utilidad", "sum"),
      )
      .reset_index()
)

print("\nKPI por canal:")
print(kpi_canal.to_string(index=False))


# 4. Ordenar para responder
# sort_values() ordena la tabla por una columna; ascending=False pone el
# mayor de primero. Ordenar dos veces, por dos columnas distintas,
# responde las dos preguntas de la gerencia.

print("\n¿Quién vende más?    ->", kpi_canal.sort_values("ingreso", ascending=False).iloc[0]["canal"])
print("¿Quién deja más utilidad? ->", kpi_canal.sort_values("utilidad", ascending=False).iloc[0]["canal"])

# Lectura del resultado: la aplicación es el canal que más factura, pero
# el salón, sin comisiones, es el que más utilidad deja. Si la decisión
# se hubiera tomado mirando solo las ventas, habría sido la equivocada.
# Para eso se agrupa: para comparar categorías completas antes de decidir.


# 5. El patrón, encapsulado en una función
# La misma idea de las Cápsulas 1 y 2: lo que se calculó una vez se
# escribe como función y queda listo para reutilizarse con cualquier
# subconjunto de la tabla.

def utilidad_por_canal(tabla):
    """KPI: tabla de utilidad por canal, de mayor a menor."""
    return (
        tabla.groupby("canal")["utilidad"]
             .sum()
             .sort_values(ascending=False)
             .reset_index()
    )


print("\nUtilidad por canal (toda la tabla):")
print(utilidad_por_canal(df).to_string(index=False))

solo_centro = df[df["sede"] == "Centro"]
print("\nUtilidad por canal (solo sede Centro):")
print(utilidad_por_canal(solo_centro).to_string(index=False))


# 6. Retos
# Dos retos con el patrón de las secciones 3 a 5, y uno para valientes.
#
# Reto 1 - Por sede. Construya el KPI por sede (transacciones, ingreso y
#   utilidad) con agg() y diga cuál sede lidera la utilidad.

# Reto 2 - El producto líder. Agrupe por producto, sume unidades
#   (cantidad) e ingreso, y ordene de mayor a menor ingreso. ¿El producto
#   que más unidades vende es el que más ingreso genera?
#
# Reto 3 - Margen por producto. Sobre la tabla del Reto 2 agregue también
#   la utilidad y calcule margen_pct = utilidad / ingreso * 100 por
#   producto. Recuerde la regla vista en clase: primero se suman
#   numerador y denominador y se divide al final; los porcentajes no se
#   promedian.

# Reto 1: su código aquí
kpi_sede = (df.groupby("sede").agg
            (transacciones=("producto", "count"),ingreso=("ingreso", "sum"),utilidad=("utilidad", "sum"),).reset_index())

print("\nKPI por sede:")
print(kpi_sede.to_string(index=False))

lider = kpi_sede.sort_values("utilidad", ascending=False).iloc[0]["sede"]

print("La sede que lidera la utilidad :", lider)

# Reto 2: su código aquí
kpi_producto = (df.groupby("producto").agg(unidades=("cantidad", "sum"),ingreso=("ingreso", "sum"),)
          .reset_index().sort_values("ingreso", ascending=False))

print("\nKPI por producto:")
print(kpi_producto.to_string(index=False))

lider_unidades = kpi_producto.sort_values("unidades", ascending=False).iloc[0]["producto"]

lider_ingreso = kpi_producto.sort_values("ingreso", ascending=False).iloc[0]["producto"]

print("Producto líder en unidades:", lider_unidades) 
print("Producto líder en ingreso:", lider_ingreso)

# Reto 3: su código aquí
kpi_producto = (df.groupby("producto").agg(unidades=("cantidad", "sum"),ingreso=("ingreso", "sum"),utilidad=("utilidad", "sum"),)
      .reset_index()
      .sort_values("ingreso", ascending=False))

kpi_producto["margen_pct"] = (kpi_producto["utilidad"] / kpi_producto["ingreso"] * 100)

print("\nReto 3 - Margen por producto:")
print(kpi_producto.to_string(index=False))


# 7. Cierre
# groupby + agg + sort_values: tres instrucciones que convierten 16
# transacciones en una decisión de gerencia. Y la lección quedó escrita
# en los datos, pues el canal que más vende no es el que más utilidad deja.
