import random
import matplotlib.pyplot as plt
import stats
import numpy
import math

def generoValoresEmpiricos(matrizValores):
    x=random.random()
    for i in range(0,len(matrizValores)):
        if (matrizValores[i][3]>=x):
            x=matrizValores[i][0]
    return x

cantNum=1000
matrizValores=[[1,15,0.15,0.15],[2,15,0.15,0.3],[3,17,0.17,0.52],[4,12,0.12,0.64],[5,20,0.2,0.84],[6,16,0.16,1]]

for j in range(0,2):
    valores=[]
    for i in range(0,cantNum):
        valores.append(generoValoresEmpiricos(matrizValores))
    print("\nMuestra Nro ",j+1)
    print("La Esperanza de la muestra es =", stats.mean(valores))
    print("La Varianza es = ", stats.variance(valores))
    plt.hist(valores, edgecolor='black', linewidth=1, alpha=0.5)
    plt.show()


