# analyze_data.py
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col, dayofmonth, month, year, to_date, concat_ws

def analyze_data(parquet_file_name):
    # Create a Spark session
    spark = SparkSession.builder.appName("AISAnalysist").master("spark://spark-master:7077").config("spark.executor.cores", "4").config("spark.executor.memory", "1g").getOrCreate()
    # Load the data from HDFS
    data = spark.read.parquet("hdfs://namenode:8020/parquet/"+ parquet_file_name +".parquet")

    # Assuming your timestamp column is named 'Timestamp'
    # Convert it to a date type if it's not already
    data = data.withColumn('Date', to_date(col("# Timestamp").alias("Timestamp")))

# Create a combined column for day-month-year
    data = data.withColumn('DayMonthYear', 
                       concat_ws('-', dayofmonth(col('Date')), month(col('Date')), year(col('Date'))))


    # Clean the data: Remove rows where 'Destination' is null or empty
    clean_data = data.filter(col("Destination").isNotNull() & (col("Destination") != ""))

    # Group by the combined day-month-year and destination and count occurrences
    popular_destinations = (
        clean_data.groupBy("DayMonthYear", "Destination")
        .agg(count("*").alias("Count"))
        .orderBy("Count", ascending=False)
    )
    
    # Convert column names to lowercase
    popular_destinations = popular_destinations.toDF(*[c.lower() for c in popular_destinations.columns])

    # Save the popular destinations analysis back to HDFS
    popular_destinations.write.mode("overwrite").parquet("hdfs://namenode:8020/aggs/PDA/" + parquet_file_name + ".parquet")

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    parquet_file_name = sys.argv[1]  # Get the Parquet file name from the command-line arguments
    analyze_data(parquet_file_name)
