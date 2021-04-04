import random
import matplotlib.pyplot as plt

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

def generoValores(n):
    lista=[]
    for i in range(0,n):
        lista.append(random.random())
    return lista

#Programa principal
k = 10
n = 1000
valoresGenerados = []
listaFrecAbsoluta=[]
valoresGenerados=generoValores(n)
lista=plt.hist(valoresGenerados,bins=k)
listaFrecAbsoluta=limpiarLista(lista)
print("\nLa frecuencia absoluta por intervalos es ",listaFrecAbsoluta)
valorChiCuadrado=creoValorChiCuadrado(listaFrecAbsoluta,n,k)
print("\nEl valor generado de ChiCuadrado es = ",valorChiCuadrado)
