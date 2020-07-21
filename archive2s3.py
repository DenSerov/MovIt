# import boto3
from boto3 import client as s3client
from sys import argv
from time import sleep
from os import listdir
from os import path
from random import randint


if len(argv) == 6:
    source = argv[1]
    target = argv[2]
    url = argv[3]
    access_key_id = argv[4]
    secret_access_key = argv[5]
    print("Using input parameters", url, access_key_id,secret_access_key)
else:
    source = "./"
    target = "testbucket"+str(randint(100000,999999))
    url = "http://192.168.221.1:9000"
    access_key_id = "minioadmin"
    secret_access_key = "minioadmin"
    print("Using defaults", url, access_key_id,secret_access_key,source,target)
    sleep(1)


def list_buckets(client):
    response = client.list_buckets()
    print('Existing buckets:')
    i=0
    for bucket in response['Buckets']:
        bucket_name = bucket["Name"]
        i += 1
        print(f'{i}    {bucket_name}')
    return response['Buckets']


def s3_client():
    connection = s3client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        endpoint_url=url,
        use_ssl=False,
        verify=False
    )
    print('Connected to',url)
    return connection


def upload_folder_to_bucket(connection,folder_name,bucket_name):
    response = connection.create_bucket(Bucket=bucket_name)
    # print(response)
    files=listdir(source)
    for f in files:
        object_name = f
        if not path.isdir(f):
            print("Uploading to S3:",f)
            connection.upload_file(folder_name+'\\'+f, bucket_name, object_name,ExtraArgs={'Metadata': {'Seq_ID': 'Test'}})
    sleep(5)
    return


# initialize()
connection=s3_client()
upload_folder_to_bucket(connection,source,target)
sleep(10)
