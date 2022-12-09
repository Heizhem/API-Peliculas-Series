from fastapi import FastAPI
import pandas as pd
import numpy as np


app = FastAPI()
#cargo el dataframe
df = pd.read_csv('df_procesado.csv')

@app.get("/")
def read_root():
    return {"Hecho por": "Carlos Porcel"}


#Cantidad de películas y series (separado) por plataforma
@app.get('/get_count_plataform/{plataforma}')
async def get_count_plataform(plataforma):
    #dataframe que cuanta las peliculas agrupado por plataforma y por tipo
    cant_videos = df.groupby(['platform','type']).count()['title'].loc[plataforma]
    #diccionario con la cantidad de pelicula y series
    valores ={'peliculas': int(cant_videos[0]),'series' : int(cant_videos[1])}
    return valores

#Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo
@app.get('/get_listedin/{genero}')
async def get_listedin(genero:str):
    #mascara que verifica si la pelicula es de ese genero
    mask=df['listed_in'].str.contains(",\s*{0}\s*,|^{0}\s*,|,\s*{0}$|^{0}$".format(genero),regex=True)# verifica genro esta en el comienza, termina o esta en medio de cada valor de listed_in 
    #cuenta la cantidad de peliculas con ese genero agrupado por plataforma, luego lo ordena de forma ecendente
    cants = df[mask].groupby(['platform']).count()['title'].sort_values()
    #mayor numero de peliculas con ese genro
    cantidad = int(cants.max())
    #plataforma con que con el mayor cantidad de ese genero
    plataforma = cants.loc[cants == cantidad].index[0]

    return {'plataforma':plataforma,'cantidad':cantidad}



#Máxima duración según tipo de film (película/serie), por plataforma y por año
@app.get("/get_max_duration/{anio}&{plataforma}&{tipo}")
async def get_max_duration(anio:int,plataforma:str,tipo:str):
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
    
    actores=[]
    df_actores= df[(df['platform']== plataforma) & (df['release_year']== anio)&(df['cast']!= 'sin datos')]['cast']

    for elem in df_actores:
        valores=elem.split(',')
        valores = map(lambda x: x.lstrip().rstrip(),valores)
        actores+=valores
    

    resultado= {'actor': actores[0],'cantidad':0}

    for actor in actores:
        if df_actores[df_actores.str.contains(',\s*{0}\s*,|^{0}$|,\s*{0}$'.format(actor))].count() > resultado['cantidad']:
            resultado['actor'] = actor
            resultado['cantidad'] = df_actores[df_actores.str.contains(actor)].count()
    
    return {'actor' : str(resultado['actor']), 'aparicionse' : int(resultado['cantidad'])}