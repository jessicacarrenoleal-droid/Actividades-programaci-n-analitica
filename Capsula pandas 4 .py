# -*- coding: utf-8 -*-
"""Cápsula pandas 4: El CSV del mundo real.

Programación para Analítica de Datos 2026-2

Las sedes enviaron su registro de ventas en un CSV exportado a mano
desde el punto de venta, en formato separado por punto y coma, con espacios de más,
mayúsculas al gusto de cada cajero, filas repetidas y celdas vacías.
Además trae la columna calificación de 1 a 5 que una tableta
en la caja le pide al cliente.

La pregunta de la gerencia es de negocio: ¿cuánto vendió cada sede?
Pero con estos datos, la respuesta directa saldría mal. Primero se
limpia, después se analiza. Y limpiar no siempre es rellenar: a veces
la decisión correcta es borrar una columna completa.

Requisitos: pip install pandas
Ejecución:  python capsula_pandas_4.py
"""

import pandas as pd


# 0. El archivo sucio
# Para que la cápsula sea autocontenida, el script escribe el CSV tal
# como llegó y luego lo lee. En su trabajo real, este archivo se lo
# entregan a usted; salte directo a la sección 1.

CSV_SUCIO = """fecha;producto;cantidad;precio_unitario;sede;canal;calificacion
2026-08-03;Bowl Andino ;2;24000; Centro;Salón;5
2026-08-03;Pasta Urbana;1;28000;norte;Aplicación;
2026-08-04; Bowl Andino;1;24000;CENTRO;Para llevar;
2026-08-04;Hamburguesa Central;2;30000;Norte ;Aplicación;
2026-08-05;Ensalada de la Casa;1;22000;centro;;
2026-08-05;Limonada Natural;2;8000; Centro ;Salón;4
2026-08-06;Pasta Urbana;2;28000;NORTE;Salón;
2026-08-07;Bowl Andino;3;24000;Centro;Aplicación;3
2026-08-07;Bowl Andino;3;24000;Centro;Aplicación;3
2026-08-10;Pasta Urbana ;1;28000;Centro;Para llevar;
2026-08-10;Hamburguesa Central;1;30000;norte;Aplicación;
2026-08-11;Bowl Andino;2;24000;Centro;;
2026-08-11;Ensalada de la Casa;2;22000; centro;Aplicación;5
2026-08-12;Hamburguesa Central;1;30000;Norte;Aplicación;
2026-08-12;Limonada Natural;3;8000;Centro;Para llevar;
2026-08-13;Pasta Urbana;1;28000;Norte;Aplicación;
2026-08-13;Pasta Urbana;1;28000;Norte;Aplicación;
2026-08-14;Bowl Andino;2;24000;CENTRO ;Salón;4
"""

with open("ventas_sucias.csv", "w", encoding="utf-8") as archivo:
    archivo.write(CSV_SUCIO)


# 1. Leer un CSV que no usa comas
# En medio mundo (Colombia incluida) Excel exporta con punto y coma.
# El parámetro sep=";" se lo dice a read_csv. Si se olvida, todo el
# archivo queda en una sola columna: ese es el primer síntoma a revisar.

df = pd.read_csv("ventas_sucias.csv", sep=";")
print("Tabla cargada:", df.shape[0], "filas y", df.shape[1], "columnas")


# 2. Diagnosticar antes de limpiar
# La regla de la Cápsula 1, elevada al cuadrado: nunca limpie una tabla
# que no ha diagnosticado.

# a) ¿Qué valores distintos hay en las columnas de texto?
print("\nValores de 'sede' tal como llegaron:")
print(df["sede"].unique())

# b) ¿Qué tan vacía está cada columna? isna() marca las celdas vacías y
# mean() convierte esas marcas en proporción: el diagnóstico más útil
# de esta cápsula.
print("\nPorcentaje de celdas vacías por columna:")
print((df.isna().mean() * 100).round(1).to_string())

# c) ¿Cuántas filas repetidas hay?
print("\nFilas duplicadas:", df.duplicated().sum())

# El diagnóstico deja tres problemas de tamaño muy distinto: 'Centro'
# escrito de seis formas, un puñado de canales vacíos... y una columna,
# calificacion, vacía en dos de cada tres filas.


# 3. Limpiar texto: strip y una capitalización uniforme
# El accesor .str aplica las operaciones de cadenas que usted ya conoce
# a la columna completa: .str.strip() quita espacios en los bordes y
# .str.capitalize() deja Primera-mayúscula-resto-minúsculas.

df["sede"] = df["sede"].str.strip().str.capitalize()
df["producto"] = df["producto"].str.strip()

print("\nValores de 'sede' después de limpiar:")
print(df["sede"].unique())


