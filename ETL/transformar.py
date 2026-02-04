from carga import cargar_datos
import pandas as pd
import numpy as np

dfs = cargar_datos('../Datos/raw') # [amazon, disney, netflix, hulu]

def arreglar_formato():
    # La columna 'cast' tiene Dtype float64, cuando deberia ser object.
    # Además que no tiene datos por lo que cambaire lso ceros a 'Sin datos'

    df_h = dfs[3]
    df_h['cast'] = df_h['cast'].astype('object')
    df_h['cast'] = df_h['cast'].fillna('Sin datos')

    
    return

def normalizar_show_id():
    # normalizo la columna 'show_id' para las distintas plataformas
    letras = ['a','d','n','h']
    #itera sobre los df en dfs y agrega la letra corespondiente a la plataforma usando el index de dfs.
    for i,df in enumerate(dfs):
        df['show_id'] = df['show_id'].map(lambda x: letras[i]+x[1:])

    return dfs



def transformar_datos():
    transformar_datos_hulu()

    #funcion que deja solo la parte numerica de la columna 'duration'
