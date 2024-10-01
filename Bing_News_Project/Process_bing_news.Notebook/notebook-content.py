# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e4ac12f2-0009-4eda-a6ac-47af67fb1ee9",
# META       "default_lakehouse_name": "bing_lake_db",
# META       "default_lakehouse_workspace_id": "b9817d44-c0fe-4db8-b955-c3a1eb72ab46"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # **Proyecto de Ingeniería de Datos**
# ## Extracción y Transformación de Noticias
# ### <font color = "green">Autor: Alejandro Parra Palacios </font>
# ---
# ## Descripción del Proyecto
# Este proyecto tiene como objetivo extraer noticias de la API de Bing Noticias y transformar la información utilizando Azure Data Factory para analizar contenido relevante de medios en tiempo real.

# MARKDOWN ********************

# ## Importe de librerass

# CELL ********************

# Importe de librerias
from pyspark.sql.functions import explode
import json
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import to_date, date_format
from pyspark.sql.utils import AnalysisException

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Conexion al dataset

# CELL ********************

# Extraemos la informacion del lakehouse
df = spark.read.option("multiline", "true").json("Files/bing-latest-news.json")
# df now is a Spark DataFrame containing JSON data from "Files/bing-latest-news.json".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transformacion de los datoss

# CELL ********************

# Selecionamos la columna de valor
df = df.select('value')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Expandimos la informacion
df_exploded = df.select(explode(df['value']).alias("json_object"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_exploded)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Volvemos la informacion Json en listas
json_list = df_exploded.toJSON().collect()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(json_list[18])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

news_json = json.loads(json_list[18])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(news_json)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Extraemos la informacion necesaria - prueba
print(news_json['json_object']['name'])
print(news_json['json_object']['description'])
print(news_json['json_object']['category'])
print(news_json['json_object']['url'])
print(news_json['json_object']['provider'][0]['image']['thumbnail']['contentUrl'])
print(news_json['json_object']['provider'][0]['name'])
print(news_json['json_object']['datePublished'])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Extraemos de forma general la informacion necesaria
title = []
description = []
category = []
url = []
image = []
provider = []
datePublished = []

for json_str in json_list:
    try:
        article = json.loads(json_str)

        if article['json_object'].get('category'):

            title.append(article['json_object']['name'])
            description.append(article['json_object']['description'])
            category.append(article['json_object']['category'])
            url.append(article['json_object']['url'])
            image.append(article['json_object']['provider'][0]['image']['thumbnail']['contentUrl'])
            provider.append(article['json_object']['provider'][0]['name'])
            datePublished.append(article['json_object']['datePublished'])

    except Exception as e:
        print(f'Error para procesar los Json: {e}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Creamos un dataframe con la informacion extraida
data = list(zip(title, description, category, url, image, provider, datePublished))

schema = StructType([
    StructField("title", StringType(), True),
    StructField("description", StringType(), True),
    StructField("category", StringType(), True),
    StructField("url", StringType(), True),
    StructField("image", StringType(), True),
    StructField("provider", StringType(), True),
    StructField("datePublished", StringType(), True)
])

df_cleaned = spark.createDataFrame(data, schema = schema)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_cleaned)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_cleaned_final = df_cleaned.withColumn('datePublished', date_format(to_date('datePublished'), 'dd-MMM-yyyy'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_cleaned_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Guardamos la informacion como tabla `Lakehouse`

# CELL ********************

try:
    table_name = 'bing_lake_db.tbl_latest_news'
    df_cleaned_final.write.format('delta').saveAsTable(table_name)

except AnalysisException:

    print('Table Already Exists')

    df_cleaned_final.createOrReplaceTempView('vw_df_cleaned_final')

    spark.sql(f"""
        MERGE INTO {table_name} target_table
        USING vw_df_cleaned_final source_view

        ON source_view.url = target_table.url

        WHEN MATCHED AND
        source_view.title <> target_table.title OR
        source_view.description <> target_table.description OR
        source_view.category <> target_table.category OR
        source_view.image <> target_table.image OR
        source_view.provider <> target_table.provider OR
        source_view.datePublished <> target_table.datePublished

        THEN UPDATE SET *

        WHEN NOT MATCHED THEN INSERT *
    """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