# 4. Eliminar duplicados
# drop_duplicates() conserva la primera aparición de cada fila repetida.
# Se hace después de limpiar el texto: "Bowl Andino" y "Bowl Andino " no
# se reconocen como duplicados mientras el espacio siga ahí.

antes = len(df)
df = df.drop_duplicates()
print("\nDuplicados eliminados:", antes - len(df), "-> quedan", len(df), "filas")


# 5. Datos faltantes: tres situaciones, tres decisiones
# fillna() no es un reflejo automático. Cada hueco se resuelve según su
# tamaño y según lo que se sepa del negocio.

# Caso A - Pocos huecos y una regla de negocio clara: se rellena.
# El punto de venta solo registra el canal cuando no es el salón, así
# que un canal vacío es, por definición, una venta de salón.
df["canal"] = df["canal"].fillna("Salón")

# Caso B - Una columna mayormente vacía y sin regla de imputación: se
# elimina completa. Con dos tercios de huecos, cualquier relleno (el
# promedio, un 3 "neutro", lo que sea) inventaría más datos de los que
# hay de verdad, y un promedio calculado sobre 5 respuestas voluntarias
# diría más de quién quiso contestar que de la satisfacción real.
df = df.drop(columns=["calificacion"])
print("\nColumna 'calificacion' eliminada. Columnas restantes:", list(df.columns))

# No hay un umbral mágico, pero pasado el 50% de vacíos y sin una regla
# confiable para rellenar, la carga de la prueba se invierte: hay que
# justificar por qué conservarla. La decisión se documenta (este
# comentario es esa documentación) y, si la encuesta le interesa a
# alguien, se analiza aparte con las filas que sí respondieron.

# Caso C - Dato faltante en una columna esencial (fecha, producto, cantidad):
# ni rellenar ni borrar la columna; se elimina la fila completa con dropna(),
# porque una venta sin producto no es una venta. En este archivo no
# ocurrió, pero es la tercera puerta y conviene saber que existe.


# 6.  KPI
# La tabla limpia responde en dos líneas lo que la sucia habría
# respondido mal.

df["ingreso"] = df["cantidad"] * df["precio_unitario"]

ingreso_por_sede = df.groupby("sede")["ingreso"].sum().sort_values(ascending=False)
print("\nIngreso por sede (tabla limpia):")
print(ingreso_por_sede.to_string())

# Dos sedes, sin el ingreso inflado por los duplicados y
# sin arrastrar una columna que no aportaba nada al cálculo.


# 7. Retos
#
# Reto 1 - El costo del descuido. Vuelva a leer ventas_sucias.csv sin
#   limpiar nada, calcule el ingreso por sede y compare contra la
#   sección 6. ¿Cuántas "sedes" aparecen y cuánto ingreso sobra?
## Reto 1 - El costo del descuido

# Reto 2 - Escriba limpiar_ventas(tabla) para aplicar 
#   en orden las secciones 3 a 5 (incluida la eliminación de
#   calificacion) y devuelva la tabla limpia. Verifíquela: 16 filas,
#   6 columnas, cero celdas vacías.
#
# Responda la sigueinte pregunta:
#   ¿en qué escenario sería un error borrar la columna calificacion,
#   aun con dos tercios de las celdas vacías? Piense qué pasaría si la
#   pregunta de la gerencia no fuera "¿cuánto vendió cada sede?"

# Reto 1: su código aquí

df_sucio = pd.read_csv("ventas_sucias.csv", sep=";")

df_sucio["ingreso"] = df_sucio["cantidad"] * df_sucio["precio_unitario"]

ingreso_por_sede_sucia = (df_sucio.groupby("sede")["ingreso"].sum().sort_values(ascending=False))

print("\nIngreso por sede (tabla sucia):")
print(ingreso_por_sede_sucia.to_string())

print("\nCantidad de sedes que aparecen:", df_sucio["sede"].nunique())

ingreso_sucio = df_sucio["ingreso"].sum()
ingreso_limpio = df["ingreso"].sum()

print("\nIngreso total sucio:", ingreso_sucio)
print("Ingreso total limpio:", ingreso_limpio)
print("Ingreso que sobra:", ingreso_sucio - ingreso_limpio)

# Reto 2: su código aquí



# 8. Cierre
# Limpiar fue tomar cuatro decisiones distintas: uniformar el texto,
# borrar duplicados, rellenar con criterio y eliminar una columna que
# no daba para más. Y la función limpiar_ventas() del Reto 2 no es un
# ejercicio de juguete: téngala a mano para el estudio de caso.
#
# Cápsula pandas 5: dos tablas que se necesitan. Las ventas por un lado,
# el catálogo de productos por otro... y esta vez, desde una base de
# datos SQL.