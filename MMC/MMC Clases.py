import math
import random
import matplotlib.pyplot as plt
import sys
#----------------------------------------------------------------------------------------
class Arribo():
    tasaArribo=1    #Variables de clase

    def __init__(self,relojSimulacion):
        self.tiempoArribo = relojSimulacion + (- Arribo.tasaArribo * math.log(random.random()))

    def dameTuTiempo(self):
        return(self.tiempoArribo)

    def dameTuTipo(self):
        return("A")

#----------------------------------------------------------------------------------------

class Partida():

    tasaServicio=0.25   #Variables de clase

    def __init__(self,relojSimulacion):
        self.tiempoPartida= relojSimulacion + ( - Partida.tasaServicio * math.log(random.random()))

    def dameTuTiempo(self):
        return (self.tiempoPartida)

    def dameTuTipo(self):
        return("P")

#----------------------------------------------------------------------------------------

class Cola:
    numeroCola=0
    def __init__(self):
        self.areaDeUsuariosEnCola = 0
        self.listaCantDeUsuariosDemorados=[]
        self.tiempoArribos = []
        self.numeroCola=Cola.numeroCola+1
        Cola.numeroCola += 1
        self.totalDeDemoras=0
        self.cantDeDemorados=0

    def actualizoArea(self, tiempoDesdeUltimoEvento):
        self.areaDeUsuariosEnCola  = self.areaDeUsuariosEnCola + (len(self.tiempoArribos) * tiempoDesdeUltimoEvento)
        #len(tiempoArribo) reemplaza a la cantidad en cola

    def actualizoEstadistico(self,relojSimulacion):
        self.listaCantDeUsuariosDemorados.append(self.areaDeUsuariosEnCola / relojSimulacion)

    def dameTusDatos(self,relojSimulacion):
        print("Valor promedio de personas en cola",self.numeroCola ," : ",self.areaDeUsuariosEnCola / relojSimulacion)

    def dameValorFIFO(self):
        valor = self.tiempoArribos[0].tiempoArribo
        self.tiempoArribos.pop(0)
        return (valor)   #Esto devuelvo el objeto arribo en la primer posicion

    def dameValorLIFO(self):
        valor=self.tiempoArribos[len(self.tiempoArribos)]
        self.tiempoArribos.pop(len(self.tiempoArribos))
        return valor

    def dameValorRandom(self):
        valor=random.choice(self.tiempoArribos)
        self.tiempoArribos.pop(valor)
        return valor
#----------------------------------------------------------------------------------------

class Servidor():
    numeroServidor=0

    def __init__(self):
        self.partida=None
        self.estado=0
        self.areaBdeT=0
        self.listaBdeT=[]
        self.numeroServidor= Servidor.numeroServidor+1
        Servidor.numeroServidor += 1

    def ocupoServidor(self,partida):
        self.partida= partida
        self.estado=1

    def desocupoServidor(self):
        self.partida=None
        self.estado=0

    def dameTusDatos(self,relojSimulacion):
        print("Uso del servidor ", self.numeroServidor, " : ", self.areaBdeT / relojSimulacion)

    def actualizoArea(self,tiempoDesdeUltimoEvento):
        self.areaBdeT= self.areaBdeT+ (self.estado * tiempoDesdeUltimoEvento)

    def actualizoEstadistico(self,relojSimulacion):
        self.listaBdeT.append(self.areaBdeT / relojSimulacion)

    def creoGrafico(self):
        plt.title('Uso del servidor ' + str(self.numeroServidor))
        plt.plot(self.listaBdeT)
        plt.xlabel("Usuarios")
        plt.ylabel("Porcentaje de uso")
        plt.axhline(0.0625, color='r', ls="dotted")  # Comando para linea horizontal constante
        plt.show()

#----------------------------------------------------------------------------------------

