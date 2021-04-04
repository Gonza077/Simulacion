from random import random
import matplotlib.pyplot as plt
import stats
import numpy
import math

def calcularEsperanza(alfa):
    esperanza=1/alfa
    return esperanza

def calcularVarianza(alfa):
    var= 1/(alfa**2)
    return var

def muestroEspeYVar(valores,esperanzaTeorica,alfa):
    print("El calculo de la Esperanza en la muestra es:", stats.mean(valores))
    print("Teoricamente la Esperanza es:", esperanzaTeorica)
    print("El calculo de la Varianza en la muestra es:", numpy.var(valores))
    print("Teoricamente la Varianza es:", calcularVarianza(alfa))
    print("El calculo del Desvio Estandar en la muestra es:", math.sqrt(numpy.var(valores)))
    print("Teoricamente es:", math.sqrt(calcularVarianza(alfa)))
    print("El parametro alfa de la muestra es :",1/(stats.mean(valores)))
    print("Teoricamente es :",alfa)
    print("\n")


def creoGraficos(valores,alfa,i):
    y = [alfa*math.exp(-alfa*x) for x in valores]
    plt.plot(valores, y,'.')
    plt.hist(valores,edgecolor = 'black',linewidth=1,density=1,alpha=0.5 ,label=(f'Funcion {i+1} Alfa ={alfa}'))
    plt.legend(title='Funcion densidad')
    plt.xlabel("Valores")
    plt.grid(True)
    plt.title("Grafica de Distribuciones Exponencial")
    plt.show()


cantNum = 1000
alfas=[2,3]
for i in range(0,len(alfas)):
    valores = []
    esperanzaTeorica=calcularEsperanza(alfas[i])
    for j in range(0,cantNum):
         valores.append((-esperanzaTeorica) * (math.log(random())))
    print("Muestra Nro",i+1)
    muestroEspeYVar(valores,esperanzaTeorica,alfas[i])
    y = [alfas[i] * math.exp(-alfas[i] * x) for x in valores]
    plt.plot(valores, y, '.')
    plt.hist(valores,color='red',edgecolor="black", linewidth=1, density=1, alpha=1, label=(f'Funcion {i + 1} Alfa ={alfas[i]}'))
    plt.legend()
    plt.xlabel("Valores")
    plt.grid(True)
    plt.title("Grafica de Distribucion Exponencial")
    plt.show()

#plt.show() Esto sirve para graficar todo de una