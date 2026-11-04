import json
import os
import re

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
    # Letters, digits, underscore, and hyphen are safe in the S3 prefix and the table key.
    project_code_name = re.sub(r"[^\w-]", "", project_name)
    bucket = os.environ.get("BUCKET")
    dynamodb = os.environ.get("DYNAMODB")

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

    if (not project_code_name):
        logger.error(f'Project name has no valid characters: {project_name}')
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "message": "Project name has no valid characters."
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

    if (not dynamodb):
        logger.error(f'On project: ${project_name}, no dynamoDB table is configured.')
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({
                "message": "Server error, please try later."
            })
        }
        

    s3 = boto3.resource('s3')
    table = boto3.resource("dynamodb").Table(dynamodb)
    readmeFile = s3.Object(bucket, f"projects/{project_code_name}/README.md")
    putReadmeFileResults = readmeFile.put(Body=README_DEFAULT,)

    readmeSource = s3.Object(bucket, f"projects/{project_code_name}/sources/README.md")
    putReadmeSourceResults = readmeSource.put(Body=README_SOURCES,)

    table.put_item(Item={"projectNameKey": project_code_name, "title": project_name})

    logger.info(f'Created project: {project_code_name} successfully.')

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "message": "Ok"
        })
    }
