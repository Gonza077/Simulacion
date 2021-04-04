import math
import random
import numpy

#----------------------------------------------------------------------------------------------------------------------

class Servidor():
    numerante = 0             #variable de clase para dar numero consecutivo a los servidores cada vez que se instancia
    def __init__(self,mediaServicio):
        self.estado = False
        self.arribo = None
        self.tiempoDeUtilizacon = 0
        self.tiempoIngresoEvento = None
        self.tiempoPartida = None
        self.mediaServicio = mediaServicio
        self.numero = self.numerante
        Servidor.numerante = Servidor.numerante + 1

    def expon(self, media):
        valor = (-media * math.log(random.random()))
        return (valor)

    def ocuparServidor(self,tiempo,arribo):
        self.estado = True
        self.arribo = arribo
        self.tiempoIngresoEvento = tiempo
        self.tiempoPartida = self.expon(self.mediaServicio) + tiempo
        return (self.tiempoPartida,self.numero)                # REVISAR RETORNO

    def desocuparServidor(self):
        self.tiempoDeUtilizacon = self.tiempoDeUtilizacon + self.tiempoPartida - self.tiempoIngresoEvento
        self.estado = False
        arribo = self.arribo
        self.arribo = None
        self.tiempoPartida = None
        return arribo


    def calcularEstadisticos(self,tiempo):
        if self.estado == True:
            self.tiempoDeUtilizacon = self.tiempoDeUtilizacon + tiempo - self.tiempoIngresoEvento    #PROBAR(suma el tiempo que estucvo ocupado hasta que termino la simulacion)

        promedioUtilizacion = self.tiempoDeUtilizacon/tiempo
        return promedioUtilizacion
#----------------------------------------------------------------------------------------------------------------------

class ConjuntoServidores():
    def __init__(self,cant_servidores,media):
        self.servidores = []
        for i in range(cant_servidores):
            self.servidores.append(Servidor(media))
        #self.nivel = nivel
        #self.servidores_desocupados = self.servidores

    def servidoresDesocupados(self):
        desocupados = []
        for i in self.servidores:
            if(i.estado == False):
                desocupados.append(i.numero)
        return desocupados

    def ocuparServidor(self,tiempo,arribo):
        sd = self.servidoresDesocupados()
        if len(sd)!=0:
            num_serv = random.choice(sd)
            for i in range(len(self.servidores)):
                if (self.servidores[i].numero == num_serv):
                    tiempoPartida, numServidor = self.servidores[i].ocuparServidor(tiempo,arribo)
                    return (tiempoPartida , numServidor)
        else:
            raise Exception('que se yo hiciste cualquiera y no eligio un sorongo el servidor libre')


    def desocuparservidor(self,numero):
        for i in range(len(self.servidores)):
            if (self.servidores[i].numero == numero):
                arribo = self.servidores[i].desocuparServidor()
                return arribo

#----------------------------------------------------------------------------------------------------------------------
#
#class Cliente():        #por ahora no la necesito
#    numerante = 0
#    def __init__(self):
#        self.numero = Cliente.numerate
#        Cliente.numerante = Cliente.numerante + 1
#
#----------------------------------------------------------------------------------------------------------------------

class Evento:
    arribos = 1
    def __init__(self, tipo, tiempo, numeroServidor = None, conjuntoColaServidor = None, nivel = None):
        self.tipo = tipo
        self.tiempo = tiempo
        if tipo == 'a':
            self.numero = Evento.arribos
            Evento.arribos = Evento.arribos + 1
        if tipo == 'p':
            self.servidor = numeroServidor
            self.conjuntoColaServidor = conjuntoColaServidor
            self.nivel = nivel

#----------------------------------------------------------------------------------------------------------------------

