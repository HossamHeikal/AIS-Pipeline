# convert_to_parquet.py
import sys
from pyspark.sql import SparkSession

def convert_to_parquet(url):
    date_string = url.split('/')[-1].replace('.zip', '')
    csv_path_on_hdfs = 'hdfs://namenode:8020/data/unzipped/' + date_string + '.csv'

    spark = SparkSession.builder.appName("convert from CSV to Parquet").master("spark://spark-master:7077").config("spark.executor.cores", "4").config("spark.executor.memory", "1g").getOrCreate()
    df = spark.read.csv(csv_path_on_hdfs, header=True, inferSchema=True)
    parquet_path = f"hdfs://namenode:8020/parquet/" + date_string + ".parquet"
    df.write.parquet(parquet_path)

    spark.stop()

if __name__ == "__main__":
    # Get the URL from the command-line arguments
    url = sys.argv[1]
    convert_to_parquet(url)