
#%% Ejercicio 1 Definir una función
def saludar():
    print("Hola")
    
saludar()
#%% Ejercicio 2  Llamar a la función
def bienvenida():
    print("Bienvenido al curso")

bienvenida()
#%% Ejercicio 3 Predice el orden de ejecución
def uno():
    print("A")

print("B")
uno()
print("C")
# Python define la funcion uno() que es B 
# el orden es B,A,C
#%% Ejercicio 4 Corrige el orden
def saludar(nombre):
    print("Hola,", nombre)  
   
saludar("Ana")
#%%  Ejercicio 5 Función con un parámetro
def saludar(nombre):
    print("Hola,", nombre)

saludar("Ana")
#%% Ejercicio 6 Función con dos parámetros 
def area(base, altura):
    return base * altura

print(area(3, 4)) 
#%%  Ejercicio 7 Completa la llamada 
def area(base, altura):
 return base * altura

print(area(5, 5)) # 25.0
#%% Ejercicio 8 Reutilizar la misma función
def con_iva(precio):
    return precio * 1.19
print(con_iva(100))
print(con_iva(250))
print(con_iva(500))
#%% Ejercicio 9 Parámetro o argumento 
def doble(n):
    return n * 2

resultado = doble(5)
# n es el parametro y 5 es el argumento
#%% Ejercicio 10 Argumentos por posición
def perfil(nombre, edad, ciudad):
    print(nombre, edad, ciudad)

perfil("Ana",20,"Bogota")
#%% Ejercicio 11 Argumentos por nombre 
def perfil(nombre, edad, ciudad):
    print(nombre, edad, ciudad)

perfil(edad=20, nombre="Ana",ciudad="Bogota")

#%% Ejercicio 12 Valor por defecto
def saludar(nombre, saludo="Hola"):
    print(saludo, nombre)

saludar("Ana")
#%%  Ejercicio 13 Reemplazar el valor por defecto 
def saludar(nombre, saludo="Hola"):
    print(saludo, nombre)
saludar("Luis", "Buen dia")
#%%  Ejercicio 14 Orden de los parámetros 
def registrar(producto, cantidad=1):
    print(producto, cantidad)
#parametro con valor va al final 
#%%  Ejercicio 15 Una lista como argumento
def total(precios):
    suma = 0
    for p in precios:
        suma = suma + p
    return suma

print(total([1200, 950, 3400]))
#%%  Ejercicio 16 Devolver un valor 
def doble(n):
    return n * 2

print(doble(5))

#%%  Ejercicio 17 Usar el valor devuelto
def doble(n):
    return n * 2

resultado = doble(6)
print(resultado + 1)
#%%  Ejercicio 18 Función sin return 
def saludo(nombre):
    print("Hola,", nombre)

x = saludo("Ana")
print(x)
# no hay nombre asociado a la variable por eso es ninguno
#%% Ejercicio 19 print o return
def doble(n):
    print(n * 2)

total = doble (5 + 3)

def doble(n):
    return n * 2

total= doble(5) + 3
print (total)

#%% Ejercicio 20 return dentro de una condición
def signo(n):
    if n < 0:
        return "negativo"
 
    return "positivo"

print(signo(-4))
print(signo(7))
#%% Ejercicio 21 return termina la función 
def prueba(n):
    if n > 0:
        return "positivo"
    
    print("linea intermedia")
    return "otro"

print(prueba(5))
# n>o ejecuta positivo print linea intermedia nunca se ejecuta
#%%Ejercicio 22 Devolver dos valores
def resumen(valores):
    return min(valores), max(valores)

menor, mayor = resumen([8, 3, 10, 5])
print(menor, mayor)
#%% Ejercicio 23 Encadenar funciones
def con_iva(p):
    return p * 1.19
def redondear(valor):
    return round(valor, 2)

print(redondear(con_iva(1200)))
#%% Ejercio 24 Variable local y global 
mensaje = "global"
def prueba():
    mensaje = "local"
    print(mensaje)

prueba()
print(mensaje)
#%% Ejercio 25  Evitar las variables globales
iva = 0.19
def con_iva(precio, iva):
    return precio * (1 + iva)

print(con_iva(1000, 0.19))