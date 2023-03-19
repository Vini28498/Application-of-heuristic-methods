import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import features
from geopy import distance

df=pd.read_excel('caminho-diretório-excel')

print(df)

print(df.iloc[1][3])

print(type(df.iloc[0][2]))

coord_mapa=[]
for n in range(len(df)):
    lista_aux=[]
    lista_aux.append(df.iloc[n][3])
    lista_aux.append(df.iloc[n][4])
    
    coord_mapa.append(lista_aux)
    
print(coord_mapa)
print(coord_mapa[0])

tt=distance.distance((df.iloc[0][3],df.iloc[0][4]),(df.iloc[1][3],df.iloc[1][4]))
print(tt)

mapa=folium.Map(location=[coord_mapa[0][0],coord_mapa[0][1]])

for n in range(len(df)):
    folium.Marker(location=coord_mapa[n],icon=folium.Icon(color='blue',icon_color='white',icon='info-sing')).add_to(mapa)
        
        
        
    #mapa.add_child(fg)
    
print(mapa)

tt=distance.distance((df.iloc[0][3],df.iloc[0][4]),(df.iloc[1][3],df.iloc[1][4]))

cidades=[i for i in range(len(df))]
print(cidades)

arcos=[(i,j) for i in cidades for j in cidades if i!=j]
print(arcos)

distancia={(i,j): distance.distance((df.iloc[i][3],df.iloc[i][4]),(df.iloc[j][3],df.iloc[j][4])).m 
                for i,j in arcos}

print(distancia)

cidade_inicio=0

def vizinho_proximo(cidade_inicio,cidades,distancia):
    NN=[cidade_inicio]
    arcos_ativos=[]
    n=len(cidades)
    
    while len(NN)<n:
        k=NN[-1]
        nn={(k,j): distancia[(k,j)] for j in cidades if k!=j and j not in NN}
        new=min(nn.items(),key=lambda x:x[1])    #ver
        NN.append(new[0][1])
        arcos_ativos.append(new[0])
    NN.append(cidade_inicio)    
    arcos_ativos.append((arcos_ativos[n-2][1],arcos_ativos[0][0]))
    return NN, arcos_ativos

NN,arcos_ativos =vizinho_proximo(cidade_inicio,cidades,distancia)
print(NN)

lista=NN

def distancia_total(lista,distancia):
    dist=0
    for n in range(len(lista)-1):
        i=lista[n]
        j=lista[n+1]
        dist=dist+distancia[(i,j)]
    
    return dist

dist=distancia_total(NN,distancia)
print(dist)

mapa=folium.Map(location=[coord_mapa[0][0],coord_mapa[0][1]])
for i,j in arcos_ativos:
    linea=folium.PolyLine(locations= [ [coord_mapa[i][0],coord_mapa[i][1]], [coord_mapa[j][0],coord_mapa[j][1]]],weight=5)
    
    mapa.add_child(linea)
    
print(mapa)

# Busca Local
def BL_2opt(NN,distancia):
    
    min_mudar=0
    
    
    for i in range(len(NN)-1):
        for j in range(i+2,len(NN)-1):
            
            custo_atual=distancia[(NN[i],NN[i+1])]+distancia[(NN[j],NN[j+1])]
            custo_novo=distancia[(NN[i],NN[j])]+distancia[(NN[i+1],NN[j+1])]
            mudar=custo_novo-custo_atual
            
            if mudar<min_mudar:
                min_mudar=mudar
                min_i=i
                min_j=j
                
    if min_mudar < 0:
        NN[min_i+1:min_j+1]=NN[min_i+1:min_j+1][::-1]
        
    return NN

NN=BL_2opt(NN,distancia)
print(NN)

def Arco_Ativo(NN):
    
    arcos_ativos01=[]
    for i in range(len(NN)-1):
        arcos_ativos01.append((NN[i],NN[i+1]))

    return arcos_ativos01 

arcos_ativos01=Arco_Ativo(NN)
print(arcos_ativos01)

mapa=folium.Map(location=[coord_mapa[0][0],coord_mapa[0][1]])

for i,j in arcos_ativos01:
    linea=folium.PolyLine(locations= [ [coord_mapa[i][0],coord_mapa[i][1]], [coord_mapa[j][0],coord_mapa[j][1]]],weight=5)
    
    mapa.add_child(linea)
    
print(mapa)

time_inicio=time.time()
sol=NN.copy()

cambio=1
count=0

while cambio !=0:
    
    count=count+1
    inicial=distancia_total(sol,distancia)
    sol=BL_2opt(sol,distancia).copy()
    final=distancia_total(sol,distancia)
    
    cambio=np.abs(final-inicial)
    
time_final=time.time()

print("Solução vizinho mais proximo ",NN)
print("Solução ",sol)
print("Distancia total Vizinho mais próximo ",distancia_total(NN,distancia))
print("Distancia total ",distancia_total(sol,distancia))
print("Tempo ", time_final-time_inicio)
print("Número de iterações ", count)

