#!/bin/bash

# Run the command to create an Airflow user
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

# Execute the CMD
exec "$@"
