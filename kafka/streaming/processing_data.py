from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lit, sum
from pyspark.sql.types import StringType
from pyspark.streaming import StreamingContext


@udf(returnType=StringType())
def get_ip(value):
    return value.split()[-1][:-1]


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[*]") \
        .appName("streaming_test") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1") \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 3)

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .option("subscribe", "test") \
        .load()

    drop_column = ["key", "topic", "partition", "offset", "timestamp", "timestampType"]
    df = df.withColumn("value", df['value'].cast(StringType())).drop(*drop_column)

    ip_count_df = df.withColumn("ip", get_ip(col('value'))) \
        .withColumn("count", lit(1)) \
        .groupBy(col("ip")) \
        .agg(sum(col("count"))).alias("count") \
        .orderBy("count", ascending=False)

    ip_count_df.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()
