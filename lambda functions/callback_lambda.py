# not needed in lambda:
from dotenv import load_dotenv
from utils_layer.python import utils 
# needed in lambda:
import os
import base64
import requests
import utils

client_id: str = os.environ['SPOTIFY_CLIENT_ID']
client_secret: str = os.environ['SPOTIFY_CLIENT_SECRET']
redirect_uri: str = utils.redirect_uri

def lambda_handler(event: any, context: any):
    if 'code' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': "{'error': 'Missing code parameter'}",
        }

    authorization_code: str = event['queryStringParameters']['code']
    form = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
    }

    auth_client: str = f"{client_id}:{client_secret}"
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': f"Basic {base64.b64encode(auth_client.encode()).decode()}",
    }

    response = requests.post(url = "https://accounts.spotify.com/api/token", data = form, headers = headers)

    if response.status_code == 200:
        return_response = {
            'statusCode': response.status_code,
            'body': response.text,
        }
    else:
        return_response = {
            'statusCode': response.status_code,
            'body': response.text,
        }

   
    return return_response


if __name__ == "__main__":
    load_dotenv()

    event = {} # test case

    print(lambda_handler(event, None))
