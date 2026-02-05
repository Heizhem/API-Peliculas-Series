import pandas as pd
import numpy as np

def Extracion(ruta:str)-> dict[str, pd.DataFrame]:
    '''Carga los datos de las distintas plataformas de streaming y los devuelve en una lista de dataframes.
        df_a: df de amazon
        df_d: df de disney
        df_n: df de netflix
        df_h: df de hulu
    '''
    df_a: pd.DataFrame= pd.read_csv(ruta +'amazon_prime_titles.csv')
    df_d: pd.DataFrame= pd.read_csv(ruta + 'disney_plus_titles.csv')
    df_n: pd.DataFrame= pd.read_json(ruta + 'netflix_titles.json')
    df_h: pd.DataFrame= pd.read_csv(ruta + 'hulu_titles.csv')

    #lista con los df para iterar en los distintos procesos
    dfs:dict[str, pd.DataFrame] = {
        "amazon": df_a,
        "disney": df_d,
        "netflix": df_n,
        "hulu": df_h
    }

    return dfs
