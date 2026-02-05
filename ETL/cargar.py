import pandas as pd

def Guardar(df):
    """
    Guarda el DataFrame procesado en un archivo CSV.
    """
    df.to_csv('../Datos/procesados/df_procesado.csv', index=False)