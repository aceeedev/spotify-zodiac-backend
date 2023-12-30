import os
import hashlib
import boto3
import requests
import utils

aes_key:str = os.environ['AES_KEY']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SPOTIFY_ZODIAC')

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
    elif 'house' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': "{'error': 'Missing house parameter'}",
        }
    
    encrypted_access_token: str = bytes.fromhex(event['queryStringParameters']['access_token'])
    nonce: str = bytes.fromhex(event['queryStringParameters']['nonce'])
    
    accessToken = utils.decrypt_text(encrypted_access_token, aes_key, nonce)

    headers = {
      'Authorization': f"Bearer {accessToken}"
    }
    
    response = requests.get(url = 'https://api.spotify.com/v1/me', headers = headers)

    hashed_account_id = None

    if response.status_code == 200:
        raw_json = response.json()

        raw_account_id = raw_json['id']
        hashed_account_id = hashlib.sha256(raw_account_id.encode()).hexdigest()
    else:
        return {
            'statusCode': response.status_code,
            'body': 'c',
        }
    
    # check if user has already submitted before
    # TODO: ^^^
    
    query = {
        'limit': 50,
        'offset': 0,
        'time_range': 'long_term'
    }
    
    response = requests.get(url = 'https://api.spotify.com/v1/me/top/tracks', headers = headers, params = query)

    track_ids = ''
    track_count = 0
    if response.status_code == 200:
        raw_json = response.json()

        for song in raw_json['items']:
            track_ids += f"{song['id']},"
            track_count += 1

        track_ids = track_ids[:-1]

    else:
        return {
            'statusCode': response.status_code,
            'body': 'b',
        }
        
    query = {
        'ids': track_ids
    }
    
    response = requests.get(url = 'https://api.spotify.com/v1/audio-features', headers = headers, params = query)

    if response.status_code == 200:
        raw_json = response.json()
        
        i = 0
        for audio_features in raw_json['audio_features']:
            for key, value in audio_features.items():
                if isinstance(value, float):
                    raw_json['audio_features'][i][key] = str(value)
                    
            i += 1
                
        formatted_json = raw_json
        formatted_json['Account_id'] = hashed_account_id
        formatted_json['house'] = int(event['queryStringParameters']['house'])
        formatted_json['count'] = track_count
        
        table.put_item(Item=formatted_json)
        
        return {
            'statusCode': 200,
            'headers': {
                'access-control-allow-origin': 'https://astrolify.netlify.app',
            },
            'body': 'success',
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': 'a',
        }