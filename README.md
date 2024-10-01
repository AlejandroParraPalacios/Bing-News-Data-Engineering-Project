# Proyecto de Ingeniería de Datos: Análisis de Noticias de Bing

Este proyecto realiza una ingeniería de datos de extremo a extremo en la plataforma **Microsoft Azure Fabric** para analizar noticias provenientes de la API de Bing. La solución implementada utiliza diversos servicios de Azure para la extracción, transformación, carga (ETL), almacenamiento y visualización de los datos, proporcionando información valiosa mediante la integración de tecnologías como **PySpark** y **Microsoft Power BI**.

---

## Descripción del Proyecto

Este proyecto consiste en la construcción de un flujo de datos que extrae noticias de Bing a través de su API, realiza un procesamiento de datos con **PySpark**, y almacena los resultados en un **Data Lake**. A continuación, se utiliza **Power BI** para visualizar los resultados, permitiendo un análisis más profundo de las noticias en tiempo real.

## Objetivos del Proyecto

- Extraer datos de la API de Bing.
- Procesar los datos utilizando PySpark en Microsoft Fabric.
- Almacenar los datos procesados en un Data Lake.
- Analizar los datos utilizando un dashboard de Power BI.
- Realizar análisis de sentimiento sobre las noticias.

## Tecnologías Utilizadas

- **Microsoft Azure Fabric**: Para la gestión del flujo completo de datos.
- **PySpark**: Para el procesamiento distribuido de grandes volúmenes de datos.
- **Microsoft Power BI**: Para la creación de dashboards interactivos que permiten visualizar el análisis de las noticias.
- **API de Bing**: Para la extracción de las noticias en tiempo real.
- **Data Lake**: Para el almacenamiento de datos estructurados y no estructurados.

## Componentes Principales

1. **Extracción de datos (API de Bing)**: Se utiliza la API de Bing para obtener un conjunto de noticias recientes. Estas noticias incluyen información como el título, descripción, fuente, fecha de publicación y otros metadatos relevantes.
   
2. **Transformación de datos (PySpark)**: Se aplica PySpark para limpiar y transformar los datos extraídos. Las operaciones incluyen:
   - Eliminación de duplicados.
   - Normalización de campos.
   - Análisis de sentimientos sobre los títulos de las noticias.
   
3. **Almacenamiento de datos (Data Lake)**: Los datos transformados se almacenan en un **Lakehouse** dentro de Microsoft Fabric, que actúa como repositorio centralizado para el análisis posterior.

4. **Visualización (Power BI)**: Un tablero en Power BI presenta un análisis visual de los datos transformados, con métricas clave como:
   - Número de noticias por categoría.
   - Análisis de sentimientos.
   - Tendencias de noticias por fecha y fuente.