class Cola():
    #demorados = 0
    #tiempoUltimoEvento = 0

    def __init__(self):
        self.demorados = 0
        self.tiempoUltimoEvento = 0
        self.clientesEnCola = []
        self.tiempoDeingreso = []
        self.areaQt = 0
        self.esperaTotal = 0
        self.esperaPromedio = None
        self.numeroPromedioEnCola = None


    def entrada(self,relojSimulacion,arribo):
        self.actualizarQt(relojSimulacion)
        self.clientesEnCola.append(arribo)
        self.tiempoDeingreso.append(relojSimulacion)            #tiempo de ingreso a cola

    def salidaFifo(self,relojSimulacion):
        self.demorados = self.demorados + 1
        periodo = relojSimulacion - self.tiempoDeingreso[0]
        self.esperaTotal = self.esperaTotal + periodo
        self.actualizarQt(relojSimulacion)
        cliente = self.clientesEnCola[0]
        self.clientesEnCola.pop(0)
        self.tiempoDeingreso.pop(0)
        return cliente

    def actualizarQt(self,relojSimulacion):
        periodoNClientes = relojSimulacion - self.tiempoUltimoEvento
        self.areaQt = self.areaQt + (len(self.clientesEnCola) * periodoNClientes)
        self.tiempoUltimoEvento = relojSimulacion


    def calcularEstadisticos(self,tiempo):
        self.esperaPromedio = self.esperaTotal / self.demorados
        self.numeroPromedioEnCola = self.areaQt / tiempo        #REVISAR

#----------------------------------------------------------------------------------------------------------------------

class ConjuntoColaServidores():
    numeroConjunto = 0
    def __init__(self,disciplina,cantServidores,mediaServicio):
        self.conjuntoServidores = ConjuntoServidores(cantServidores,mediaServicio)
        self.cola = Cola()
        self.disciplina = disciplina
        self.numero = ConjuntoColaServidores.numeroConjunto
        ConjuntoColaServidores.numeroConjunto += 1

    def entradaEvento(self,reloj,arribo):
        partida = None
        if (len(self.conjuntoServidores.servidoresDesocupados()) > 0):   #PUEDE ESTAR MAL EL IF(creo que no)
            self.cola.entrada(reloj,arribo)
            if self.disciplina == 'Fifo':
                self.cola.salidaFifo(reloj)
            elif self.disciplina == 'Lifo':
                self.cola.salidaLifo(reloj)
            elif self.disciplina == 'Random':
                self.cola.salidaRandom(reloj)
            tiempoPartida, numServidor = self.conjuntoServidores.ocuparServidor(reloj,arribo)
            return (tiempoPartida, numServidor, self.numero)
                                       # agrego la partida con el tiempo que ha calculado el servidor medianrte su tiempo de servicio
        else:
            self.cola.entrada(reloj,arribo)
            return None, None, None
    def salidaEvento(self,reloj, numeroServidor):
        arribo = self.conjuntoServidores.desocuparservidor(numeroServidor)
        if self.conjuntoServidores.servidoresDesocupados():
            if self.cola.clientesEnCola:
                if self.disciplina == 'Fifo':
                    a = self.cola.salidaFifo(reloj)
                elif self.disciplina == 'Lifo':
                    a = self.cola.salidaLifo(reloj)
                elif self.disciplina == 'Random':
                    a = self.cola.salidaRandom(reloj)
                tiempoPartida, numServidor = self.conjuntoServidores.ocuparServidor(reloj,a)
                return arribo, tiempoPartida, numeroServidor, self.numero
        return arribo, None, None, None

#----------------------------------------------------------------------------------------------------------------------

