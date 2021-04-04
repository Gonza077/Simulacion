from  random import *
import matplotlib.pyplot as plt
import stats
import numpy
import math

def generoValoresPoisson(lambdaa):
    x=0
    tr=1
    b=math.exp(-lambdaa)
    while(tr-b)>0:
        tr= tr*random()
        if(tr-b)>0:
          x=x+1
    return(x)

def muestroEspeYVar(valores,lambdaa,i):
    print("\n Muestra Nro ",i+1)
    print("\nEl calculo de la Esperanza de los valores generados es:", stats.mean(valores))
    print("Teoricamente es =", lambdaa)
    print("El calculo de la Varianza de los valores generados es =", numpy.var(valores))
    print("Teoricamente es:", lambdaa)
    print("El Desvio Estandar de los valores generados es = ",math.sqrt(numpy.var(valores)))
    print("Teoricamente es =",math.sqrt(lambdaa))

def creoHistogramas(valores,lambdaa):
    plt.hist(valores,edgecolor='black',linewidth=1,density=1, label=(f'Lambda={lambdaa}'))
    y=[(( math.exp(-lambdaa)* (lambdaa**x ) )/(math.factorial(x))) for x in valores]
    plt.plot(valores,y,'.')
    plt.legend(title='Parametros Muestra')
    plt.grid(True)
    plt.title("Grafica")
    plt.show()

cantNum = 1000
lambdas=[3,7]
for i in range(0,2):
    valores = []
    for j in range(0,cantNum):
        valores.append(generoValoresPoisson(lambdas[i]))
    muestroEspeYVar(valores,lambdas[i],i)
    creoHistogramas(valores,lambdas[i])
