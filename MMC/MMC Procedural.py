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
    global mediaDeDemoradosEnCola1
    global mediaDeNumeroEnCola1
    # Informe parte 1
    print("Simulacion finalizada al tiempo: ", tiempo)
    print("Personas que usaron el sistema", numeroDeUsuariosDemorados,"\n")
    print("Cantidad promedio de personas en cola Q(t) :", mediaDeDemoradosEnCola1)
    print("Valor promedio de usuario en  fila : ", mediaDeNumeroEnCola1)
    for i in range(0, len(servidores1)):
        print("Uso del servidor", i + 1, ":", areaServidores1[i] / tiempo)
    for i in range(0, len(servidores1)):
        creoGraficoFuncion(listaB1deT[i], i)

def buscoServidorMinimo():
    global servidores1
    tiempoMinimoServidor=math.exp(29)
    for i in range(0, len(servidores1)):
        if servidores1[i]< tiempoMinimoServidor and servidores1[i]!=0:
          tiempoMinimoServidor =servidores1[i]  # Esto contiene los valores en forma de lista por eso necesito en indice [j]# para podra acceder a dicho valor,tiempoMinimo Servidor cotiene el valor menor de los servidores distinto de 0
          #print("El valor minimo de los servidores1 es : ",tiempoMinimoServidor)    #Lo vaa hacer 4 veces por que recorre todos los servidores
    return tiempoMinimoServidor

def estadoServidor():
    global servidores1
    estadoServidores=[]
    for i in range(0,len(servidores1)):
        if servidores1[i]!=0:
            estadoServidores.append(1)
        else:
            estadoServidores.append(0)
    #print(estadoServidores)
    return estadoServidores

def actualizarAreas():
    global areaServidores1
    global tiempoUltimoEvento
    global areaNumeroDeUsuariosEnCola1
    estadoServidores1=estadoServidor()
    tiempoDesdeUltimoEvento = tiempo - tiempoUltimoEvento
    "Actualiza el area de los clientes en cola Q(t)"
    areaNumeroDeUsuariosEnCola1 = areaNumeroDeUsuariosEnCola1 + (numeroEnCola1 * tiempoDesdeUltimoEvento)
    "Actualiza el area del estado del servidor B(t)"
    #print(tiempoDesdeUltimoEvento)
    for i in range(0,len(servidores1)):
        areaServidores1[i] =areaServidores1[i]+ estadoServidores1[i] * tiempoDesdeUltimoEvento
    #print("El area de los servidores es", areaServidores1,"\n")

def arribo1():
    global numeroEnCola1
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global tiempoProximoEvento1
    global tasaArribo
    global tasaServicio
    global numeroMaxEnCola
    global servidores1
    global totalDeDemoras
    #Se setea el proximo arribo, por que solo hay un arribo por vez, es lo miso que MM1
    tiempoProximoEvento1[0]=tiempo+Expon(tasaArribo)
    #Se elije un servidor a ocupar para ese arribo
    servidorAOcupar=elegirServidor()
    if servidorAOcupar == -1:
        numeroEnCola1 += 1
        if numeroEnCola1 > numeroMaxEnCola:
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
        #servidoresLibres()
        tiempoProximoEvento1[1]=partida
        #print("los servidores se encuentran ",servidores1,"\n")

def partida1():
    global tiempoArribos
    global numeroEnCola1
    global tiempoProximoEvento
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    demora=0
    if numeroEnCola1==0:
        desocupoServidor()
        tiempoProximoEvento1[1]=math.exp(29)
    else:
        desocupoServidor()
        numeroEnCola1-=1
        demora = tiempo - tiempoArribos[0]
        totalDeDemoras+=demora
        numeroDeUsuariosDemorados+=1
        partida = tiempo + Expon(tasaServicio)
        servidorAOcupar=elegirServidor()
        asignoPartidaAServidor(partida, servidorAOcupar)
        #servidoresLibres()      #Esto chequea los servidores que estan libres en el momento
        tiempoProximoEvento1[1]=partida
        tiempoArribos.pop(0)
    calculoEstadisticos()

