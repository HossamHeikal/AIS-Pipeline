from hdfs import InsecureClient
from zipfile import ZipFile
import os
import shutil

def upload_to_hdfs(file_name):
    # Create an HDFS client connected to the NameNode
    hdfs_client = InsecureClient('http://namenode:9870', user='root')
    
    # Define the HDFS path where the file will be uploaded
    hdfs_path = '/data/' + os.path.basename(file_name)

    # Read the file from the specified directory and write it to HDFS
    with open('/data/' + file_name, "rb") as file:
        hdfs_client.write(hdfs_path, file)

    # Specify the local directory for unzipped files
    unzip_dir = '/data/unzipped_data'
    os.makedirs(unzip_dir, exist_ok=True) # Ensure the directory exists

    # Unzip the file within the specified directory
    with ZipFile('/data/' + file_name, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)

    # Upload the unzipped files to HDFS
    for root, dirs, files in os.walk(unzip_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            hdfs_file_path = '/data/unzipped/' + file
            with open(local_file_path, 'rb') as local_file:
                hdfs_client.write(hdfs_file_path, local_file)

    # Delete the unzipped data directory
    shutil.rmtree(unzip_dir)
