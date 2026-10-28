import json
import os

import boto3

import logging  
logger = logging.getLogger()
logger.setLevel(logging.INFO)
README_DEFAULT = b'Inicio del proyecto'
README_SOURCES = b'Aqui van los archivos'

# Creates a media project in S3
def handler(event, context):

    params = event.get("queryStringParameters") or {}
    project_name = (params.get("project_name") or "").strip()
    bucket = os.environ.get("BUCKET")

    if (not params):
        logger.error(f'Attempted to create a project with no params.')
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "message": "No params were provided."
            })
        }

    if (not project_name):
        logger.error(f'Project has no project_name')
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "message": "No project name was provided."
            })
        }

    if (not bucket):
        logger.error(f'On project: ${project_name}, no bucket is configured.')
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "message": "Server error, please try later."
            })
        }

    s3 = boto3.resource('s3')
    readmeFile = s3.Object(bucket, f"projects/{project_name}/README.md")
    putReadmeFileResults = readmeFile.put(Body=README_DEFAULT,)

    readmeSource = s3.Object(bucket, f"projects/{project_name}/sources/README.md")
    putReadmeSourceResults = readmeSource.put(Body=README_SOURCES,)

    logger.info(f'Created project: {project_name} successfully.')

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "message": "Ok"
        })
    }
