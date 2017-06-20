import os
import sys
import json

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
import fitbit

sys.path.append(os.path.join(here, "./mymodules"))
from MyFitbitModule import FitbitToken

CLIENT_ID       = '228DDF'
TABLE_NAME      = 'fitbit_token'

def handler(event, context):
    ft = FitbitToken(CLIENT_ID, TABLE_NAME)
    client = ft.set_client()

    ts = client.time_series(resource='activities/heart', period='1d')
    return ts
