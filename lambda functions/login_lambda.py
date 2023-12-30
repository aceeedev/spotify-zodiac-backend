import os
import urllib.parse
import utils

client_id: str = os.environ['SPOTIFY_CLIENT_ID']
redirect_uri: str = utils.redirect_uri

def lambda_handler(event: any, context: any):
    scope = 'user-read-private%20user-read-email%20user-top-read'
    query = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    }

    url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query)}&scope={scope}"

    # redirect to Spotify and sends back to the client for callback
    return {
        'statusCode': 301,
        'headers': {'Location': url}
    }