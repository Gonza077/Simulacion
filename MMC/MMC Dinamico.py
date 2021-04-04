import matplotlib.pyplot as plt
import numpy
import math
import sys
import random

def temporizador():
  global tiempoProximoEvento
  global tiempoUltimoEvento
  global tipoProximoEvento
  global tiempo
  tiempoMinimoServidor = 0
  tipoProximoEvento = 0
  tiempoMinimoServidor= buscoServidorMinimo()  #Esto devuelve el menor tiempo de los servidores, si estan todos desocupados los setea en infinito
  tiempoProximoEvento1[1]=tiempoMinimoServidor
  tiempoMinimoProximoEvento= 1*math.exp(29)
  for i in range(0,2):
    if(tiempoProximoEvento1[i] < tiempoMinimoProximoEvento):
        tiempoMinimoProximoEvento = tiempoProximoEvento1[i]
        tipoProximoEvento=i
  tiempoUltimoEvento = tiempo       #Se guarda el tiempo del ultimo evento antes de avanzar el reloj
  tiempo=tiempoMinimoProximoEvento
  #print("La lista de sucesos es : ",tiempoProximoEvento,"\n")
  #print("Tiempo ultimo evento",tiempoUltimoEvento)
  #print("El proximo evento es al tiempo ", tiempo)
  actualizarAreas()

def informe1():
    global mediaDeDemoradosEnCola
    global mediaDeNumeroEnCola
    global mediaUsoDeServidores
    # Informe parte 1
    print("Simulacion finalizada al tiempo: ", tiempo)
    print("Personas que usaron el sistema", numeroDeUsuariosDemorados,"\n")
    print("Cantidad promedio de personas en cola Q(t) :", mediaDeDemoradosEnCola)
    print("Valor promedio de usuario en sistema : ", mediaDeNumeroEnCola)
    for i in range(0, len(servidores)):
        print("Uso del servidor", i + 1, ":", areaServidores[i] / tiempo)
    for i in range(0, len(servidores)):
        creoGraficoFuncionServidor(listaBdeT[i], i)
    #creoGraficoFuncion(listaQdeT,0)
    #creoGraficoFuncion(listaCantDemorados,0)

def buscoServidorMinimo():
    global servidores
    tiempoMinimoServidor=math.exp(29)
    for i in range(0, len(servidores)):
        if servidores[i]< tiempoMinimoServidor and servidores[i]!=0:
          tiempoMinimoServidor =servidores[i]  # Esto contiene los valores en forma de lista por eso necesito en indice [j]# para podra acceder a dicho valor,tiempoMinimo Servidor cotiene el valor menor de los servidores distinto de 0
          #print("El valor minimo de los servidores1 es : ",tiempoMinimoServidor)    #Lo vaa hacer 4 veces por que recorre todos los servidores
    return tiempoMinimoServidor

def estadoServidor():
    global servidores
    estadoServidores=[]
    for i in range(0,len(servidores)):
        if servidores[i]!=0:
            estadoServidores.append(1)
        else:
            estadoServidores.append(0)
    #print(estadoServidores)
    return estadoServidores

def actualizarAreas():
    global areaServidores
    global tiempoUltimoEvento
    global areaNumeroDeUsuariosEnCola
    global servidores
    global numeroEnCola
    estadoServidores=estadoServidor()
    tiempoDesdeUltimoEvento = tiempo - tiempoUltimoEvento
    "Actualiza el area de los clientes en cola Q(t)"
    areaNumeroDeUsuariosEnCola = areaNumeroDeUsuariosEnCola + (numeroEnCola * tiempoDesdeUltimoEvento)
    "Actualiza el area del estado del servidor B(t)"
    #print(tiempoDesdeUltimoEvento)
    for i in range(0,len(servidores)):
        areaServidores[i] =areaServidores[i]+ estadoServidores[i] * tiempoDesdeUltimoEvento
    #print("El area de los servidores es", areaServidores1,"\n")

def arribo():
    global numeroEnCola
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global tiempoProximoEvento1
    global tasaArribo
    global tasaServicio
    global numeroMaxEnCola
    global servidores
    global totalDeDemoras
    #Se setea el proximo arribo, por que solo hay un arribo por vez, es lo miso que MM1
    tiempoProximoEvento1[0]=tiempo+Expon(tasaArribo)
    #Se elije un servidor a ocupar para ese arribo
    servidorAOcupar=elegirServidor()
    if servidorAOcupar == -1:
        numeroEnCola += 1
        if numeroEnCola > numeroMaxEnCola:
            print("Numero maximo exedido al tiempo : ", tiempo)
            sys.exit()  # Esto cierra si el numero en cola supera al maximo permitido el programa nunca lo use
        tiempoArribos.append(tiempo)
        #print("Servidor ocupado, se mando al arribo a la cola")
        #print(tiempoArribos,"\n")
    else:
        """Servidor libre, por lo tanto el arribo de usuarios/consumidores sera 0"""
        demora = 0  # Variable local
        totalDeDemoras += demora
        """Se incrementa el numero de usuarios que usaron el sistema y se cambia el estado del servidor a ocupado"""
        numeroDeUsuariosDemorados += 1
        #print("El arribo ocupara el servidor :", servidorAOcupar+1) #Esto toma ls indices, como arrancan en 0, lo incremento en 1
        # Actualizo la lista de servidores desocupados (saco de la lista los servidores que se ocupan)
        #servidoresXArribos.append(servidorAOcupar)  # Agrego el servidor que ocupa el primer arribo
        """Esto genera la partida del arribo en el servidor X con el tiempo generado """
        partida = tiempo + Expon(tasaServicio)
        asignoPartidaAServidor(partida,servidorAOcupar)
        servidoresLibres()
        tiempoProximoEvento1[1]=partida
        #print("los servidores se encuentran ",servidores1,"\n")

