import os
import json
import requests
import utils

aes_key:str = os.environ['AES_KEY']

def lambda_handler(event: any, context: any):
    if 'access_token' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': "{'error': 'Missing access_token parameter'}",
        }
    elif 'nonce' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': "{'error': 'Missing nonce parameter'}",
        }
    elif 'uri' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': "{'error': 'Missing uri parameter'}",
        }
    
    encrypted_access_token: str = bytes.fromhex(event['queryStringParameters']['access_token'])
    nonce: str = bytes.fromhex(event['queryStringParameters']['nonce'])
    
    accessToken = utils.decrypt_text(encrypted_access_token, aes_key, nonce)

    headers = {
      'Authorization': f"Bearer {accessToken}"
    }
    
    query = {
        'market': 'US'
    }
    
    response = requests.get(url = f"https://api.spotify.com/v1/playlists/{event['queryStringParameters']['uri']}", headers = headers, params = query)

    if response.status_code == 200:
        raw_json = response.json()
        return_json = {}
        
        return_json['name'] = raw_json['name']
        return_json['description'] = raw_json['description']
        return_json['image'] = raw_json['images'][0]['url']
        return_json['house'] = (ord(raw_json['name'][0]) % 12) + 1

        return {
            'statusCode': 200,
            'headers': {
                'access-control-allow-origin': 'https://astrolify.netlify.app',
            },
            'body': json.dumps(return_json),
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': response.text,
        }
        