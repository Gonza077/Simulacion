from  random import *
import matplotlib.pyplot as plt
import stats
import numpy
import math

def calculaEsperanzaTeorica(a,b):
    e=(a+b)/2
    return e

def calculaVarianzaTeorica(a,b):
    v=((b-a)**2)/12
    return v

def creoGraficos(valores,limInfe,limSup):
    plt.hist(valores,edgecolor = 'black',linewidth=1,density=1)
    y=[1/(limSup-limInfe)for x in valores]
    plt.plot(valores,y)
    plt.grid(True)
    plt.show()

def muestroEspeVarianzaDesvio(valores,a,b):
    esperanza = stats.mean(valores)
    esperanzaTeorica = calculaEsperanzaTeorica(a, b)
    print("\nEl calculo de la esperanza en la muestra es:", esperanza, "\nTeoricamente la esperanza es:",esperanzaTeorica)
    varianza = numpy.var(valores)
    varianzaTeorica = calculaVarianzaTeorica(a, b)
    print("\nEl calculo de la varianza en la muestra es:", varianza, "\nTeoricamente la varianza es:",varianzaTeorica)
    desvioEstandar = math.sqrt(varianza)
    desvioEstandarTeorico = math.sqrt(varianzaTeorica)
    print("\nEl calculo del desvio estandar en la muestra es:", desvioEstandar, "\nTeoricamente el desvio estandar es:",desvioEstandarTeorico)

valores=[]
limInfe= 0
limSup= 1000
for i in range (limInfe,limSup):
     valores.append(limInfe + (limSup - limInfe)*(random()))

muestroEspeVarianzaDesvio(valores,limInfe,limSup)
creoGraficos(valores,limInfe,limSup)