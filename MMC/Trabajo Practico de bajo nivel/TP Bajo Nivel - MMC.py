import math
import random
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------------------------
class Arribo():
    tasaArribo = 1 # Variables de clase

    def __init__(self, relojSimulacion):
        self.tiempoArribo = relojSimulacion + (- Arribo.tasaArribo * math.log(random.random()))
        self.nivel = 0
        self.tipo = "A"
        self.prioridad = False

    def generarPrioridad(self):
        if random.random() <= 0.05:
            self.prioridad = True

    def dameTuTiempo(self):
        return self.tiempoArribo

    def actualizaTuNivel(self,partida):
        self.tiempoArribo = partida.tiempoPartida
        self.nivel = partida.nivel+1

    def dameTuTipo(self):
        return self.tipo

# ----------------------------------------------------------------------------------------

class Partida():

    def __init__(self, relojSimulacion, tasaServicio,nivel):
        self.tiempoPartida = relojSimulacion + (- tasaServicio * math.log(random.random()))
        self.nivel = nivel
        self.tipo = "P"

    def dameTuTiempo(self):
        return self.tiempoPartida

    def dameTuTipo(self):
        return self.tipo

# ----------------------------------------------------------------------------------------

class Cola:
    numeroCola = 0

    def __init__(self):
        self.areaDeUsuariosEnCola = 0
        self.listaQdeT = []
        self.tiempoArribos = []
        self.totalDeDemoras=0
        self.numeroCola = Cola.numeroCola
        self.actualizoNumeroCola()

    def actualizoNumeroCola(self):
        Cola.numeroCola += 1

    def agregarArribo(self,arribo):
        if arribo.prioridad == True:
            self.tiempoArribos.insert(0,arribo)
        else:
            self.tiempoArribos.append(arribo)

    def actualizarArea(self, tiempoDesdeUltimoEvento):
        self.areaDeUsuariosEnCola = self.areaDeUsuariosEnCola + (len(self.tiempoArribos) * tiempoDesdeUltimoEvento)
        # len(tiempoArribo) reemplaza a la cantidad en cola

    def actualizarEstadistico(self, relojSimulacion):
        self.listaQdeT.append(self.areaDeUsuariosEnCola / relojSimulacion)

    def dameTusDatos(self, relojSimulacion):
        print("Valor promedio de personas Q(t) en cola", self.numeroCola +1, " : ",self.areaDeUsuariosEnCola / relojSimulacion)
        print("Demora promedio de una persona en la cola",self.numeroCola +1," . ",self.totalDeDemoras/Simu.cantDeDemorados)

    def dameValorFIFO(self):
        valor = self.tiempoArribos[0]
        self.tiempoArribos.pop(0)
        return valor  # Esto devuelvo el objeto arribo en la primer posicion

    def dameValorLIFO(self):
        valor = self.tiempoArribos[len(self.tiempoArribos) - 1]             #Tiene que tener ser n-1 por que se toma el 0 como arranque
        self.tiempoArribos.pop(len(self.tiempoArribos) - 1)
        return valor

    def dameTuLongitud(self):
        return len(self.tiempoArribos)

    def dameValorRandom(self):
        valor = random.choice(self.tiempoArribos)
        self.tiempoArribos.pop(self.tiempoArribos.index(valor))
        return valor

    def creoGrafico(self):
        plt.title('Grafico de gente en cola ' + str(self.numeroCola+1))
        plt.plot(self.listaQdeT)
        plt.xlabel("Usuarios")
        plt.ylabel("Porcentaje de uso")


# ----------------------------------------------------------------------------------------

