#!/bin/bash
# move_to_hdfs.sh

# Move the file to HDFS
hdfs dfs -put /opt/hadoop/data/aisdk-2023-10-26.zip /path/in/hdfs
