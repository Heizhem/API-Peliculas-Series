from fastapi import FastAPI
import pandas as pd
import numpy as np
import re


app = FastAPI()
#cargo el dataframe
df = pd.read_csv('.\Datos\procesados\df_procesado.csv')

@app.get("/")
def read_root():
    return {"Hecho por": "Carlos Pórcel"}

# Devuelve las plataformas
@app.get("/plataformas")
def get_plataformas():
    return {"plataformas": df['platform'].unique().tolist()}

# Devuelve las años
@app.get("/años")
def get_años():
    años = df['release_year'].unique().tolist()
    años.sort()
    return {"años": años}

# Devuelve las generos y la cantidad total de génerosS
@app.get("/generos")
def get_generos():
    cant_por_genero = {}
    for fila in df['listed_in'].unique():
        for genero in fila.split(','):
            genero = genero.strip().lower()
            if genero not in cant_por_genero:
                cant_por_genero[genero] = 0
            cant_por_genero[genero] += 1
    total_generos = len(cant_por_genero)

    return {"generos": list(cant_por_genero.keys()),"cantidades_por_genero": total_generos}

#Cantidad de películas y series (separado) por plataforma
@app.get('/get_count_plataform/{plataforma}')
async def get_count_plataform(plataforma):

    plataforma = plataforma.lower().lstrip().rstrip()
    #dataframe que cuanta las peliculas agrupado por plataforma y por tipo
    cant_videos = df.groupby(['platform','type']).count()['title'].loc[plataforma]
    #diccionario con la cantidad de pelicula y series
    valores ={'peliculas': int(cant_videos[0]),'series' : int(cant_videos[1])}
    return valores

#Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo
@app.get('/get_listedin/{genero}')
async def get_listedin(genero:str):

    genero = genero.lower().strip()
    #mascara que verifica si la pelicula es de ese genero
    mask = df['listed_in'].str.contains(",\s*{0}\s*,|^{0}\s*,|,\s*{0}$|^{0}$".format(genero),regex=True)# verifica genero esta en el comienza, termina o esta en medio de cada valor de listed_in 
    #cuenta la cantidad de peliculas con ese genero agrupado por plataforma, luego lo ordena de forma decendente
    cants = df[mask].groupby(['platform']).count()['title'].sort_values()
    #mayor numero de peliculas con ese genero
    cantidad = int(cants.max())
    #plataforma con que con la mayor cantidad de ese genero
    plataforma = cants.loc[cants == cantidad].index[0]

    return {'plataforma':plataforma,'cantidad':cantidad}

@app.get('/get_listedin/{genero}')
async def get_listedin_v2(genero:str):

    genero = genero.lower().strip()
    #mascara que verifica si la pelicula es de ese genero
    mask = df['listed_in'].str.contains(rf'(^|,\s*){re.escape(genero)}(\s*,|$)', regex=True)
    #cuenta la cantidad de peliculas con ese genero agrupado por plataforma, luego lo ordena de forma decendente
    totales_por_plataforma = df[mask].groupby(['platform']).count()['title'].sort_values()
    #mayor numero de peliculas con ese genero
    cantidad = int(totales_por_plataforma.iloc[-1])
    #plataforma con que con la mayor cantidad de ese genero
    plataforma = totales_por_plataforma.index[-1]

    return {'plataforma':plataforma,'cantidad':cantidad}

#Máxima duración según tipo de film (película/serie), por plataforma y por año
@app.get("/get_max_duration/{anio}&{plataforma}&{tipo}")
async def get_max_duration(anio:int,plataforma:str,tipo:str):

    plataforma = plataforma.lower().lstrip().rstrip()
    tipo = tipo.lower().strip()
    
    if tipo == 'min':
        tipo = 'movie'
    else:
        tipo= 'tv show'
    df_pelis = df[(df.type == tipo) & (df.platform == plataforma) & (df.release_year == anio)]
    max_duracion = int(df_pelis['duration'].max())
    pelicula = df_pelis.loc[df_pelis['duration']==max_duracion]['title'].iloc[0]

    
    return {'titulo':pelicula,'duracion':max_duracion}

#Actor que más se repite según plataforma y año
@app.get('/get_actor/{plataforma}&{anio}')
def get_actor(plataforma:str, anio:int):
    plataforma = plataforma.lower().strip()
    actores = {}
    mask = (df['platform']== plataforma) & (df['release_year']== anio)&(df['cast']!= 'sin datos')
    df_actores = df[mask]
    for fila in df_actores['cast']:
        actores_fila = fila.split(',')
        for actor in actores_fila:
            actor = actor.lower().strip()
            if actor not in actores:
                actores[actor] = 0
            actores[actor] += 1

    actor_mas_repetido = max(actores, key=actores.get)
    cantidad_apariciones = actores[actor_mas_repetido]

    return {'actor': actor_mas_repetido, 'apariciones': cantidad_apariciones}