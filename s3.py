import boto3



def list_buckets(client):
    response=client.list_buckets()
    print('Existing buckets:')
    i=0
    for bucket in response['Buckets']:
        bucket_name=bucket["Name"]
        i+=1
        print(f'{i}    {bucket_name}')
    return response['Buckets']

def s3_client():

#    Tenant Account Name,Access Key ID,Secret Access Key
#    Lab on Demand StorageGRID Tenant,7AOELIY3RT43U497MA6C,J+uRfTHWIeCTEjf4ZnZUwmXalNJcbdfVpz0YcixA

    endpoint_url='https://dc1-g1.demo.netapp.com:8082'
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
    # list_buckets(connection)
    return connection


def list_objects(connection, bucket_name):
    print('Listing object in bucket:',bucket_name)
    response=connection.list_objects(Bucket=bucket_name)
    i=0
    print('{0:<4s} {1:<15s} {2:<25s} {3:<10s} {4:<15s} {5:<15s}'.format('#','Name','Modified','Size','StorageClass','Owner'))
    for o in response['Contents']:
        i+=1
        print('{0:<4d} {1:<15s} {2:<25s} {3:<10d} {4:<15s} {5:<15s}'.format(i,o['Key'],str(o['LastModified'])[0:19],o['Size'],o['StorageClass'],o['Owner']['DisplayName']))
    return


def upload_file(connection,file_name,object_name=None):
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
    response = connection.upload_file(file_name, bucket_name, object_name,ExtraArgs={'Metadata': {'Seq_ID': 'Genome X'}})
    # print(response)
    list_objects(connection, bucket_name)
    return


connection=s3_client()
upload_file(connection,"s3test.py")
