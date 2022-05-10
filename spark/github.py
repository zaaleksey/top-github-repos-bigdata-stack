from configparser import ConfigParser

from github_top_repos import *
from pyspark import SparkContext
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark: SparkSession = SparkSession.builder \
        .master("local[*]") \
        .appName("top repos") \
        .getOrCreate()
    sc: SparkContext = spark.sparkContext

    config = ConfigParser()
    config.read("config.ini")

    number_of_organization = int(config['GitHub']['number_of_organization'])
    top_number = int(config['GitHub']['top_number'])

    api = DefaultGitHubAPI(config)

    orgs_worker = OrganizationWorker(number_of_organization, api)
    repos_urls = [url for url in orgs_worker.exec()]
    repos_urls_rdd = sc.parallelize(repos_urls)

    repos_worker = RepositoryWorker(api)
    repos_rdd = repos_urls_rdd.flatMap(lambda url: repos_worker.exec(url))
    repos_df = spark.createDataFrame(repos_rdd)

    sorted_repos_df = repos_df.sort("stars_count", ascending=False)

    top_repos = sorted_repos_df.head(top_number)

    top = list(map(lambda row: row.asDict(), top_repos))

    db = DatabaseWorker()
    db.exec(top)
