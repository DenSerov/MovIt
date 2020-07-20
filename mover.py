#!/usr/bin/python

genome_new = "L:\\genome.new"
genome_processing = "L:\\genome.processing"
genome_finished = "L:\\genome.finished"

#genome_new = ".\\genome.new"
#genome_processing = ".\\genome.processing"
#genome_finished = ".\\genome.finished"
basecal = "basecall2.py"

from os import listdir
from os import mkdir
from os import rename
from os import chdir
from os import getcwd
from os import walk
from time import sleep
from time import ctime
from subprocess import Popen
import boto3


def list_buckets(client):
    response = client.list_buckets()
    print('Existing buckets:')
    i = 0
    for bucket in response['Buckets']:
        bucket_name = bucket["Name"]
        i += 1
        print(f'{i}    {bucket_name}')
    return response['Buckets']


def create_bucket(connection, bucket_name):
    connection.create_bucket(Bucket=bucket_name)
    return


def s3_client():

#    Tenant Account Name,Access Key ID,Secret Access Key
#    Lab on Demand StorageGRID Tenant,7AOELIY3RT43U497MA6C,J+uRfTHWIeCTEjf4ZnZUwmXalNJcbdfVpz0YcixA

    endpoint_url = 'https://dc1-g1.demo.netapp.com:8082'
    connection = boto3.client(
        's3',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id='7AOELIY3RT43U497MA6C',
        aws_secret_access_key='J+uRfTHWIeCTEjf4ZnZUwmXalNJcbdfVpz0YcixA',
        endpoint_url=endpoint_url,
        use_ssl=False,
        verify=False
    )
    # attrs=dir(connection)
    # for a in attrs:
    #     if hasattr(connection,a): print(a)
    print('Connected to',endpoint_url)
    list_buckets(connection)
    return connection


def list_objects(connection, bucket_name):
    print('Listing object in bucket:',bucket_name)
    response = connection.list_objects(Bucket=bucket_name)
    i = 0
    print('{0:<4s} {1:<15s} {2:<25s} {3:<10s} {4:<15s} {5:<15s}'.format('#','Name','Modified','Size','StorageClass','Owner'))
    for o in response['Contents']:
        i += 1
        print('{0:<4d} {1:<15s} {2:<25s} {3:<10d} {4:<15s} {5:<15s}'.format(i,o['Key'],str(o['LastModified'])[0:19],o['Size'],o['StorageClass'],o['Owner']['DisplayName']))
    return


def upload_file(connection, file_name, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    bucket_name = "genome"
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    connection.upload_file(file_name, bucket_name, object_name, ExtraArgs={'Metadata': {'Seq_ID': 'Genome X'}})
    # print(response)
    list_objects(connection, bucket_name)
    return


def download_file(connection, object_name, destination=None):
    """Down a file from an S3 bucket
    :param bucket: Bucket to download from
    :param object_name: S3 object name.
    :return: True if file was downloaded, else False
    """
    bucket_name = "genome"
    file_name = object_name
    response = connection.download_file(bucket_name, object_name, file_name)
    print(response)
    return


def mover():
    print(ctime(), "Mover is checking for FAST5 files")
    folder = []
    for entry in walk(genome_new):
        folder.append(entry)
    for address, dirs, files in folder:
        for f in files:
            print(address, f)
            if "fast5" in f:
                destination = address.replace('new', 'processing')
                try:
                    rename(address, destination)
                    print(f, "is moved to", destination, "directory")
                except :
                    print("error moving files!")

    folder = []
    for entry in walk(genome_processing):
        folder.append(entry)

    for address, dirs, files in folder:
        for d in dirs:
            print(ctime(), "Launching base call for FAST5 Seq_ID", d[-5:])
            print(address+'\\'+d)
            target = address+'\\'+d
            Popen('python3 basecall2.py %s' % (target,), shell=True)
            sleep(2)
    return True


mypath = '"'+getcwd() + "\\" + basecal + '"'
print(mypath)

while True:
    mover()
    sleep(2)
#    exit(0)
