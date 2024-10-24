import json
import boto3

dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Posts'

def lambda_handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        response = table.scan()
        posts = response.get('Items', [])
        
        return {
            "data": posts
        }, 200

    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Failed to retrieve posts: {str(e)}"
        }
