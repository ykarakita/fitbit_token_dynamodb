import sys
import os
import boto3
from ast import literal_eval

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))
import fitbit

class FitbitToken:
    def __init__(self, CLIENT_ID, TABLE_NAME):
        self.CLIENT_ID = CLIENT_ID

        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(TABLE_NAME)

    def set_client(self):
        items = self.get_token()
        client = fitbit.Fitbit(
            client_id     = self.CLIENT_ID,
            client_secret = items['Item']['secret'],
            access_token  = items['Item']['access_token'],
            refresh_token = items['Item']['refresh_token'],
            expires_at    = float(items['Item']['expires_at']),
            refresh_cb    = self.update_token,
            system        = 'ja_JP'
        )
        return client

    def get_token(self):
        item = self.table.get_item(
            Key={
                "id": self.CLIENT_ID
            }
        )
        return item

    def update_token(self, token):
        token_dict = literal_eval(str(token))
        res = self.table.update_item(
            Key = {
                "id": self.CLIENT_ID
            },
            AttributeUpdates = {
                'refresh_token':{
                    'Action': 'PUT',
                    'Value': token_dict['refresh_token']
                },
                'access_token': {
                    'Action': 'PUT',
                    'Value': token_dict['access_token']
                },
                'expires_at': {
                    'Action': 'PUT',
                    'Value': str(token_dict['expires_at'])
                }
            }
        )
        return 