def partida():
    global tiempoArribos
    global numeroEnCola1
    global tiempoProximoEvento
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global numeroEnCola
    demora=0
    if numeroEnCola == 0:
        desocupoServidor()
        tiempoProximoEvento1[1] = math.exp(29)
    else:
        desocupoServidor()
        numeroEnCola -= 1
        demora = tiempo - tiempoArribos[0]
        totalDeDemoras += demora
        numeroDeUsuariosDemorados += 1
        partida = tiempo + Expon(tasaServicio)
        servidorAOcupar = elegirServidor()
        asignoPartidaAServidor(partida, servidorAOcupar)
        #servidoresLibres()      #Esto chequea los servidores que estan libres en el momento
        tiempoProximoEvento1[1]=partida
        tiempoArribos.pop(0)
    calculoEstadisticos()

def calculoEstadisticos():
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global areaNumeroDeUsuariosEnCola
    global tiempo
    global servidores
    global mediaDeNumeroEnCola
    global mediaDeDemoradosEnCola
    global listaCantDemorados
    global listaQdeT
    global listaBdeT
    global areaServidores
    global mediaUsoDeServidores
    global mediaDeNumeroEnCola
    valores=[]
    for i in range(0,len(servidores)):
           mediaUsoDeServidores[i]=areaServidores[i]/tiempo
    for i in range(0, len(servidores)):  # areaServidores y servidores1 van a tener siempre la misma longitud
        for j in range(0, len(areaServidores)):
            if i == j:
                listaBdeT[i].append(mediaUsoDeServidores[j])  # Aca se guarda iteracion a iteracion la media de cada servidor
    mediaDeDemoradosEnCola= totalDeDemoras / numeroDeUsuariosDemorados
    listaQdeT.append(mediaDeDemoradosEnCola)
    mediaDeNumeroEnCola = areaNumeroDeUsuariosEnCola / tiempo
    listaCantDemorados.append(mediaDeNumeroEnCola)

def creoGraficoFuncionServidor(lista,i):
    plt.title('Uso del servidor '+str (i+1))
    plt.plot(lista)
    plt.xlabel("Usuarios")
    plt.ylabel("Porcentaje de uso")
    #plt.ylim(0, 1)  # Limites para el eje Y
    #plt.xlim(0, cantidad)  # Limites para el eje X
    plt.show()

def elegirServidor():
    global servidores
    lista=[]
    for i in range(0,len(servidores)):
        if servidores[i]==0:
            lista.append(i)   #Se guarda los indices de los servidores desocupados
    if len(lista)!=0:
        numServidorAOcupar = numpy.random.choice(lista)
    else:
        numServidorAOcupar=-1  #-1 para cuando los servidores estan llenos, condicion de control
    return (numServidorAOcupar)   #Devuelve el indice del servidor desocupado

def servidoresLibres():
    global servidores
    listaServidoresLibres = []
    for i in range(0, len(servidores)):
        if servidores[i] == 0:
            listaServidoresLibres.append(i+1)  # Se guarda los indices de los servidores desocupados
    #print("Los servidores libres son:",listaServidoresLibres)

def asignoPartidaAServidor(partida,servidorAOcupar):
    global servidores
    if (servidorAOcupar == 0):
        servidores[0] = partida
    if (servidorAOcupar == 1):
        servidores[1] = partida
    if (servidorAOcupar == 2):
        servidores[2] = partida
    if (servidorAOcupar == 3):
        servidores[3] = partida

def desocupoServidor():
    global servidores
    global tiempo
    #print("Servidor antes",servidores)
    for i in range(0,len(servidores)):
        if servidores[i]== tiempo:
            servidores[i]=0
            break
    #print("Servidor despues",servidores1)

def Expon(media):
    valor= (- media * math.log(random.random()))
    return(valor)


tiempo = 0
tiempoUltimoEvento=0
tiempoProximoEvento1 =[0,0]
tipoProximoEvento=[]
numeroEnCola=0
numeroMaxEnCola=1000
tiempoArribos=[]
tasaServicio = 0
tasaArribo = 0
totalDeDemoras=0
listaQdeT=[]
listaCantDemorados=[]
listaUsuariosDemorados=[0]
numeroDeUsuariosDemorados=0
mediaDeDemoradosEnCola=0
mediaDeNumeroEnCola=0
areaNumeroDeUsuariosEnCola=0


tiempoProximoEvento1[0]= tiempo+Expon(tasaArribo)   #Seteo el primer arribo para poder empezar la simulacion

cantServidores=int(input("Ingrese la cantidad de servidores :"))
tasaArribo=float(input("Ingrese la tasa de arribo :"))
tasaServicio=float(input("Ingrese la tasa de servicio :"))

#Se inicializan todas las variables del sistema
servidores=[0]*cantServidores
areaServidores=[0]*cantServidores
mediaUsoDeServidores=[0]*cantServidores
listaBdeT=[]
for i in range(0,cantServidores):    #Si lo defino de otra manera, se vuelve loco a la hora de guardar valores, asi funciona correctamente
    listaBdeT.append([])
#Termina la inicializacion y empieza la simulacion

while (numeroDeUsuariosDemorados<=9999):
    #Se actualiza el tiempo de la simulacion
    temporizador()
    #Actualizar areas esta dentro del temporizador
    if tipoProximoEvento==0:     # 0- ARRIBO // 1- PARTIDA
        arribo()
    else:
        partida()
informe1()
















