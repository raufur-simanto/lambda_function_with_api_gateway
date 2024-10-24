import json
import boto3
import uuid
import hashlib
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def lambda_handler(event, context):
    try:
        username = event['username']
        email = event['email']
        password = event['password']

        
        password_hash = hash_password(password)
        user_id = str(uuid.uuid4())

        table = dynamodb.Table(DYNAMODB_TABLE)

        # Check if user already exists
        try:
            response = table.get_item(Key={'email': email})
            print(response)
            if 'Item' in response:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Username already exists'})
                }
        except ClientError as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Internal server error: ' + str(e)})
            }

        table.put_item(
            Item={
                'username': username,
                'email': email,
                'password_hash': password_hash,  
                'user_id': user_id,
                'status': 'active'  
            }
        )

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'User registered successfully!'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred: ' + str(e)})
        }
