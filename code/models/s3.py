import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

class s3Client():

    s3_client = boto3.client('s3')

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_s3_resource(cls, name):

        return cls.s3_resource.Bucket(name)
