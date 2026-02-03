# **Proyecto: Ingesta y Exposición de Datos mediante API REST**  

## **Descripción**  
Este proyecto consiste en la ingesta, transformación y exposición de datos desde múltiples fuentes, permitiendo su consulta a través de una API desarrollada en un entorno virtualizado con Docker. Se procesan datos de distintos formatos (CSV, JSON), se aplican técnicas de limpieza y normalización, y se implementan endpoints para responder a consultas específicas sobre películas y series.  

## **🛠 Tecnologías Utilizadas**  
- **Lenguaje:** Python 
- **Manejo de datos:** pandas, numpy  
- **API:** FastAPI
- **Virtualización:** Docker  
- **Almacenamiento:** Archivos CSV y JSON

## **📁 Estructura del Proyecto**  
```
📂 API-Peliculas-Series
 ├── 📁 app                    # Código fuente  
 │   ├── 📁__pycache__            
 │   ├── main.py               # Transformaciones y limpieza  
 │   ├── df_procesado          # Implementación de la API 
 ├── 📁 Datasets               # Archivos de datos en CSV/JSON     
 ├── Dockerfile                # Configuración del contenedor   
 ├── etl.ipynb                 # Análisis exploratorio de datos (EDA)
 ├── README.md                 # Documentación del proyecto
 ├── requirements.txt          # Dependencias del proyecto  
   
```


## **📌 Endpoints de la API**  

| Endpoint | Descripción | Ejemplo de Uso |
|----------|------------|----------------|
| `/get_max_duration?año=2020&plataforma=Netflix&tipo=min` | Devuelve la película/serie más larga por año y plataforma. | `get_max_duration(2020, "Netflix", "min")` |
| `/get_count_platform?plataforma=Amazon` | Cantidad de películas y series en una plataforma. | `get_count_platform("Amazon")` |
| `/get_listedin?genero=Comedy` | Plataforma con más títulos de un género específico. | `get_listedin("Comedy")` |
| `/get_actor?plataforma=Hulu&año=2019` | Actor más frecuente en una plataforma y año. | `get_actor("Hulu", 2019)` |
