import json
import boto3


dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'

def lambda_handler(event, context):
    email = event['pathParameters'].get('email')
    
    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Email query parameter is required"})
        }

   
    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        del user["password_hash"]

        if not user:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"})
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps(user)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to retrieve user: {str(e)}"})
        }