class Simulador:

    def __init__(self):
        self.relojSimulacion=0
        self.tiempoUltimoEvento=0
        self.areaQ1deT=0
        self.servidores=[]
        self.colas=[]
        self.numeroDeDemorados=0
        self.totalDeDemoras=0
        self.proximoEventos=[0]*2
        self.tipoProximoEvento=0
        self.cantDeDemorados = 1
        self.mediaDeDemoradosEnCola=0
        self.listaQdeT=[]
        self.cont=0

    def temporizador(self):

        tiempoMinimoProximoEvento=Partida(math.exp(29))         #Lo seteo en un arribo/partida muy grande para poder cambiar los valores
        servidorMinimo=self.buscoServidorMinimo()               #Esto devuelve un objeto servidor
        listaAux=[]
        if servidorMinimo is None:
            self.proximoEventos[1]=Partida(math.exp(29))        #Lo seteo en un arribo muy grande para poder cambiar los valores
        else:
            self.proximoEventos[1]= servidorMinimo.partida      #Aca le asigno el objeto partida que tiene el servidor

        for i in range(0,len(self.proximoEventos)):
            if self.proximoEventos[i].dameTuTiempo() < tiempoMinimoProximoEvento.dameTuTiempo() :
                tiempoMinimoProximoEvento = self.proximoEventos[i]
                self.tipoProximoEvento = self.proximoEventos[i].dameTuTipo()

        self.tiempoUltimoEvento = self.relojSimulacion          #Se guarda el tiempo del ultimo evento antes de avanzar el reloj
        self.relojSimulacion = tiempoMinimoProximoEvento.dameTuTiempo()
        #print("La lista de sucesos es : ",self.proximoEventos,"\n")
        #print("Tiempo ultimo evento",self.tiempoUltimoEvento)
        #print("El proximo evento es al tiempo ", self.relojSimulacion)
        self.actualizarAreas()

    def actualizarAreas(self):

        tiempoDesdeUltimoEvento = self.relojSimulacion - self.tiempoUltimoEvento
        for i in range(len(self.servidores)):  # Esto es asi por las dos etapas con los servidores
            for j in range(len(self.servidores[i])):
                self.servidores[i][j].actualizoArea(tiempoDesdeUltimoEvento)

        for i in range(len(self.colas)):
            for j in range(len(self.colas[i])):
                self.colas[i][j].actualizoArea(tiempoDesdeUltimoEvento)

    def arribo(self):
        arriboViejo=self.proximoEventos[0]  #Para poder guardar el arribo que voy a reemplazar
        self.proximoEventos[0]= Arribo(self.relojSimulacion)
        numServidorAOcupar=0
        numServidorAOcupar=self.buscoServidor()
        #print("Servidor elegido",numServidorAOcupar)
        if numServidorAOcupar == -1:    #Todos los servidores de nivel 0 ocupados
            self.colas[0][0].tiempoArribos.append(arriboViejo)
            self.cont+=1
        else:
            demora=0
            self.totalDeDemoras+= demora
            self.cantDeDemorados+=1
            partida=Partida(self.relojSimulacion)
            self.asignoPartidaAServidor(partida,numServidorAOcupar)
            self.proximoEventos[1]=partida
            #self.servidoresLibres()

    def partida(self):
        demora=0
        self.desocupoServidor(self.proximoEventos[1])
        if len(self.colas[0][0].tiempoArribos) == 0:
            #self.desocupoServidor(self.proximoEventos[1])    #Esto tiene el objeto partida
            self.proximoEventos[1]=Partida(math.exp(29))
        else:
            #self.desocupoServidor(self.proximoEventos[1])
            demora= self.relojSimulacion - self.colas[0][0].dameValorFIFO()
            self.totalDeDemoras+= demora
            self.cantDeDemorados+=1
            partida=Partida(self.relojSimulacion)
            self.proximoEventos[1] = partida
            numServidorAOcupar = self.buscoServidor()
            self.asignoPartidaAServidor(partida, numServidorAOcupar)
            #La salida fifo ya esta hecha en la cola
        self.calculoEstadisticos()

    def calculoEstadisticos(self):

        self.mediaDeDemoradosEnCola=self.totalDeDemoras/self.cantDeDemorados
        self.listaQdeT.append(self.mediaDeDemoradosEnCola)

        for i in range(len(self.servidores)):
            for j in range(len(self.servidores[i])):
                self.servidores[i][j].actualizoEstadistico(self.relojSimulacion)

        for i in range(len(self.colas)):
            for j in range(len(self.colas[i])):
                self.colas[i][j].actualizoEstadistico(self.relojSimulacion)

    def asignoPartidaAServidor(self,partida,servidorAOcupar):
        for i in range(0,len(self.servidores[0])):
            if self.servidores[0][i].numeroServidor == servidorAOcupar:
                self.servidores[0][i].ocupoServidor(partida)

    def desocupoServidor(self,partida):
        for i in range(len(self.servidores[0])):
            if self.servidores[0][i].partida==partida:     #Aca se comparan objetos
                self.servidores[0][i].desocupoServidor()

    def buscoServidor(self):
        lista= []
        numServidor = -1
        for i in range(len(self.servidores[0])):
          if( self.servidores[0][i].estado != 1):
              lista.append(self.servidores[0][i].numeroServidor)
        if len(lista)!=0:
            numServidor=random.choice(lista)
        return numServidor

    def buscoServidorMinimo(self):
      tiempoMinimoServidor=math.exp(29)
      servidorMinimo=None                               #Lo seteo en nulo para buscar el minimo servidor
      for i in range(len(self.servidores)):             #Esto es asi por las dos etapas con los servidores
        for j in range(len(self.servidores[i])):
          if(self.servidores[i][j].partida is not None):                              #Esto es para saber si es un objeto,y asi evitar pasar con un servidorMinimo en None
            if self.servidores[i][j].partida.tiempoPartida < tiempoMinimoServidor :   #Verifico que el tiempo de partida sea menor al del servidor minimo
                servidorMinimo = self.servidores[i][j]                                #Esto devuelve un objeto servidor con el menor tiempo
      return servidorMinimo

    def inicializar(self):
        cantServidores1=4
        cantServidores2=2
        servidores1=[]
        servidores2=[]
        cola1=[]
        cola2=[]
        for i in range(cantServidores1):
            servidores1.append(Servidor())
            #Servidores del nivel 1
        for i in range(cantServidores2):
            servidores2.append(Servidor())
            #Servidores del nivel 2
        self.servidores.append(servidores1)
        self.servidores.append(servidores2)
        #print(self.servidores)
        cola1.append(Cola())                   #Cola en el nivel 1
        for i in range(2):
            cola2.append(Cola())               #Cola en el nivel 2
        self.colas.append(cola1)
        self.colas.append(cola2)
        #print(self.colas)

    def informe(self):

        print("\n------------Datos del sistema ------------")
        for i in range(len(self.servidores)):
            print("Datos de los servidores nivel ",i+1)
            for j in range(len(self.servidores[i])):
             self.servidores[i][j].dameTusDatos(self.relojSimulacion)
            print("-------------------------------------------")

        for i in range(len(self.colas)):
            print("Datos de las colas de nivel ", i + 1)
            for j in range(len(self.colas[i])):
                self.colas[i][j].dameTusDatos(self.relojSimulacion)
            print("-------------------------------------------")

        print("Demora promedio de una persona Q(t)  ",self.mediaDeDemoradosEnCola)
        print("-------------------------------------------")
        #for i in range(len(Simu.servidores[0])):
        #    self.servidores[0][i].creoGrafico()

#----------------------------------------------------------------------------------------

Simu = Simulador()
Simu.inicializar()

#Arribo.tasaArribo=float(input("Ingrese tasa de arribo : "))
#Partida.tasaServicio=float(input("Ingrese tasa de servicio : "))

Simu.proximoEventos[0]= Arribo(Simu.relojSimulacion)   #Reloj de simulacion en 0
Simu.proximoEventos[1]=Partida(math.exp(29))


while(Simu.cantDeDemorados<9999):#Simu.relojSimulacion<5):
    # Se actualiza el tiempo de la simulacion
    Simu.temporizador()
    # Actualizar areas esta dentro del temporizador
    if Simu.tipoProximoEvento == "A":
        Simu.arribo()
    else:
        Simu.partida()
Simu.informe()








