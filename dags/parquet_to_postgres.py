import sys
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from sqlalchemy import create_engine

def parquet_to_postgres(hdfs_path, postgres_url, postgres_url2, table_name, user, password):
    # Initialize the SparkSession
    spark = SparkSession.builder \
    .appName("Parquet to Postgres") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.cores", "4") \
    .config("spark.executor.memory", "1g") \
    .config("spark.jars", "/opt/spark/jars/postgresql-42.6.0.jar").getOrCreate()


    # Define PostgreSQL properties
    properties = {
        "user": user,
        "password": password,
        "driver": "org.postgresql.Driver"
    }

    # Read data from HDFS
    df = spark.read.parquet(hdfs_path)

    # Convert column names to lowercase
    df = df.toDF(*[c.lower() for c in df.columns])

    # Initialize SQLAlchemy engine
    engine = create_engine(postgres_url)

    # Check if the schema exists, create if not
    if not engine.dialect.has_schema(engine, "ais"):
        engine.execute("CREATE SCHEMA ais")

    # Define the full table path including the schema
    full_table_name = f"ais.{table_name}"

    try:
        # Write data to PostgreSQL, it will create the table if it does not exist
        df.write.jdbc(url=postgres_url2, table=full_table_name, mode="overwrite", properties=properties)
    except AnalysisException as e:
        print(f"An error occurred: {e}")

    # Close the SparkSession
    spark.stop()

if __name__ == "__main__":
    # Get parameters from command line arguments
    hdfs_path = sys.argv[1]
    postgres_url = sys.argv[2]
    postgres_url2 = sys.argv[3]
    schema_name = 'ais'  # This is your schema name
    table_name = sys.argv[4]
    user = sys.argv[5]
    password = sys.argv[6]

    # Call the function with the schema included in the table name
    parquet_to_postgres(hdfs_path, postgres_url, postgres_url2, table_name, user, password)
