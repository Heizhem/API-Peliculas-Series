# Proyecto: Pipeline de Datos y API REST para Películas y Series

## 📌 Descripción
Este proyecto implementa un **pipeline completo de datos**, desde el análisis exploratorio (EDA), pasando por un proceso de **ETL**, hasta la **exposición de los datos mediante una API REST** desarrollada con FastAPI.

Se procesan datasets de distintas plataformas de streaming (CSV y JSON), se aplican procesos de limpieza, normalización y consolidación, y el dataset resultante es expuesto mediante endpoints de solo lectura (GET).

---

## 🔄 Flujo del Proyecto

1. **EDA (Exploratory Data Analysis)**  
   Análisis exploratorio de los datasets originales para detectar inconsistencias, valores faltantes y definir reglas de normalización.

2. **ETL (Extract, Transform, Load)**  
   - **Extract:** lectura de datos desde archivos CSV/JSON  
   - **Transform:** limpieza, normalización de categorías y unificación de formatos  
   - **Load:** generación de un dataset consolidado en CSV

3. **API REST**  
   La API carga el dataset procesado una única vez en memoria y expone endpoints para consultas analíticas.

---

## 🛠 Tecnologías Utilizadas
- **Lenguaje:** Python  
- **Procesamiento de datos:** pandas, numpy  
- **API:** FastAPI  
- **Contenerización:** Docker  
- **Almacenamiento:** Archivos CSV y JSON  

---

## 📁 Estructura del Proyecto

```text
app/
├── main.py                # API FastAPI (endpoints GET)

Datos/
├── archivos/              # Datasets originales (raw)
└── procesados/
    └── df_procesado.csv   # Dataset final generado por el ETL

ETL/
├── extraer.py             # Extracción de datos
├── transformar.py         # Transformaciones y normalización
├── cargar.py              # Carga del dataset final
├── etl.py                 # Orquestador del proceso ETL
└── EDA.ipynb              # Análisis exploratorio de datos

Dockerfile
requirements.txt
README.md
````

---

## ⚙️ Ejecución del ETL

Desde la raíz del proyecto:

```bash
python ETL/etl.py
```

Este proceso genera el archivo:

```text
Datos/procesados/df_procesado.csv
```

---

## 🚀 Ejecución de la API por Consola

```bash
uvicorn app.main:app --reload
```
*Para detener el programa* `ctrl + C`.

## 🚀 Ejecución de la API con Docker

### 📋 Requisitos

- Tener Docker instalado
- Estar ubicado en la raíz del proyecto (donde está el `Dockerfile`)

---

**Construir la imagen**

```bash
docker build -t fastapi-app .
```
**Ejecutar el contenedor**
```bash
docker run -p 8000:80 --name api-peliculas fastapi-app
```

*Para detener el programa* `ctrl + C`.

---
### Ejecutar al terminar de usar la api
**Detener el contenedor**

```bash
docker stop api-peliculas
```
**Eliminar el contenedor**

```bash
docker rm -f api-peliculas
```
---
## 📋 Acceder a la API

**Abrir en el navegador**

```bash
http://localhost:8000
```
**Documentación interactiva**

```bash
http://localhost:8000/docs
```
---

## 📌 Endpoints Disponibles

| Endpoint              | Descripción                                            |
| --------------------- | ------------------------------------------------------ |
| `/get_max_duration`   | Título con mayor duración según año, plataforma y tipo |
| `/get_count_platform` | Cantidad de títulos por plataforma                     |
| `/get_listedin`       | Plataforma con más títulos de un género                |
| `/get_actor`          | Actor más frecuente por plataforma y año               |

---

## 🎯 Alcance y Decisiones de Diseño

* API de solo lectura (GET)
* Dataset cargado una sola vez en memoria
* Separación clara entre EDA, ETL y API
* Diseño simple y reproducible, preparado para escalar a base de datos si el volumen lo requiere

---

## 🧠 Comentario Final

El proyecto prioriza **claridad, buenas prácticas y separación de responsabilidades**, evitando complejidad innecesaria dada la escala del dataset y el tipo de consultas.
