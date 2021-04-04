import random
import matplotlib.pyplot as plt

n = 10000
listaFrecAbsoluta=[[],[]]

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
k = int(input("Ingrese la cantidad de intervalos : "))
for j in range(0,2):
    valoresGenerados=[]
    for i in range (0,n):
        valoresGenerados.append(creoValoresRandom())
    lista=plt.hist(valoresGenerados,bins=k)
    listaFrecAbsoluta[j]=limpiarLista(lista)
for j in range(0,2):
    print("\nLa frecuencia absoluta de la fila ",j+1," es : ",listaFrecAbsoluta[j])


