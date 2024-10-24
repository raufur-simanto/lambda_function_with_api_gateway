import json
import boto3

dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'

def lambda_handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        response = table.scan()
        users = response.get('Items', [])

        for user in users:
            del user["password_hash"]
        
        return {
            "statusCode": 200,
            "body": json.dumps(users)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to retrieve users: {str(e)}"})
        }
