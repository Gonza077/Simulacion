import random
import matplotlib.pyplot as plt
import scipy.stats

n = 1000
valoresGenerados = []
listaFrecAbsoluta=[]

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

def creoValoresRandom():
    valor=random.random()
    return valor

#Programa principal
for i in range (0,n):
   valoresGenerados.append(creoValoresRandom())
k=int(input("Ingrese la cantidad de intervalos : "))
lista=plt.hist(valoresGenerados,bins=k)
listaFrecAbsoluta=limpiarLista(lista)
print(listaFrecAbsoluta)
print("\nLa frecuencia absoluta por intervalos es ",listaFrecAbsoluta)
valorChiCuadrado=creoValorChiCuadrado(listaFrecAbsoluta,n,k)
print("\nEl valor generado de ChiCuadrado es = ",valorChiCuadrado)
print("El valor esperado es = ",scipy.stats.chisquare(listaFrecAbsoluta)[0])



