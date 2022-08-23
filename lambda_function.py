import json
import boto3
import logging
from custom_encorder import CustomEncorder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'AcholiWords'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
healthPath = '/health'
wordPath = '/word'

def lambda_handler(event, context):    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == wordPath:
        response = getWord(event['queryStringParameters']['word'])
    elif httpMethod == postMethod and path == wordPath:
        response = postWord(json.loads(event['body']))
    else:
        response = buildResponse(404, 'not found')

    return response


def getWord(wordSearch):
    try:
        response = table.get_item(
            Key = {
                'word': wordSearch
            }
        )
        if 'Item' in response:            
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'message': 'word not found'})
    except:
        logger.exception('an error occured with get request, please contact your admin')


def postWord(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(201, body)
    except:
        logger.exception('an error occured with post request, please contact your admin')


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncorder)
    return response