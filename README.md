* Data Source: http://web.ais.dk/aisdata/aisdk-2023-10-26.zip
* Java 8: https://www.oracle.com/java/technologies/downloads/#license-lightbox

# AIS-Pipeline
End-to-End Automated Data Pipeline: From Data Acquisition to Visualization with Dockerized Spark, HDFS, and Airflow
![AIS-Pipeline](https://github.com/HossamHeikal/AIS-Pipeline/assets/58578405/fdc5e73a-9996-4e38-84bb-9a2785066eba)
**Project Overview**

**Objective**:
Build a system that automates data download, processes it, and prepares it for visualization.

**Project Context**:
The data engineering project extracts AIS data for analysis, helping in visualizing ship movements and related insights.

**AIS Data**

**AIS (Automatic Identification System)** is a navigation safety system used by ships and maritime authorities. It electronically shares vessel details, such as:

1. **Identification**: Unique vessel ID, call sign, and name.
2. **Location**: Current position, course, and speed.
3. **Vessel Details**: Type (e.g., cargo, tanker), destination, estimated arrival time, and more.
   
**Components**:
1. **Docker**: Ensures our setup works uniformly across different environments.
2. **Apache Spark**: Handles large-scale data processing.
3. **HDFS**: A place to store our large datasets.
4. **PostgreSQL**: A database for storing our processed data.
5. **Metabase**: A tool to visualize our data.
6. **Airflow**: Schedules and automates our tasks.

**Workflow**:

1. **Setup**:
   - Use Docker to create a system with Spark, Hadoop, Kafka, PostgreSQL, Metabase, and other necessary tools.
   
2. **Data Collection and Storage**:
   - Automatically download data from a specific website.
   - Store the data in HDFS.
   
3. **Task Automation**:
   - Use Airflow to schedule daily data downloads and processing between specific dates.
   
4. **Data Transformation**:
   - Read the stored data, clean it, and make a popular destination analysis for the ship.
   
**Outcome**:
The system will automatically gather, process, and store data daily, making it ready for visual analysis.

**Recommendations**:
1. Add error-handling to ensure smooth operations.
2. Push the results to PostgreSQL for easy visualization.
3. Monitor the system's health regularly.
4. Add a debezium connector and a kafka image to make more transformations to the postgres table

Implement error-handling for reliability.
Integrate results with PostgreSQL for enhanced visualization.
Conduct regular system health checks.