class Nivel():
    numeroNivel = 0
    def __init__(self,cantidadConjuntos,disciplina,cantServidores,mediaServicio):
        self.numero = Nivel.numeroNivel
        Nivel.numeroNivel += 1
        self.conjuntosColaServidor = []
        for i in range(cantidadConjuntos):
            c = ConjuntoColaServidores(disciplina,cantServidores,mediaServicio)
            self.conjuntosColaServidor.append(c)

    def entradaEvento(self,reloj,arribo):
        posicionesMenoresColas = []
        comparador = len(self.conjuntosColaServidor[0].cola.clientesEnCola)
        for i in range(len(self.conjuntosColaServidor)):
            cantidadEnCola = len(self.conjuntosColaServidor[i].cola.clientesEnCola)
            if cantidadEnCola == comparador:
                posicionesMenoresColas.append(i)
            if cantidadEnCola < comparador :
                comparador = cantidadEnCola
                posicionesMenoresColas = []
                posicionesMenoresColas.append(i)
        posicion = random.choice(posicionesMenoresColas)
        tiempoPartida, numServidor, numeroConjunto = self.conjuntosColaServidor[posicion].entradaEvento(reloj,arribo)
        return tiempoPartida, numServidor, numeroConjunto, self.numero

    def salidaEvento(self,reloj,numeroConjunto,numeroServidor):
        arribo = None
        for i in range(len(self.conjuntosColaServidor)):
            if (self.conjuntosColaServidor[i].numero == numeroConjunto):
                arribo, tiempoPartida, numServidor, numConj = self.conjuntosColaServidor[i].salidaEvento(reloj,numeroServidor)
                return arribo, tiempoPartida, numServidor, numConj, self.numero          #si son null los ultimos dos no se ocupo un servidor (la cola estaba vacia)
        raise ('algo salio mal (nivel, salidaEvento) ')
#----------------------------------------------------------------------------------------------------------------------

class Simulacion():
    def __init__(self,mediaArribo):
        self.mediaArribo = mediaArribo
        self.reloj = 0
        self.niveles = []
        self.listaEventos = []
        self.conjuntoNiveles = []
        self.conjuntoNiveles.append(Nivel(1,'Fifo',4,0.25))
        self.conjuntoNiveles.append(Nivel(2, 'Fifo',1, 0.5)) #el 2 ese esta mal
        self.serviciosCompletados = []
        self.pasados = 0
        self.aplicacion()



    def generarArribo(self):
        tiempo = self.reloj + self.expon(self.mediaArribo)
        e  = Evento('a',tiempo)
        return e

    def expon(self, media):
        valor = (-media * math.log(random.random()))
        return (valor)

    def agregarEventoLista(self,evento): #La lista de eventos ingresa el nuevo evento ordenado por tiempo (PRIMER EVENTO EN LISTA ES EL PROXIMO EVENTO)
        if not self.listaEventos:
            self.listaEventos.append(evento)
        else:
            long = len(self.listaEventos)
            for i in range(long):
                if ((self.listaEventos[i].tiempo) > (evento.tiempo)):
                    self.listaEventos.insert(i,evento)
                    break
                if i == (long-1):
                    self.listaEventos.append(evento)
                    break

    def manejarEntrada(self,nivel,arribo):
        tiempoPartida, numServidor, numeroConjunto, numeroNivel = self.conjuntoNiveles[nivel].entradaEvento(self.reloj,arribo)
        if tiempoPartida == None and numServidor == None and numeroConjunto == None:
            pass
        else:
            e = Evento('p', tiempoPartida, numeroServidor=numServidor, conjuntoColaServidor=numeroConjunto,
                       nivel=numeroNivel)
            self.agregarEventoLista(e)

    def manejarPartida(self):
        serv = self.listaEventos[0].servidor
        conj = self.listaEventos[0].conjuntoColaServidor
        niv = self.listaEventos[0].nivel
        if niv < (len(self.conjuntoNiveles) - 1):
            arribo, tiempoPartida, numServidor, numConjunto, numNivel = self.conjuntoNiveles[niv].salidaEvento(self.reloj,conj, serv)
            if tiempoPartida == None:
                self.manejarEntrada(niv + 1,arribo)
            else:
                self.manejarEntrada(niv + 1,arribo)
                e = Evento('p',tiempoPartida, numeroServidor=numServidor, conjuntoColaServidor=numConjunto,nivel=numNivel)
                self.agregarEventoLista(e)
            self.pasados = self.pasados + 1

        elif niv == (len(self.conjuntoNiveles) - 1):
            arribo, tiempoPartida, numServidor, numConjunto, numNivel = self.conjuntoNiveles[niv].salidaEvento(self.reloj,conj, serv)
            if tiempoPartida == None:
               self.serviciosCompletados.append(arribo)
            else:
                e = Evento('p', tiempoPartida, numeroServidor=numServidor, conjuntoColaServidor=numConjunto,
                           nivel=numNivel)
                self.agregarEventoLista(e)
                self.serviciosCompletados.append(arribo)



    def aplicacion(self):
        a0 = self.generarArribo()
        self.agregarEventoLista(a0)
        while (Evento.arribos <= 10000):                       # BUCLE DE PRUEBAS CON 10000 CLIENTES ARRIBANDO
            self.reloj = self.listaEventos[0].tiempo

            if self.listaEventos[0].tipo == 'a':                    #veo si es un arribo el prox evento
                self.manejarEntrada(0,self.listaEventos[0])
                a = self.generarArribo()
                self.agregarEventoLista(a)

            else :                                                   #Si no es arribo entonces es partida
                self.manejarPartida()
            #print()
            self.listaEventos.pop(0)   ##VER ESTE POP




