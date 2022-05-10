import requests
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, avg, row_number, udf
from pyspark.sql.types import IntegerType
from pyspark.sql.window import Window


def get_spark_session(name: str, master: str = "local[*]"):
    spark_session = SparkSession.builder \
        .master(master) \
        .appName(name) \
        .getOrCreate()
    return spark_session


@udf(returnType=IntegerType())
def define_group(value, num):
    return value // num


if __name__ == '__main__':
    spark: SparkSession = get_spark_session("ohlcv")
    sc: SparkContext = spark.sparkContext

    sma_num = 30
    coin = "ethereum"
    period = "365"
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days={period}"
    schema = ["time", "open", "high", "low", "close"]

    data = requests.get(url).json()

    rdd = sc.parallelize(data)
    df = spark.createDataFrame(rdd, schema=schema)

    order_by_time = Window.orderBy("time")
    partition_by_group = Window.partitionBy("group")

    df = df.withColumn("row_num", row_number().over(order_by_time))
    df = df.withColumn("group", define_group(df["row_num"], lit(sma_num)))
    df = df.withColumn("sma", avg("close").over(partition_by_group))

    price_over_sma_df = df.filter(df["close"] > df["sma"])

    columns_to_drop = ["row_num", "group", "sma"]
    df = df.drop(*columns_to_drop)
    price_over_sma_df = price_over_sma_df.drop(*columns_to_drop)

    # save resulting df
    price_over_sma_df.write.csv(path="filter_sma_csv", header=True, sep=",")
    price_over_sma_df.write.parquet(path="filter_sma_parquet")
