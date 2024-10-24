import json
import boto3
import uuid
import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE = 'Posts'

def lambda_handler(event, context):
    try:
        email = event['email']
        title = event['title']

        post_id = str(uuid.uuid4())

        created_at = datetime.datetime.utcnow().isoformat()

        table = dynamodb.Table(DYNAMODB_TABLE)

        table.put_item(
            Item={
                'email': email,
                'post_id': post_id,
                'title': title,
                'created_at': created_at
            }
        )

        # Return success response
        return {
            'statusCode': 201,
            'message': f'Post created successfully with id: {post_id}'
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'error': f'Internal server error: {str(e)}'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': f'An error occurred: {str(e)}'
        }
