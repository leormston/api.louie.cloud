import json
import boto3

def return_format(statusCode, headers, body):
    return {
        'statusCode': statusCode,
        'headers': headers,
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': True,
        'mode': 'cors'
    }
    
    dynamodb = boto3.resource('dynamodb')
    paths = event['rawPath'].split("/")[1:]
    if len(paths) == 1:
        return "Hi from the louie.cloud API"
    else:
        if paths[1].lower() == "projects":
            table = dynamodb.Table('louie-cloud-projects')
            if len(paths) == 3:
                response = table.get_item(
                    Key={
                        'projectId': str(paths[2])
                    }
                )
                if "Item" in response:
                    data = response['Item']
                    return return_format(200, headers, data)
            else:
                response = table.scan()
                data = response['Items']
                return return_format(200, headers, data)
    
    return return_format(404, headers, "Resource with path not found.") 