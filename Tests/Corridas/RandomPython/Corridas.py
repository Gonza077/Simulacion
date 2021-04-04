import random
cant_valores = 10000
lista_numeros = []
lista_corridas = []
lista_cuenta_corridas = []
matriz_A=[ [0,0,0,0,0,0,0],
    [0,4529.4, 9044.9, 13568, 18091, 22615, 27892],
    [0,9044.9, 18097, 27139, 36187, 45234, 55789],
    [0,13568, 27139, 40721, 54281, 67852, 83685],
    [0,18091, 36187, 54281, 72414, 90470, 111580],
    [0,22615, 45234, 67852, 90470, 113262, 139476],
    [0,27892, 55789,  83685,111580, 139476, 172860]]
matriz_B=  [0,1/6, 5/24, 11/120, 19/720, 29/5040, 1/840]

valorR=[0,0,0,0,0,0,0]
valorA=random.random()
valorJ=1
for i in range(2,cant_valores):
    valorB=random.random()
    if (valorA>valorB):
        valorJ=min(valorJ,6)
        valorR[valorJ]=valorR[valorJ]+1
        valorJ=1
    else:
        valorJ=valorJ+1
    valorA=valorB

valorJ = min(valorJ,6)
valorR[valorJ]=valorR[valorJ]+1
valorChiCuadrado=0

for i in range(1,7):
    for j in range(1,7):
        valorChiCuadrado+=(matriz_A[i][j])*(valorR[i]-cant_valores*matriz_B[i])*(valorR[j]-cant_valores*matriz_B[j])/cant_valores
for i in range(1,7):
    print("Cantidad de corridas de longitud ", i, " = ",valorR[i])

print("\n")
print("El valor Chi-Cuadrado generado es ",valorChiCuadrado)










