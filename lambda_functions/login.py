import json
import boto3
import hashlib
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def lambda_handler(event, context):
    try:
        email = event['email']              
        password = event['password']        
        
        password_hash = hash_password(password)

        
        table = dynamodb.Table(DYNAMODB_TABLE)

        
        try:
            response = table.get_item(Key={'email': email})
            if 'Item' not in response:
                return {
                    'statusCode': 400,
                    'error': 'User not found'
                }

            stored_password_hash = response['Item']['password_hash']

            if password_hash != stored_password_hash:
                return {
                    'statusCode': 401,
                    'error': f'Incorrect password'
                }

            return {
                'statusCode': 200,
                'message': 'Login successful'
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
