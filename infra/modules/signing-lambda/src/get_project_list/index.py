import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lists media projects in S3
def handler(event, context):
    dynamodb = os.environ.get("DYNAMODB")

    table = boto3.resource("dynamodb").Table(dynamodb)

    # Scan the table for all entries
    response = table.scan()
    items = response.get("Items", [])

    projects = [
        {
            "project_code_name": item["projectNameKey"],
            "project_name": item["title"],
        }
        for item in items
    ]

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "projectList": projects
        }, default=str),
    }
