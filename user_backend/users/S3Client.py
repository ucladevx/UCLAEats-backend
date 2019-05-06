import boto3
import os
from io import BytesIO

boto3.set_stream_logger(name='botocore')

class S3Client(object):
    def __init__(self):
        ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
        SECRET_KEY = os.getenv('AWS_SECRET_KEY')
        print(ACCESS_KEY, SECRET_KEY)
        self.client = boto3.client(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                region_name='us-west-2'
        )
        self.bucket = os.getenv('S3_BUCKET')
    # takes a file-like 'fileobj' (can perform fileobj.read())
    def upload_obj(self, fileobj, filename):
        #print(fileobj.read())
        try:
            self.client.upload_fileobj(fileobj, self.bucket, filename)
        except Exception as e:
            print(e)
            raise e
        return
    
    #fileobj (internal variable) must be a file-like (can perform fileobj.write())
    def download_obj(self, filename):
        #fileobj = BytesIO()
        try:
            # with open('test_file.jpg', 'wb') as data:
            #     self.client.download_fileobj(self.bucket, filename, data)
            #     file_data = data.read()
            ret = self.client.get_object(Bucket=self.bucket, Key=filename)
        except Exception as e:
            print(e)
            raise e
        file_data = ret['Body'].read()
        return file_data