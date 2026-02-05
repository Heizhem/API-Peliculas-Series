from extraer import Extracion
from transformar import Transformacion
from cargar import Guardar


def realizar_etl():
    """
    Ejecuta el pipeline completo de ETL.
    """
    ruta = "../Datos/archivos/"
    dfs = Extracion(ruta)
    df_final = Transformacion(dfs)
    Guardar(df_final)
    return


if __name__ == "__main__":
    realizar_etl()