class Servidor():
    numeroServidor = 0

    def __init__(self, valor):
        self.arribo = None
        self.tasaServicio = valor
        self.partida = Partida(math.exp(40),0,0)
        self.estado = 0
        self.areaBdeT = 0
        self.listaBdeT = []
        self.numeroServidor = Servidor.numeroServidor
        self.actualizoNumeroServidor()

    def actualizoNumeroServidor(self):
        Servidor.numeroServidor += 1

    def ocupoServidor(self, partida, arribo):
        self.partida = partida  # Partida va a ser un objeto
        self.estado = 1
        self.arribo = arribo

    def desocupoServidor(self):
        arribo=self.arribo
        self.arribo=None
        self.partida = Partida(math.exp(40),0,0) #Tiempo grande para que no se detecte
        self.estado = 0
        return arribo  # Retorno el arribo para pasarlo a otro nivel, siempre y cuando no sea el maximo

    def dameTusDatos(self, relojSimulacion):
        print("Uso del servidor ", self.numeroServidor+1, " : ", self.areaBdeT / relojSimulacion)

    def actualizarArea(self, tiempoDesdeUltimoEvento):
        self.areaBdeT = self.areaBdeT + (self.estado * tiempoDesdeUltimoEvento)

    def actualizarEstadistico(self, relojSimulacion):
        self.listaBdeT.append(self.areaBdeT / relojSimulacion)

    def creoGrafico(self,nivel):
        listaGrafico=[0.0625,0.25]
        plt.plot(self.listaBdeT)
        plt.xlabel("Usuarios")
        plt.ylabel("Porcentaje de uso")
        plt.axhline(listaGrafico[nivel], color='r', ls="dotted")  # Comando para linea horizontal constante

    def dameTuPartida(self):
        return self.partida.tiempoPartida
# ----------------------------------------------------------------------------------------
class Nivel:
    numero = 0
    cantMaxNiveles = 0

    def __init__(self, cantColas,cantServidores, tasaDeServicios):
        self.nivel = Nivel.numero
        self.actualizoNumeroNivel()
        self.colas = []
        self.servidores = []
        self.demoraEnNivel = 0
        for i in range(cantServidores):
            self.servidores.append(Servidor(tasaDeServicios[i]))
        for i in range(cantColas):
            self.colas.append(Cola())

    def actualizoNumeroNivel(self):
        Nivel.numero = Nivel.numero + 1

    def arribo(self,eventoArribo):
        #print("Genere arribo al nivel",self.nivel)
        indice = 0
        comparador = 0
        servidor = self.buscoServidor()
        genteEnCola = math.exp(99)
        listaAux=[]
        if servidor == -1:  # Todos los servidores deL nivel ocupados
            if eventoArribo.prioridad == False:
                for i in range(len(self.colas)):
                    comparador= self.colas[i].dameTuLongitud()
                    if comparador < genteEnCola:
                        genteEnCola = comparador
                        cola=self.colas[i]
                    if comparador==genteEnCola and self.nivel==1 :
                        listaAux.append(self.colas[0])
                        listaAux.append(self.colas[1])
                        cola=random.choice(listaAux)
                cola.agregarArribo(eventoArribo)
            else:
                cola = random.choice(self.colas)  # Elije al azar un objeto cola y inserta el arribo con prioridad
                cola.agregarArribo(eventoArribo)
        else:
            partida = Partida(Simu.relojSimulacion, servidor.tasaServicio, self.nivel)
            self.asignoPartidaAServidor(partida, servidor, eventoArribo)    #Ocurrio el arribo, por eso lo seteo en un tiempo grande

    def partida(self,eventoPartida):
        #print("Genere una partida en el nivel", self.nivel)
        arriboProxNivel= self.desocupoServidor(eventoPartida)        #Devuelvo el objetivo arribo que llego al servidor y lo seteo con el tiempo de partida
        listaAux = []
        if self.nivel==0:
            if self.colas[0].dameTuLongitud()!=0  :                            #Si las colas no estan vacias
                cola = self.colas[0]
                arriboEnCola = cola.dameValorFIFO()  # arribo va a tener un objeto Arribo
                demora = Simu.relojSimulacion - arriboEnCola.tiempoArribo
                self.colas[0].totalDeDemoras += demora
                servidor = self.buscoServidor()
                partida = Partida(Simu.relojSimulacion, servidor.tasaServicio,self.nivel)
                self.asignoPartidaAServidor(partida, servidor, arriboEnCola)  #Si las colas estan vacias
        elif self.nivel==1:
            if self.colas[0].dameTuLongitud() !=0 and self.servidores[0].estado==0:
                cola=self.colas[0]
                arriboEnCola=cola.dameValorFIFO()
                demora=Simu.relojSimulacion-arriboEnCola.tiempoArribo
                self.colas[0].totalDeDemoras+= demora
                servidor = self.servidores[0]
                partida = Partida(Simu.relojSimulacion, servidor.tasaServicio, self.nivel)
                self.asignoPartidaAServidor(partida, servidor, arriboEnCola)  # Si las colas estan vacias
                Simu.cantDeDemorados +=1
            elif self.colas[1].dameTuLongitud()!=0 and self.servidores[1].estado==0:
                cola = self.colas[1]
                arriboEnCola = cola.dameValorFIFO()
                demora = Simu.relojSimulacion - arriboEnCola.tiempoArribo
                self.colas[1].totalDeDemoras += demora
                servidor = self.servidores[1]
                partida = Partida(Simu.relojSimulacion, servidor.tasaServicio, self.nivel)
                Simu.cantDeDemorados += 1
                self.asignoPartidaAServidor(partida, servidor, arriboEnCola)  # Si las colas estan vacias
        self.actualizarEstadisticos()
        return arriboProxNivel

    def actualizarEstadisticos(self):

        for i in range(len(self.servidores)):
            self.servidores[i].actualizarEstadistico(Simu.relojSimulacion)
        for i in range(len(self.colas)):
            self.colas[i].actualizarEstadistico(Simu.relojSimulacion)

    def asignoPartidaAServidor(self, partida, servidor, arribo):
        for i in range(0, len(self.servidores)):
            if self.servidores[i] == servidor:
                self.servidores[i].ocupoServidor(partida, arribo)

    def desocupoServidor(self, partida):
        for i in range(len(self.servidores)):
            if self.servidores[i].partida == partida:
                arriboProxNivel = self.servidores[i].desocupoServidor()
                return arriboProxNivel

    def buscoServidor(self):
        listaAux = []
        servidor=0
        for i in range(len(self.servidores)):
            if self.servidores[i].estado == 0:
                listaAux.append(self.servidores[i])
        if len(listaAux) == 0:  # Verificar si la lista de servidores esta vacia
            servidor = -1
        else:
            servidor = random.choice(listaAux)
        return servidor

    def objetoMinimoEnNivel(self):
        listaAux = []
        for i in range(len(self.servidores)):
            listaAux.append(self.servidores[i].dameTuPartida()) # Se guardan los tiempos de la partida y el arribo

        minimoTiempo = min(listaAux)  # Minimo tiempo va a tener los tiempos, no los objetos, por eso despues vuelvo a buscarlo

        for i in range(len(self.servidores)):
            if minimoTiempo == self.servidores[i].dameTuPartida():
                    return self.servidores[i].partida           # Se retorna el objetoMinimo

    def actualizarAreas(self, relojSimulacion, tiempoUltimoEvento):
        tiempoDesdeUltimoEvento = relojSimulacion - tiempoUltimoEvento

        for i in range(len(self.servidores)):  # Esto es asi por las dos etapas con los servidores
            self.servidores[i].actualizarArea(tiempoDesdeUltimoEvento)

        for i in range(len(self.colas)):
            self.colas[i].actualizarArea(tiempoDesdeUltimoEvento)

    def dameTusDatos(self,relojSimulacion):

        for i in range(len(self.servidores)):
            self.servidores[i].dameTusDatos(relojSimulacion)

        for j in range(len(self.colas)):
            self.colas[j].dameTusDatos(relojSimulacion)

        for i in range(len(self.servidores)):
            plt.title("Grafico de los servidores del nivel " + str(self.nivel + 1))
            self.servidores[i].creoGrafico(self.nivel)
        plt.show()

        for i in range(len(self.colas)):
            plt.title("Grafico de las colas del nivel " + str(self.nivel + 1))
            self.colas[i].creoGrafico()
        plt.show()
