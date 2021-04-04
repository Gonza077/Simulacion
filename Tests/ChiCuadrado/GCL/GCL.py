import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats

def verificoNumerosPrimos(numero):
    for i in range(2, numero):
        if (numero % i) == 0:
            return False
    return True

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

def vericoParametros(a,c,m):

    if (((a - 1)%4)==0 and m%4!=0) or (((a - 1)%4)!=0 and m%4==0):
        print("\nERROR\nEl valor (a-1)=",a-1,"y m = ",m,"no son divisibles por 4 al a vez")
    if (verificoNumerosPrimos(c)==False and verificoNumerosPrimos(m)==False ):
            print("\nERROR\nEl valor m =",m,"y c = ",c,"No son primos entre si")
    if (((a - 1) % 2)==0 and m%2!=0) or (((a - 1) % 2)!=0 and m%2==0):
              print("\nERROR\nEl valor m =",m,"y (a-1) = ",a-1,"no son divisibles por 2 a la vez ")

#Programa Principal
z0=7
a=5
c=3
m=2000000
n=1000
listaValores=[]
vericoParametros(a,c,m)
listaValores.append(z0)

for i in range(0, n):
    listaValores.append((a * listaValores[i] + c) % m)
print(listaValores)
k=int(input("Ingrese la cantidad de intervalos : "))
lista=plt.hist(listaValores,bins=k)
listaFrecAbsoluta=limpiarLista(lista)
print("\nLa frecuencia absoluta por intervalos es ",listaFrecAbsoluta)
valorChiCuadrado=creoValorChiCuadrado(listaFrecAbsoluta,n,k)
print("\nEl valor generado de ChiCuadrado es = ",valorChiCuadrado)
print("El valor esperado es = ",scipy.stats.chisquare(listaFrecAbsoluta)[0])