import sys
import os.path
from os import path
import boto3
import botocore
from botocore.client import Config
import time
from time import mktime
from datetime import datetime
import pytz


if len(sys.argv) != 3:
    print("Arguments must be : Folder_name Bucket_name")
    exit()

utc=pytz.UTC
bucket_name = sys.argv[2]
folder_path = sys.argv[1]
client = boto3.client('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='minioadmin',
                    aws_secret_access_key='minioadmin',
                    config=Config(signature_version='s3v4'),
                    region_name='eu-west-1')


s3 = boto3.resource('s3',
                    endpoint_url='http://localhost:9000',
                    aws_access_key_id='minioadmin',
                    aws_secret_access_key='minioadmin',
                    config=Config(signature_version='s3v4'),
                    region_name='eu-west-1')



_exit = 0

bucket_exist = client.head_bucket(
    Bucket=bucket_name
)

if (not bucket_exist.get("ResponseMetadata").get("HTTPStatusCode") == 200):
    print("No bucket with the given name")
    _exit = 1
if (not os.path.exists(folder_path)):
    print("No folder with the given name")
    _exit = 1
if (_exit == 1):
    print("Quitting script")
    exit


bucket = s3.Bucket(bucket_name)
bucket_objects = bucket.objects.all()


def uploaded(string):
    print ("file uploaded" + string)


def sync_folder(path):
    folder = os.listdir(path)
    for item in folder:
        if (os.path.isdir(item)):
            sync_folder(path+item+'\\')
        else:
            file_path=path+item
            print(file_path)
            try:
                bucket.Object(file_path).get()
                _object = bucket.Object(file_path)
                print("their is an item with the name " + _object.key)
                if (not _object == None):
                    last_modified_file = datetime.fromtimestamp(os.path.getatime(file_path)).replace(tzinfo=pytz.UTC)
                    last_modified_object = (_object.last_modified)
                    print("object last modified : ")
                    print(last_modified_object)
                    print("file last modified : ")
                    print(last_modified_file)
                    if (last_modified_object < last_modified_file):
                        print("uploading file")
                        s3.meta.client.upload_file(
                            Filename=file_path,
                            Bucket=bucket_name, 
                            Key=file_path,
                            ExtraArgs=None,
                            Callback=None,
                            Config=None)
            except botocore.exceptions.ClientError as ex:
                if ex.response['Error']['Code'] == 'NoSuchKey':
                    s3.meta.client.upload_file(
                        Filename=file_path,
                        Bucket=bucket_name, 
                        Key=file_path,
                        ExtraArgs=None,
                        Callback=uploaded(file_path),
                        Config=None)

                    
    for item in bucket_objects:
        _object = bucket.Object(item)
        if (not os.path.exists(item.key)):
            print("Deleting : "+item.key)
            s3.meta.client.delete_object(
                        Bucket=bucket_name, 
                        Key=item.key)


sync_folder(folder_path)