from carga import cargar_datos
import pandas as pd
import numpy as np

dfs = cargar_datos('../Datos/raw') # [amazon, disney, netflix, hulu]

# La columna 'cast' tiene Dtype float64, cuando deberia ser object.
# Además que no tiene datos por lo que cambaire lso ceros a 'Sin datos'

df_h = dfs[3]
df_h['cast'] = df_h['cast'].astype('object')
df_h['cast'] = df_h['cast'].fillna('Sin datos')