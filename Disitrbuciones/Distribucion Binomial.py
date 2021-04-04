from  random import *
import matplotlib.pyplot as plt
import stats
import numpy
import math

def generoValoresBinomial(probSuceso,numeroEnsayos):
    x=0
    for i in range(0,numeroEnsayos):
        if ( random() -probSuceso )<0:
            x=x+1
    return(x)

def cantCombinaciones(m, n):
    return ( math.factorial(m) // (math.factorial(n) * math.factorial(m - n)) )

def muestroEspeYVar(valores,probSuceso,numeroEnsayos):
    print("\nEl calculo de la Esperanza de los valores generados es:", stats.mean(valores))
    print("Teoricamente es =",numeroEnsayos*probSuceso)
    print("El calculo de la Varianza de los valores generados es =",numpy.var(valores) )
    print("Teoricamente es:", numeroEnsayos*probSuceso*(1-probSuceso))
    print("El Desvio Estandar de los valores generados es = ",math.sqrt(numpy.var(valores)))
    print("Teoricamente es =",math.sqrt(numeroEnsayos*probSuceso*(1-probSuceso)))

def creoHistogramas(valores,probSuceso,numeroEnsayos):
    plt.hist(valores, color='b',edgecolor = 'black',linewidth=1,density=1, label=(f'Prob.Suceso 1 ={probSuceso} , Num. de Ensayos 1= {numeroEnsayos}'))
    plt.xlabel("Valores")
    plt.ylim(0,0.05)
    y=[(cantCombinaciones(numeroEnsayos,x))*( probSuceso**x ) * ( (1-probSuceso)**(numeroEnsayos-x) ) for x in valores]
    plt.legend()
    plt.plot(valores,y, '.')
    plt.grid(True)
    plt.title("Grafica de Distribuciones Exponencial")
    plt.show()


cantNum = 1000
probSuceso=[0.8,0.6,]
numeroEnsayos=[1000,900]
for i in range(0,2):
    valores1 = []
    for j in range(0,cantNum):
        valores1.append(generoValoresBinomial(probSuceso[i],numeroEnsayos[i]))
    print("Muestra Nro",i+1)
    muestroEspeYVar(valores1,probSuceso[i],numeroEnsayos[i])
    creoHistogramas(valores1,probSuceso[i],numeroEnsayos[i])