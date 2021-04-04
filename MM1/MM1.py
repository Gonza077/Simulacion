import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import math
import sys
import random

def temporizador():
    global tiempoUltimoEvento
    global tipoProximoEvento
    global tiempo
    tiempoMinimoProximoEvento= 1*math.exp(29)
    tipoProximoEvento=0
    for i in range(1,numeroDeEventos+1):
        if(tiempoProxEvento[i] < tiempoMinimoProximoEvento):
            tiempoMinimoProximoEvento = tiempoProxEvento[i]
            tipoProximoEvento=i
    if(tipoProximoEvento==0):
        print("Lista de eventos vacia al tiempo : ",tiempo)
        sys.exit() #Cierra el programa
    tiempoUltimoEvento = tiempo       #Esto lo puse aca para poder tener el tiempo del ultimo evento lo del pdf no funcionaba
    tiempo=tiempoMinimoProximoEvento

def actualizarAreas():
    global tiempoUltimoEvento
    global areaEstadoServidor
    global areaNumeroDeUsuariosEnCola
    tiempoDesdeUltimoEvento = tiempo - tiempoUltimoEvento
    #print(tiempoDesdeUltimoEvento)
    "Actualiza el area de los clientes en cola Q(t)"
    areaNumeroDeUsuariosEnCola = areaNumeroDeUsuariosEnCola + (numeroEnCola * tiempoDesdeUltimoEvento)
    #print(areaNumeroDeUsuariosEnCola)
    "Actualiza el area del estado del servidor B(t)"
    areaEstadoServidor= areaEstadoServidor + (estadoServidor * tiempoDesdeUltimoEvento)
    #print(areaEstadoServidor)

def arribo():
    global estadoServidor
    global numeroEnCola
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global tiempoProxEvento
    #Se setea el proximo arribo
    tiempoProxEvento[1]=tiempo+Expon(mediaTiempoArribo)
    #Se chequea el estado del servidor
    if estadoServidor == 1 :
        numeroEnCola+= 1
        if numeroEnCola>numeroMaxEnCola:
            print("Numero maximo exedido al tiempo : ",tiempo)
            sys.exit() #Esto cierra si el numero en cola supera al maximo permitido el programa nunca lo use
        tiempoArribos.append(tiempo)
    else :
        """Servidor libre, por lo tanto el arribo de usuarios/consumidores sera 0"""
        demora=0 #Variable local
        totalDeDemoras += demora
        """Se incrementa el numero de usuarios que usaron el sistema y se cambia el estado del
        servidor a ocupado"""
        numeroDeUsuariosDemorados += 1
        estadoServidor = 1
        """Se setea la partida del arribo(tiempor de servicio) """
        tiempoProxEvento[2]= tiempo + Expon(mediaTiempoServicio)

def partida():
    global estadoServidor
    global tiempoProxEvento
    global numeroEnCola
    global tiempoArribos
    global numeroDeUsuariosDemorados
    global totalDeDemoras
    global lista
    demora=0
    if numeroEnCola == 0 :
        estadoServidor = 0
        tiempoProxEvento[2]=1*math.exp(30)
    else:
        numeroEnCola -= 1
        demora= tiempo - tiempoArribos[0]
        totalDeDemoras+= demora
        #Se actualiza en numero de usuarios demorados y las partidas
        numeroDeUsuariosDemorados += 1
        tiempoProxEvento[2]=tiempo + Expon(mediaTiempoServicio)
        #Se mueven los usuarios en la cola(si los hay)
        tiempoArribos.pop(0)  #Esto funciona como el for

def Expon(media):
    valor= (- media * math.log(random.random()))
    return(valor)

def informe():
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global areaNumeroDeUsuariosEnCola
    global tiempo
    global areaEstadoServidor
    mediaDeDemoradosEnCola= totalDeDemoras / numeroDeUsuariosDemorados
    mediaDeNumeroEnCola= areaNumeroDeUsuariosEnCola / tiempo
    mediaUsoServidor= areaEstadoServidor / tiempo
    print("El uso medio del programa fue : ")
    print("Cantidad de usuarios que usaron el sistema : ",numeroDeUsuariosDemorados)
    print("Persona en cola al momento de finalizacion : ", numeroEnCola)
    print("Valor promedio de demora en cola : ",str(mediaDeDemoradosEnCola)+" [Seg]")
    print("Valor promedio de usuarios en cola Q(t) : ", mediaDeNumeroEnCola)
    print("Valor promedio de ocupacion del servidor B(t): ", mediaUsoServidor)
    print("Tiempo total de la ejecucion de la simulacion : ",tiempo)

#FUNCION inicializar
#Declaracion de variables
#Variables enteras en C
numeroMaxEnCola=100
numeroDeUsuariosRequeridos=0
numeroDeUsuariosDemorados=0
numeroEnCola=0
numeroEventos=2
numeroDeEventos=2
tipoProximoEvento=0
estadoServidor=0

#Variables flotantes en C
areaNumeroDeUsuariosEnCola=0
areaEstadoServidor=0
mediaEntreArribo=0
mediaEntreServicio=0
tiempo=0
tiempoArribos=[]
tiempoUltimoEvento=0
tiempoProxEvento=[0]*3
totalDeDemoras=0

#Main
print("A continuacion se cargaran los parametros de la distribucion y los usuarios requeridos")
mediaTiempoArribo = 1 / float(input("Ingrese el tiempo medio de arribos [Seg] : "))
mediaTiempoServicio = 1 /  float(input("Ingrese el tiempo medio de servico [Seg]: "))
numeroDeUsuariosRequeridos =int(input("Ingrese el numero de usuarios que van a usar el sistema : "))
print("\n")

tiempoProxEvento[1]= tiempo+Expon(mediaTiempoArribo)
tiempoProxEvento[2]=1*math.exp(30)

while(numeroDeUsuariosDemorados < numeroDeUsuariosRequeridos):
    #Se actualiza el tiempo de la simulacion
    temporizador()
    #Se actualiza las areas
    actualizarAreas()
    if (tipoProximoEvento == 1):
         arribo()
    elif (tipoProximoEvento == 2):
         partida()
informe()






