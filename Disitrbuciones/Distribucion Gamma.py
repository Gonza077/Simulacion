from random import random
import matplotlib.pyplot as plt
import stats
import numpy
import math

def generoDistGamma(ka,alfa):
    tr = 1
    for i in range(0, ka):
        tr =tr * random()
    return (-(math.log(tr)) / alfa)

def creoHistogramas(valores,alfa,ka):
    plt.hist(valores,bins=100,edgecolor = 'black',linewidth=1,density=1, label=(f'Alfa = {alfa} , k1 = {ka}'))
    plt.xlabel("Valores")
    y=[((alfa**ka)*(x**(ka-1))*math.exp(-alfa*x))/math.factorial(ka-1) for x in valores]
    plt.grid(True)
    plt.title("Distribucion Gamma")
    plt.plot(valores,y,'.')
    plt.title("Grafica de Distribuciones Gamma")
    plt.show()

def muestroEsperanzayVar(valores,alfa,ka):
    print("El calculo de la esperanza en la muestra es:",stats.mean(valores))
    print("Teoricamente la Esperanza es = ",ka/alfa)
    print("El calculo de la Varianza es = ",numpy.var(valores))
    print("Teoricamente la Varianza es = ",ka/(alfa**2))
    print("El Desvio estandar es =",math.sqrt(numpy.var(valores)))
    print("Teoricamente es =",math.sqrt(ka/(alfa**2)))

cantNum = 10000
alfas=[4,9]
kas=[5,8]
for i in range(0,2):
    valores = []
    for j in range(0,cantNum):
        valores.append(generoDistGamma(kas[i],alfas[i]))
    print("Muestra Nro ",i+1)
    muestroEsperanzayVar(valores,alfas[i],kas[i])
    creoHistogramas(valores,alfas[i],kas[i])
    print("\n")
#plt.show() Esto sirve para graficar todo de una pero se tiene que sacar el show dentro de la funcion graficos