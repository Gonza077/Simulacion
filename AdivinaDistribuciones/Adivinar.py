import pandas as pd
import matplotlib.pyplot as plt
import math
import stats

def cargoArchivos():
    datos1=pd.read_excel("Datos 01.xlsx",header=None)
    listaDatos1={col:datos1[col].dropna().tolist() for col in datos1.columns}[0]
    datos2=pd.read_excel("Datos 02.xlsx",header=None)
    listaDatos2={col:datos2[col].dropna().tolist() for col in datos2.columns}[0]
    datos3=pd.read_excel("Datos 03.xlsx",header=None)
    listaDatos3={col:datos3[col].dropna().tolist() for col in datos3.columns}[0]
    return listaDatos1,listaDatos2,listaDatos3

datos1,datos2,datos3=cargoArchivos()

print("\nDatos Muestra 1")
esperanzaDatos1 = stats.mean(datos1)
varianzaDatos1 = stats.variance(datos1)
lambdaa=esperanzaDatos1
print("La Esperanza Matematica de la muestra es = ",esperanzaDatos1)
print("La Varianza Matematica de la muestra es = ",varianzaDatos1)
print("El lambda de la muestra es = ",lambdaa)
plt.hist(datos1, edgecolor='black', linewidth=1,density=1,label=(f'Lambda = {round(lambdaa,0)}'))
y = [((math.exp(-6) * (6 ** x)) / (math.factorial(x))) for x in datos1]
plt.plot(datos1,y,'o')
plt.grid(True)
plt.ylim(0,0.25)
plt.text(9,0.15,"Amarrilo Dist.Poisson Lambda=6",color='black')
plt.legend(title="Parametros")
plt.title("Datos Muestra 1 - Distribucion Poisson")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.show()

print("\nDatos Muestra 2")
esperanzaDatos2 = stats.mean(datos2)
varianzaDatos2= stats.variance(datos2)
alfa=(1/esperanzaDatos2)
print("La Esperanza Matematica de la muestra es = ",esperanzaDatos2)
print("La Varianza Matematica de la muestra es = ",varianzaDatos2)
print("El parametro alfa es = ",alfa)
y = [(1/12)*math.exp(-(1/12)*x) for x in datos2]
plt.plot(datos2, y,'.')
plt.text(20,0.05,"Azul Funcion Densidad alfa= 1/12")
plt.hist(datos2, edgecolor='black', linewidth=1,density=1,label=(f'Alfa={round(alfa,2)}'))
plt.grid(True)
plt.legend(title="Parametro")
plt.title("Datos Muestra 2 - Distribucion Exponencial")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.show()

print("\nDatos Muestra 3")
esperanzaDatos3=stats.mean(datos3)
varianzaDatos3=stats.variance(datos3)
p= (esperanzaDatos3-varianzaDatos3)/esperanzaDatos3
n=(esperanzaDatos3**2)/(esperanzaDatos3-varianzaDatos3)
print("La Esperanza Matematica de la muestra es = ",esperanzaDatos3)
print("La Varianza Matematica de la muestra es = ",varianzaDatos3)
print("El numero de muestras (n) = ",round(n,0))
print("La probabilidad del suceso (p) de la muestra es = ",p)

plt.hist(datos3, edgecolor='black', linewidth=1,density=1,label=(f'Prob. = {round(p,2)}  NumSucesos= {round(n,0)}'))
plt.grid(True)
plt.legend(title="Parametros")
plt.title("Datos Muestra 3- Distribucion Binomial")
plt.xlabel("Intervalos")
plt.ylabel("Frecuencia")
plt.show()


