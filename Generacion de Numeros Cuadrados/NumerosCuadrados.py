listaNumeros=[[],[],[],[]]
Ui=[[],[],[],[]]
a=[5,4,5,4]
c=[3,3,4,4]
m=16

def verificoNumerosPrimos(numero):
    for i in range(2, numero):
        if (numero % i) == 0:
            return False
    return True

for j in range(0,4):
    listaNumeros[j].append(7)
    for i in range(0,19):
        listaNumeros[j].append(( a[j] * listaNumeros[j][i] +c[j])%m)
    for i in range(0,19):
        Ui[j].append(listaNumeros[j][i]/m)

    print("\nGenerador ",j+1 ,"\na =",a[j],", c = ",c[j],", m =",m)
    print("\nLos numeros generados son:\n",listaNumeros[j])
    print("\nLos Ui de cada numero son :\n",Ui[j])
    if (((a[j] - 1)%4)==0 and m%4!=0) or (((a[j] - 1)%4)!=0 and m%4==0):
        print("\nERROR\nEl valor (a-1)=",a[j]-1,"y m = ",m,"no son divisibles por 4 al a vez")
    if (verificoNumerosPrimos(c[j])==False):
        if (verificoNumerosPrimos(m)==False):
            print("\nERROR\nEl valor m =",m,"y c = ",c[j],"No son primos entre si")
    if (((a[j] - 1) % 2)==0 and m%2!=0) or (((a[j] - 1) % 2)!=0 and m%2==0):
              print("\nERROR\nEl valor m =",m,"y a = ",a[j]-1,"no son divisibles por 2 a la vez ")
    print("\n-----------------------------------------------------------------------------------------------------")