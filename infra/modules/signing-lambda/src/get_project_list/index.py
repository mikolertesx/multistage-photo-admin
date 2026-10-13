import json
import os

import boto3

# Creates a media project in S3
def handler(event, context):
    s3 = boto3.client('s3')
    bucket = os.environ["BUCKET"]

    # Delimiter groups keys at the next "/", so nested objects stay out of Contents.
    response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix='projects/',
            Delimiter='/',
            MaxKeys=100 )

    return {
        "statusCode": 200,
        "body": json.dumps({
            # Since Content only returns files
            # And S3 doesn't see folders
            # I needed to go with CommonPrefixes rather than
            # Contents, which is quite weird.
            "projectList": response["CommonPrefixes"]
        }, default=str)
    }
