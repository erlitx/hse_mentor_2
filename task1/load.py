from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date


spark = SparkSession.builder \
    .appName("Yandex Data Proc - HW") \
    .enableHiveSupport() \
    .getOrCreate()

transactions_path = "s3a://hses3/transactions_v2.csv"
logs_path = "s3a://hses3/logs_v2.txt"


# Загрузка данных
transactions = spark.read.option("header", "true").option("inferSchema", "true").csv(transactions_path)
logs = spark.read.option("header", "true").option("inferSchema", "true").csv(logs_path, sep="\t")

transactions = transactions.withColumn("transaction_date", to_date(col("transaction_date")))

transactions.write.mode("overwrite").saveAsTable("transactions_v2")
logs.write.mode("overwrite").saveAsTable("logs_v2")
