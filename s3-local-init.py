import os
import glob
import boto3


s3 = boto3.resource(
    's3',
    aws_access_key_id='accessKey1',
    aws_secret_access_key='verySecretKey1',
    endpoint_url='http://localhost:8000'
)


def put_files(bucket: str):
    prefix = f's3/{bucket}/'

    def put_file(bucket: str, path: str):
        with open(f'{prefix}{path}') as f:
            s3.Object(bucket, path).put(Body=f.read())

    entries = glob.glob(f'{prefix}**', recursive=True)
    files = filter(os.path.isfile, entries)
    for f in files:
        put_file(bucket, f.replace(prefix, ''))


buckets = map(os.path.basename, glob.glob('s3/*'))
for b in buckets:
    s3.create_bucket(Bucket=b)
    put_files(b)