# ----------------------------------------------------------------------------------------
class Simulador():

    def __init__(self):
        self.relojSimulacion = 0
        self.tiempoUltimoEvento = 0
        self.proximosEventos = [0, 0]
        self.niveles = []
        self.cantDeDemorados=0
        self.tipoProximoEvento = 0

    def temporizador(self):
        tiempoMinimoProximoEvento = math.exp(29)  # Lo seteo en un arribo muy grande para poder cambiar los valores
        # Esto devuelve el menor tiempo de los servidores, si estan todos desocupados los setea en infinito
        self.proximosEventos[1] = self.buscarTiempoMinimoEnNiveles()  # Esto devuelve un objeto con el menor tiempo o si no, uno demasiado grande
        for i in range(0, len(self.proximosEventos)):
            if self.proximosEventos[i].dameTuTiempo() < tiempoMinimoProximoEvento:
                tiempoMinimoProximoEvento = self.proximosEventos[i].dameTuTiempo()
                self.tipoProximoEvento = self.proximosEventos[i]  # Esto devuelve el objeto con el menor tiempo de ocurrir
        self.tiempoUltimoEvento = self.relojSimulacion  # Se guarda el tiempo del ultimo evento antes de avanzar el reloj
        self.relojSimulacion = tiempoMinimoProximoEvento
        self.actualizarAreas()

    def actualizarAreas(self):
        for i in range(len(self.niveles)):
            self.niveles[i].actualizarAreas(self.relojSimulacion, self.tiempoUltimoEvento)

    def buscarEventoEnNiveles(self):
        for i in range(len(self.niveles)):
            if self.tipoProximoEvento.tipo=="A":
                self.niveles[i].arribo(self.tipoProximoEvento)
                break
            else:
                arriboProxNivel=self.niveles[i].partida(self.tipoProximoEvento)
                if arriboProxNivel is not None and arriboProxNivel.nivel < Nivel.cantMaxNiveles -1:
                    arriboProxNivel.actualizaTuNivel(self.tipoProximoEvento)
                    self.niveles[arriboProxNivel.nivel].arribo(arriboProxNivel)
                    break

    def buscarTiempoMinimoEnNiveles(self):
        objetosMinimos = []  # Lo seteo en nulo para buscar el minimo servidor
        objetosNivel=[]
        for i in range(len(self.niveles)):  # Esto es asi por las dos etapas con los servidores
            objetosNivel.append(self.niveles[i].objetoMinimoEnNivel())           #Lista de objetos con tiempo minimo de cada nivel

        for i in range(len(objetosNivel)):
            objetosMinimos.append(objetosNivel[i].dameTuTiempo())           #Guardo los tiempos minimos de los objetos

        tiempoMinimo=min(objetosMinimos)                            #Encuentro el minimo

        for i in range(len(objetosNivel)):
            if tiempoMinimo== objetosNivel[i].dameTuTiempo():       #Comprao los tiempos y escuentro el objeto y lo devuelvo
                return objetosNivel[i]


    def inicializar(self):
        """
        cantNiveles = int(input("Ingrese la cantidad de niveles"))
        listaTasaServidores=[]      #Esto para cuando la tasa de los servidores sea distinta
        Nivel.cantMaxNiveles = cantNiveles
        for i in range(cantNiveles):
            print("Se ingresaran los datos del nivel ",i+1,"\n")
            cantColas=int(input("Ingrese cantidad de colas"))
            cantServidores=int(input("Ingrese cantidad de servidores"))
            for i in range(cantServidores):
               listaTasaServidores.append(float(input("Ingrese la tasa del servidor "+str(i+1)+" :")))
            self.niveles.append(Nivel(cantColas,cantServidores,listaTasaServidores))
        """
        Nivel.cantMaxNiveles = 2
        self.niveles.append(Nivel(1, 4, [0.25, 0.25, 0.25, 0.25]))
        self.niveles.append(Nivel(2, 2, [0.5, 0.5]))

    def generoArriboNivel0(self):
        arribo = Arribo(self.relojSimulacion)
        #arribo.generarPrioridad()
        self.proximosEventos[0]=arribo

    def informe(self):

        print("\n------------Datos del sistema ------------")
        for i in range(len(self.niveles)):
            print("Datos de los niveles ", i + 1)
            self.niveles[i].dameTusDatos(self.relojSimulacion)
            print("-------------------------------------------")


Simu = Simulador()
Simu.inicializar()

# Arribo.tasaArribo=float(input("Ingrese tasa de arribo : "))
# Partida.tasaServicio=float(input("Ingrese tasa de servicio : "))

Simu.proximosEventos[0] = Arribo(Simu.relojSimulacion)  # Reloj de simulacion en 0
Simu.proximosEventos[1]= Partida(math.exp(40),0,0)

while (Simu.relojSimulacion < 9999):  # Simu.relojSimulacion<5):
    # Se actualiza el tiempo de la simulacion
    #print(Simu.proximosEventos[0].dameTuTiempo(),Simu.proximosEventos[0].tipo,Simu.proximosEventos[0].nivel,"--",Simu.proximosEventos[1].dameTuTiempo(),Simu.proximosEventos[1].tipo,Simu.proximosEventos[1].nivel)
    Simu.temporizador()
    Simu.buscarEventoEnNiveles()
    Simu.generoArriboNivel0()  # Esto para generar siempre el arribo de una persona al nivel 0
    # Si bien el proximo evento puede ser un arribo o una partida de nivel n, hay que generar siempre un arribo al nivel inferior (0) SI O SI
Simu.informe()













