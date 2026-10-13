import json
import os

import boto3


README_DEFAULT = b'Inicio del proyecto'
README_SOURCES = b'Aqui van los archivos'

# Creates a media project in S3
def handler(event, context):
    s3 = boto3.resource('s3')

    projectName = event["queryStringParameters"]["project_name"]
    bucket = os.environ["BUCKET"]

    readmeFile = s3.Object(bucket, f"projects/{projectName}/README.md")
    putReadmeFileResults = readmeFile.put(Body=README_DEFAULT,)

    readmeSource = s3.Object(bucket, f"projects/{projectName}/sources/README.md")
    putReadmeSourceResults = readmeSource.put(Body=README_SOURCES,)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Ok"
        })
    }
