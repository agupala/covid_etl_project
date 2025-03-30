# 🦠 COVID-19 ETL with PySpark & Streamlit  

Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** para analizar los datos de COVID-19 en **Argentina, Chile, Bolivia, Paraguay, Brasil y Uruguay**.  

Usamos **PySpark** para procesar grandes volúmenes de datos y **Streamlit** para crear un **dashboard interactivo**.  

## 📌 Tecnologías Utilizadas  

✅ **Python** para el desarrollo general.  
✅ **PySpark** para la transformación y procesamiento de datos.  
✅ **Pandas** para manipulación inicial de datos.  
✅ **Streamlit** para visualizar datos en un dashboard.  
✅ **Pytest** para pruebas unitarias.  
✅ **PEP8, pylint, mypy** para mantener código limpio y bien documentado.  

---

## 📂 Estructura del Proyecto  

```
covid_pyspark_project/
│── .data/                    # Carpeta oculta donde se guardan los datos procesados
│── notebooks/                 # Análisis exploratorio de datos (EDA)
│   ├── eda.ipynb              # Notebook con descarga y análisis inicial de los datos
│── src/                       # Código fuente del proyecto
│   ├── main.py                # Ejecuta todo el pipeline ETL
│   ├── etl.py                 # Clase ETL para procesamiento en PySpark
│   ├── data_loader.py         # Descarga y guarda los datos COVID-19
│   ├── dashboard.py           # Dashboard interactivo con Streamlit
│   ├── utils.py               # Funciones auxiliares (si es necesario)
│── tests/                     # Pruebas unitarias con pytest
│   ├── test_data_loader.py    # Test para DataLoader
│   ├── test_etl.py            # Test para ETL
│   ├── test_dashboard.py      # Test para Dashboard
│── .gitignore                 # Archivos a ignorar en Git
│── requirements.txt           # Dependencias del proyecto
│── README.md                  # Explicación del proyecto
│── pyproject.toml             # Configuración de formato y linting
│── setup.cfg                  # Reglas de PEP8, mypy, pylint
│── tox.ini                    # Configuración para pruebas automatizadas
│── Makefile                   # Comandos para facilitar ejecución de tareas
```

---

## ⚙️ Explicación de los Módulos  

### 📌 `data_loader.py`  

🔹 Descarga el dataset desde Our World In Data.  
🔹 Filtra los datos solo para los países seleccionados.  
🔹 Guarda el dataset en **`.data/covid_data.csv`** para que pueda ser procesado en el ETL.  

### 📌 `etl.py`  

🔹 Carga los datos filtrados usando **PySpark**.  
🔹 Realiza **mínima transformación**: selecciona columnas clave y elimina valores nulos.  
🔹 Guarda los datos transformados en formato **Parquet** (`.data/covid_data.parquet`).  

### 📌 `dashboard.py`  

🔹 Carga los datos transformados en PySpark.  
🔹 Muestra los datos en una interfaz web interactiva con **Streamlit**.  

### 📌 `main.py`  

🔹 Ejecuta **todo el pipeline**:  
   1. Descarga y filtra los datos (`data_loader.py`).  
   2. Ejecuta la transformación en PySpark (`etl.py`).  
   3. Guarda el resultado en formato Parquet.  
   4. Muestra un mensaje de éxito en la consola.  

### 📌 `notebooks/eda.ipynb`  

🔹 Realiza **análisis exploratorio** del dataset de COVID-19.  
🔹 Muestra gráficos con la evolución de casos por país.  
🔹 Aplica **promedio móvil** para suavizar tendencias.  

### 📌 Carpeta `.data/`  

🔹 Es una **carpeta oculta** donde se guardan los datos (`covid_data.csv` y `covid_data.parquet`).  

### 📌 `tests/`  

🔹 Contiene pruebas unitarias para verificar que las funciones del ETL y el dashboard funcionan correctamente.  

---

## 🏃 Cómo Ejecutar el Proyecto  

### 📌 1️⃣ Instalar dependencias  

Ejecuta el siguiente comando para instalar todos los paquetes necesarios:  

```sh
pip install -r requirements.txt
```

### 📌 2️⃣ Ejecutar el ETL  

Para procesar los datos en PySpark y guardarlos en formato Parquet, ejecuta:  

```sh
python src/main.py
```

### 📌 3️⃣ Ejecutar el Dashboard  

Si quieres visualizar los datos en un dashboard interactivo, usa:  

```sh
streamlit run src/dashboard.py
```

---

## ✅ Pruebas Unitarias  

Para ejecutar las pruebas unitarias y verificar que todo funciona correctamente:  

```sh
pytest tests/
```

---

## 🎯 Mejoras Futuras  

🔹 Agregar más análisis exploratorio al notebook.  
🔹 Incluir modelos de predicción de COVID-19.  
🔹 Conectar con una base de datos SQL en lugar de archivos locales.  

---
