from  random import *
import matplotlib.pyplot as plt
import stats
import numpy
import math
import os


def generoValoresNormales(mu,sigma):
    sum=0
    for i in range(0,12):
        r=random()
        sum=sum+r
    return(sigma*(sum-6)+mu)

def muestroEspeYVar(valores,mu,sigma):
    print("\nEl calculo de la Esperanza de la muestra es:", stats.mean(valores))
    print("Teoricamente es =", mu)
    print("El calculo de la Varianza de la muestra es =",numpy.var(valores) )
    print("Teoricamente es:",  sigma**2)
    print("El Desvio Estandar de la muestra es = ",math.sqrt(numpy.var(valores)))
    print("Teoricamente es =",sigma)

def creoHistogramas(valores,mu,sigma):
    plt.hist(valores1,edgecolor = 'black',linewidth=1,density=1, label=(f'Media 1 = {mu} , Sigma 1= {sigma}'))
    plt.xlabel("Valores")
    plt.ylim(0, 0.2)
    y=[(1/(sigma*(math.sqrt(2*math.pi))))*math.exp((-1/2)*((x-mu)/sigma)**2) for x in valores]
    plt.plot(valores,y,'.')
    plt.legend(title="Funcion densidad")
    plt.grid(True)
    plt.title("Grafica de Distribuciones Exponencial")
    plt.show()

cantNum = 1000
mu=[25,30]
sigma=[3,5]
print(math.pi)
for i in range(0,2):
    valores1 = []
    for j in range(0,cantNum):
        valores1.append(generoValoresNormales(mu[i],sigma[i]))
    print("\nMuestra numero ",i+1)
    muestroEspeYVar(valores1,mu[i],sigma[i])
    creoHistogramas(valores1,mu[i],sigma[i])
