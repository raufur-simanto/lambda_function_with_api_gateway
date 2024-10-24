import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Posts'

def lambda_handler(event, context):
    post_id = event.get('pathParameters', {}).get('post_id')

    if not post_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "post_id is required"})
        }

   
    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        response = table.delete_item(
            Key={'post_id': post_id}
        )

        return {
            "statusCode": 204,
            "body": json.dumps({"message": "Post deleted successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to delete post: {str(e)}"})
        }
