import boto3
import json

dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Posts'
INDEX_NAME = 'email-created_at-index'

def get_posts_by_email(email):
    table = dynamodb.Table(DYNAMODB_TABLE)

    # Query using the GSI
    response = table.query(
        IndexName=INDEX_NAME,
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
    )

    return response['Items']

def lambda_handler(event, context):
    # Get the email from query string parameters
    email = event.get('pathParameters', {}).get('email')

    if email:
        # Fetch posts by email using the DynamoDB function
        posts = get_posts_by_email(email)
        
        return {
            'statusCode': 200,
            'body': json.dumps(posts)
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Email parameter is required"})
        }

