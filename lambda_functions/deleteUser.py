import json
import boto3


dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'

def lambda_handler(event, context):
    email = event['pathParameters'].get('email')  

    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Email path parameter is required"})
        }

    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
       
        response = table.delete_item(
            Key={'email': email}
        )

        return {
            "statusCode": 204,
            "message": "User deleted successfully"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Failed to delete user: {str(e)}"
        }
