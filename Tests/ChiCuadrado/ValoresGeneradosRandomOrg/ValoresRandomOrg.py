import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats

def cargoArchivos():
    datos1=pd.read_excel("Datos.xlsx",header=None)
    listaDatos1={col:datos1[col].dropna().tolist() for col in datos1.columns}[0]
    return listaDatos1

def limpiarLista(lista):
    listaEnteros=[]
    lista=lista[0]   #Aca la lista queda con las frecuencias pero en flotante
    for i in range(0,len(lista)):
        listaEnteros.append(int(lista[i])) #Los llevo a un valor entero para no generar problemas
    return listaEnteros

def creoValorChiCuadrado(listaFrecAbsoluta,n,k):
    valor=0
    for i in range(0, k):
        valor = valor + (listaFrecAbsoluta[i] - n / k) ** 2  # Es la sumatoria del apunte
    valor= (k/n)*valor              #Asignacion del valor de la sumatoria multiplicado por el valor de k/n
    return valor

#Programa principal
valores=[]
k=int(input("Ingrese la cantidad de intervalos que desea : "))
valores=cargoArchivos()
n=len(valores)              #Dependiendo de la cantidad de valores generados esto varia
listaFrecAbsoluta=plt.hist(valores,k)
listaFrecAbsoluta=limpiarLista(listaFrecAbsoluta)
valorChiCuadrado=creoValorChiCuadrado(listaFrecAbsoluta,n,k)
print("\nEl valor ChiCuadrado generado con los valores es =",valorChiCuadrado)
print("El valor esperado es = ",scipy.stats.chisquare(listaFrecAbsoluta)[0])
