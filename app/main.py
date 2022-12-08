from fastapi import FastAPI
import pandas as pd
import numpy as np


app = FastAPI()
#cargo el dataframe
df = pd.read_csv('../Datasets\df_query.csv')

#modelos


#Cantidad de películas y series (separado) por plataforma
@app.get('/get_count_plataform/{plataforma}')
async def get_count_plataform(plataforma):
    cant_videos = df.groupby(['platform','type']).count()['title'].loc[plataforma]
    valores ={'peliculas': int(cant_videos[0]),'series' : int(cant_videos[1])}
    return valores

#Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo
@app.get('/get_listedin/{genero}')
async def get_listedin(genero:str):
    
    cants = df[df['listed_in'].str.contains(",\s*{0}\s*,|^{0}\s*,|,\s*{0}$|^{0}$".format(genero),regex=True)].groupby(['platform']).count()['title'].sort_values()
    cantidad = int(cants.max())
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