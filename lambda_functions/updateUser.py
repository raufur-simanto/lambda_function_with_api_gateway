import json
import boto3


dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = 'Users'

def lambda_handler(event, context):
    email = event['pathParameters'].get('email') 
    update_data = json.loads(event.get('body', '{}'))

    if not email:
        return {
            "statusCode": 400,
            "error": "Email path parameter is required"
        }
    
    if not update_data:
        return {
            "statusCode": 400,
            "error": "No update data provided"
        }

    table = dynamodb.Table(DYNAMODB_TABLE)

    try:
        
        update_expression = "SET "
        expression_attribute_values = {}

        for key, value in update_data.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value

        
        update_expression = update_expression.rstrip(', ')

       
        table.update_item(
            Key={'email': email},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User updated successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Failed to update user: {str(e)}"
        }