#--------------------------------------------------'CORRER APP'--------------------------------------------------------

def app():
    s1 = Simulacion(1)
    print('reloj ', s1.reloj)
    s1.conjuntoNiveles[0].conjuntosColaServidor[0].cola.calcularEstadisticos(s1.reloj)
    print('Espera promedio en cola: 0 ',s1.conjuntoNiveles[0].conjuntosColaServidor[0].cola.esperaPromedio)
    print('Numero promedio en cola: 0 ',s1.conjuntoNiveles[0].conjuntosColaServidor[0].cola.numeroPromedioEnCola)
    print()
    for i in range(4):
        print('porcentaje de utilizacion servidor ',s1.conjuntoNiveles[0].conjuntosColaServidor[0].conjuntoServidores.servidores[i].numero,
              ' = ',s1.conjuntoNiveles[0].conjuntosColaServidor[0].conjuntoServidores.servidores[i].calcularEstadisticos(s1.reloj))

    print()
    print('------------Nivel 2-----------')
    print()
    s1.conjuntoNiveles[1].conjuntosColaServidor[0].cola.calcularEstadisticos(s1.reloj)
    s1.conjuntoNiveles[1].conjuntosColaServidor[1].cola.calcularEstadisticos(s1.reloj)
    print('Espera promedio en cola: 1 ', s1.conjuntoNiveles[1].conjuntosColaServidor[0].cola.esperaPromedio)
    print('Numero promedio en cola: 1 ', s1.conjuntoNiveles[1].conjuntosColaServidor[0].cola.numeroPromedioEnCola)
    print('Espera promedio en cola: 2 ', s1.conjuntoNiveles[1].conjuntosColaServidor[1].cola.esperaPromedio)
    print('Numero promedio en cola: 2 ', s1.conjuntoNiveles[1].conjuntosColaServidor[1].cola.numeroPromedioEnCola)
    print()
    #for i in range(2):
    print('porcentaje de utilizacion servidor ',
          s1.conjuntoNiveles[1].conjuntosColaServidor[0].conjuntoServidores.servidores[0].numero,
          ' = ',
          s1.conjuntoNiveles[1].conjuntosColaServidor[0].conjuntoServidores.servidores[0].calcularEstadisticos(
              s1.reloj))
    print('porcentaje de utilizacion servidor ',
          s1.conjuntoNiveles[1].conjuntosColaServidor[1].conjuntoServidores.servidores[0].numero,
          ' = ',
          s1.conjuntoNiveles[1].conjuntosColaServidor[1].conjuntoServidores.servidores[0].calcularEstadisticos(
              s1.reloj))
    print('------------------')
    print(s1.pasados)
    print(len(s1.serviciosCompletados))
    #print(s1.cola1.demorados)


if __name__ == "__main__":
    app()
