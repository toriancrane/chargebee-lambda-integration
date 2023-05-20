import requests
import json
import boto3
import zipfile
import io
import os

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

BUCKET_NAME = "chargebee-to-aws-workshop" # Replace this value with the name of your S3 Bucket if different
FOLDER_NAME = 'exports'

def lambda_handler(event, context):

    print("Download started...")
    url=event["Url"]
    req = requests.get(url)
    content = io.BytesIO(req.content)
    
    z = zipfile.ZipFile(content)
    
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        s3_resource.meta.client.upload_fileobj(
            z.open(filename),
            Bucket=BUCKET_NAME,
            Key=f'{FOLDER_NAME}/{filename}'
        )
        
    print("Download complete!")
    
    return event
