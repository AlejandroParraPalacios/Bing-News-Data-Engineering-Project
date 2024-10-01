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
# ## Modelo de ML para análisis de Sentimiento de Noticias
# ### <font color = "green">Autor: Alejandro Parra Palacios </font>
# ---
# ## Descripción del Proyecto
# Este notebook se enfoca en la realización de un análisis de sentimiento utilizando la librería SynapseML. El objetivo principal es analizar el sentimiento asociado a cada noticia, categorizándolas como positivas, negativas o neutras.

# CELL ********************

# Importe de librerias
import synapse.ml.core
from synapse.ml.services import AnalyzeText
from pyspark.sql.functions import col
from pyspark.sql.utils import AnalysisException
from pyspark.sql.functions import col, to_date

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Conexion al lakehouse
df = spark.sql("SELECT * FROM bing_lake_db.tbl_latest_news LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Configuramos los hiperparametros para el modelo
model = (AnalyzeText().setTextCol('description').setKind('SentimentAnalysis').setOutputCol('response').setErrorCol("error"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Entrenamos nuestro modelo
result = model.transform(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(result)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Creamos una columan de sentimiento
sentimient_df = result.withColumn('sentiment', col('response.documents.sentiment'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(sentimient_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sentimient_df_final = sentimient_df.drop('error', 'response')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(sentimient_df_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sentimient_df_final = sentimient_df_final.withColumn("datePublished", to_date(col("datePublished"), "dd-MMM-yyyy"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    table_name = 'bing_lake_db.tbl_sentiment_analysis'
    sentimient_df_final.write.format('delta').saveAsTable(table_name)

except AnalysisException:

    print('Table Already Exists')

    sentimient_df_final.createOrReplaceTempView('vw_sentimient_df_final')

    spark.sql(f"""
        MERGE INTO {table_name} target_table
        USING vw_sentimient_df_final source_view

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
