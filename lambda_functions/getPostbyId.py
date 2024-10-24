import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE = 'Posts'

def lambda_handler(event, context):
    try:
       
        post_id = event['pathParameters']['post_id']

        table = dynamodb.Table(DYNAMODB_TABLE)

        response = table.get_item(
            Key={
                'post_id': post_id
            }
        )

        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Or specific domain like 'http://localhost:3000'
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Post not found'})
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error: ' + str(e)})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred: ' + str})
        }
