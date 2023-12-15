# not needed in lambda:
from dotenv import load_dotenv
from utils_layer.python import utils 
# needed in lambda:
import os
import os
import base64
import json
import requests
import utils

client_id: str = os.environ['SPOTIFY_CLIENT_ID']
client_secret: str = os.environ['SPOTIFY_CLIENT_SECRET']
aes_key:str = os.environ['AES_KEY']
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
        raw_json = response.json()
        return_json = {}

        encrypted_access_token, nonce = utils.encrypt_text(raw_json['access_token'], aes_key)
        return_json['access_token'] = encrypted_access_token.hex()
        return_json['nonce'] = nonce.hex()

        return_response = {
            'statusCode': response.status_code,
            'body': json.dumps(return_json),
        }
    else:
        return_response = {
            'statusCode': response.status_code,
            'body': response.text,
        }

   
    return return_response


if __name__ == "__main__":
    load_dotenv()

    event = {'queryStringParameters': {'code': "abc"}} # test case

    print(lambda_handler(event, None))
