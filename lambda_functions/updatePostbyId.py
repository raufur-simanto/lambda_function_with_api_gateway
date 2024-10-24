import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Posts'

def lambda_handler(event, context):
    post_id = event.get('pathParameters', {}).get('post_id')
    
    
    body = json.loads(event.get('body', '{}'))
    title = body.get('title')  

    
    if not post_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "post_id is required"})
        }

   
    if not title:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "title is required"})
        }

   
    table = dynamodb.Table(DYNAMODB_TABLE)

    
    try:
        response = table.update_item(
            Key={'post_id': post_id},
            UpdateExpression="set title = :t",
            ExpressionAttributeValues={
                ':t': title
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
        "statusCode": 200,
        "body": json.dumps({"message": "post is updated"})
    }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Failed to update post: {str(e)}"
        }
