import pandas as pd
import numpy as np


def limpiar_datos_num(df:pd.DataFrame) -> pd.DataFrame:
    """
    Limpia la columna duration eliminando texto y dejando solo valores numéricos.
    """

    def limp_segun_duracion(duracion):
        if duracion == None or duracion == 'nan':
            return '0'
        elif type(duracion) == float:
            return limp_segun_duracion(str(duracion))
        elif 'min' in duracion:
            return duracion[:-3]
        else:
            return duracion[:-7]

    df['duration'] = df['duration'].map(lambda x: limp_segun_duracion(x))
    # return df

def dar_formato(df):
    """
    Convierte columnas numéricas al tipo uint16.
    """
    columns_int = ['release_year', 'duration']
    for col in columns_int:
        df[col] = df[col].astype('uint16')
    
    # return df


def normalizar_col(df, dict_valores, col):
    """
    Normaliza los valores de una columna según un diccionario de equivalencias.
    """
    for key, valores in dict_valores.items():
        for str_valores in df[col]:
            for val in valores:
                if val in str_valores:
                    df[col][df[col] == str_valores] = (
                        df[col][df[col] == str_valores]
                        .replace({str_valores: str_valores.replace(val, key)})
                    )


def completar_col(df, columna, df_comprobar):
    """
    Completa valores nulos de una columna usando otro DataFrame como referencia.
    """
    mask_nan = df[columna].isna()
    films_nan = df['title'][mask_nan]

    mask_comp = films_nan.isin(df_comprobar['title'])
    film_comp = films_nan[mask_comp]

    for title in film_comp:
        valor_col_df = df[columna][df['title'] == title]
        if valor_col_df.isnull().values:
            valor_col = df_comprobar[columna][df_comprobar['title'] == title]
            if not valor_col.isnull().values:
                index = df[df['title'] == title].index
                index_col = list(df[0:0]).index(columna)
                df.iloc[index, index_col] = valor_col


def completar_datos_faltantes(df, lista_col, lista_df_comprobar):
    """
    Completa múltiples columnas utilizando una lista de DataFrames de referencia.
    """
    for col in lista_col:
        for df_com in lista_df_comprobar:
            completar_col(df, col, df_com)


    
# dfs = [df_a,df_d,df_n,df_h]

def Transformacion(dfs:dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Aplica todas las transformaciones necesarias a los datasets y devuelve
    un único DataFrame consolidado.
    """

    dfs['hulu']['cast'] = dfs['hulu']['cast'].astype('object')
    
    valores_normalizar: dict[str, list[str]] = {
        'Action & Adventure': ['Action-Adventure', 'TV Action & Adventure'],
        'Anime': ['Animation', 'Anime', 'Anime Features', 'Anime Series'],
        'Classic': ['Classic & Cult TV', 'Classic Movies', 'Classics'],
        'Comedy': ['TV Comedies', 'Comedies'],
        'Crime': ['Crime TV Shows'],
        'Documentary': ['Documentaries'],
        'Drama': ['TV Dramas', 'Dramas'],
        'Faith & Spirituality': ['Faith and Spirituality'],
        'Game Shows': ['Game Show / Competition'],
        'History': ['Historical'],
        'Horror': ['TV Horror', 'Horror Movies'],
        'International': ['International Movies', 'International TV Shows'],
        'Kids': ["Kids' TV"],
        'LGBTQ': ['LGBTQ Movies', 'LGBTQ+'],
        'Lifestyle': ['Lifestyle & Culture'],
        'Mystery': ['TV Mysteries'],
        'Music': ['Music & Musicals', 'Music Videos and Concerts', 'Musical'],
        'Reality': ['Reality TV'],
        'Romance': ['Romantic Movies', 'Romantic TV Shows'],
        'Sports': ['Sports Movies'],
        'Sci-Fi & Fantasy': ['TV Sci-Fi & Fantasy'],
        'Stand Up': ['Stand-Up Comedy', 'Stand-Up Comedy & Talk Shows'],
        'Thriller': ['TV Thrillers', 'Thrillers']
    }

    
    for plataforma, df in dfs.items():
        df['show_id'] = df['show_id'].map(lambda x: plataforma[0] + x[1:])
        limpiar_datos_num(df)
        dar_formato(df)
        normalizar_col(df, valores_normalizar, 'listed_in')
        df['platform'] = plataforma

    completar_datos_faltantes(dfs['hulu'], ['duration', 'cast'], [dfs['amazon'], dfs['disney'], dfs['netflix']])
    completar_datos_faltantes(dfs['netflix'], ['duration', 'cast'], [dfs['amazon'], dfs['disney'], dfs['hulu']])
    completar_datos_faltantes(dfs['amazon'], ['cast'], [dfs['netflix'], dfs['disney'], dfs['hulu']])
    completar_datos_faltantes(dfs['disney'], ['cast'], [dfs['netflix'], dfs['amazon'], dfs['hulu']])

    df_queries = pd.concat(list(dfs.values()), ignore_index=True)

    df_queries.drop(
        ['director', 'country', 'date_added', 'rating', 'description'],
        axis=1,
        inplace=True
    )

    df_queries.fillna('sin datos', inplace=True)

    columnas = ['type', 'title', 'cast', 'listed_in']
    for col in columnas:
        df_queries[col] = df_queries[col].apply(lambda x: x.lower())
        df_queries[col] = df_queries[col].apply(lambda x: x.rstrip().lstrip())

    return df_queries
