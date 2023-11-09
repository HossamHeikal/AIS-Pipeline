FROM python:3.8

# supervisord setup                       
RUN apt-get update
RUN apt-get install -y supervisor              
COPY supervisord.conf /etc/supervisor/supervisord.conf

# Set environment variables for non-interactive (quiet) installation
ENV DEBIAN_FRONTEND=noninteractive

# Copy the JDK tarball from the build context into the image
COPY jdk1.8.0_381 /tmp/jdk1.8.0_381

# Change working directory
WORKDIR /tmp

# Move the extracted JDK 8 directory to /usr/lib/jvm/
RUN mkdir -p /usr/lib/jvm && mv jdk1.8.0_381 /usr/lib/jvm/

# Set up environment variables
ENV JAVA_HOME=/usr/lib/jvm/jdk1.8.0_381
ENV PATH="$JAVA_HOME/bin:$PATH"

# Airflow setup                       
ENV AIRFLOW_HOME=/app/airflow
RUN pip install apache-airflow        
# Install additional python packages
RUN pip install pyspark
# Install kafka-python using pip
RUN pip install wheel
RUN pip install kafka-python 
RUN pip install hdfs 
RUN pip install tqdm
RUN pip install apache-airflow-providers-apache-spark
#RUN pip install psycopg2
RUN pip install psycopg2-binary

# Copy the PostgreSQL JDBC driver into the image
COPY postgresql-42.6.0.jar /opt/spark/jars/

COPY /dags/ $AIRFLOW_HOME/dags/
COPY airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY ./aisdk-2023-10-26.zip /data/aisdk-2023-10-26.zip

RUN airflow db init
RUN airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

EXPOSE 8080
CMD ["/usr/bin/supervisord"]