def calculoEstadisticos():
    global totalDeDemoras
    global numeroDeUsuariosDemorados
    global areaNumeroDeUsuariosEnCola1
    global tiempo
    global servidores1
    global mediaDeDemoradosEnCola1
    global listaCantDemorados1
    global listaQ1deT
    global listaB1deT
    global areaServidores1
    global mediaUsoDeServidores
    global mediaDeNumeroEnCola1
    valor=0
    for i in range(0,len(servidores1)):
           mediaUsoDeServidores[i]=areaServidores1[i]/tiempo
    for i in range(0,len(servidores1)):          #areaServidores y servidores1 van a tener siempre la misma longitud
        for j in range(0,len(areaServidores1)):
            if i==j:
                listaB1deT[i].append(mediaUsoDeServidores[j])   #Aca se guarda iteracion a iteracion la media de cada servidor
    mediaDeDemoradosEnCola1 = totalDeDemoras / numeroDeUsuariosDemorados
    listaQ1deT.append(mediaDeDemoradosEnCola1)
    mediaDeNumeroEnCola1 = areaNumeroDeUsuariosEnCola1 / tiempo
    listaCantDemorados1.append(mediaDeNumeroEnCola1)

def creoGraficoFuncion(lista,i):
    # SI VAS A HACER UNA LINEA DE PUNTOS, MODIFICAR EL CAMPO EN PLT.AXHLINE 0.778 CON EL VALOR AL QUE SE ACOTA
    plt.title('Uso del servidor '+str (i+1))
    plt.plot(lista)
    plt.xlabel("Usuarios")
    plt.ylabel("Porcentaje de uso")
    plt.axhline(0.0625, color='r', ls="dotted")  # Comando para linea horizontal constante
    #plt.ylim(0, 1)  # Limites para el eje Y
    #plt.xlim(0, cantidad)  # Limites para el eje X
    plt.show()

def elegirServidor():
    global servidores1
    lista=[]
    for i in range(0,len(servidores1)):
        if servidores1[i]==0:
            lista.append(i)   #Se guarda los indices de los servidores desocupados
    if len(lista)!=0:
        numServidorAOcupar = numpy.random.choice(lista)
    else:
        numServidorAOcupar=-1  #-1 para cuando los servidores estan llenos, condicion de control
    return (numServidorAOcupar)   #Devuelve el indice del servidor desocupado

def servidoresLibres():
    global servidores1
    listaServidoresLibres = []
    for i in range(0, len(servidores1)):
        if servidores1[i] == 0:
            listaServidoresLibres.append(i+1)  # Se guarda los indices de los servidores desocupados
    #print("Los servidores libres son:",listaServidoresLibres)

def asignoPartidaAServidor(partida,servidorAOcupar):
    global servidores1
    if (servidorAOcupar == 0):
        servidores1[0] = partida
    if (servidorAOcupar == 1):
        servidores1[1] = partida
    if (servidorAOcupar == 2):
        servidores1[2] = partida
    if (servidorAOcupar == 3):
        servidores1[3] = partida

def desocupoServidor():
    global servidores1
    global tiempo
    #print("Servidor antes",servidores)
    for i in range(0,len(servidores1)):
        if servidores1[i]== tiempo:
            servidores1[i]=0
            break
    #print("Servidor despues",servidores1)

def Expon(media):
    valor= (- media * math.log(random.random()))
    return(valor)


tiempo = 0
tiempoUltimoEvento=0
tiempoProximoEvento1 =[0,0]
tiempoProximoEvento2=[0,0]
areaNumeroDeUsuariosEnCola1=0
tipoProximoEvento=[]
numeroEnCola1=0
numeroEnCola2=0
numeroMaxEnCola=1000
tiempoArribos=[]
tasaServicio = 1/4
tasaArribo = 1
totalDeDemoras=0
listaQ1deT=[]
listaB1deT=[[],[],[],[]]    #Esto es asi por que va a ser una lista donde cada indice va a contener una lista con los datos de cada servidor
listaCantDemorados1=[]
listaQ2deT=[]
listaB2deT=[[],[],[],[]]
listaCantDemorados2=[]
listaUsuariosDemorados1=[0]
numeroDeUsuariosDemorados=0
servidores1=[0,0,0,0]
servidores2=[0,0]
areaServidores1=[0,0,0,0]
areaServidores2=[[0],[0]]
mediaDeDemoradosEnCola1=0
mediaDeNumeroEnCola1=0
mediaUsoDeServidores=[0,0,0,0]

tiempoProximoEvento1[0]= tiempo+Expon(tasaArribo)
#Condicion de corte // numeroDeUsuariosDemorados-1 <= numeroDeUsuariosRequeridos

while (numeroDeUsuariosDemorados<=9999):
    #Se actualiza el tiempo de la simulacion
    temporizador()
    #Actualizar areas esta dentro del temporizador
    if tipoProximoEvento==0:     # 0- ARRIBO // 1- PARTIDA
        arribo1()
    else:
        partida1()
informe1()
















