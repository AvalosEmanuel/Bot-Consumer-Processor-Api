import logging
import json
import boto3
from botocore.exceptions import ClientError
from send_logs import update_cloudwatch

def get_secret():
    "Retrieves the API_KEY required for connection to the Alchemy node"
    secret_name = "Alchemy_Key"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            logging.error('DecryptionFailureException')
            update_cloudwatch('DecryptionFailureException')
            raise e
            
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            logging.error('InternalServiceErrorException')
            update_cloudwatch('InternalServiceErrorException')
            raise e

        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logging.error('InvalidParameterException')
            update_cloudwatch('InvalidParameterException')
            raise e

        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logging.error('InvalidRequestException')
            update_cloudwatch('InvalidRequestException')
            raise e

        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            update_cloudwatch('ResourceNotFoundException')
            raise e

    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString'] 

    alchemy_api_key = json.loads(secret)
    return alchemy_api_key['AlchemyKey']