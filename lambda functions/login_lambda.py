# not needed in lambda:
from dotenv import load_dotenv
from utils_layer.python import utils 
# needed in lambda:
import os
import urllib.parse
import utils

client_id: str = os.environ['SPOTIFY_CLIENT_ID']
redirect_uri: str = utils.redirect_uri

def lambda_handler(event: any, context: any):
    scope = ''
    query = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
    }

    url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query)}"

    # redirect to Spotify and sends back to the client for callback
    return {
        'statusCode': 301,
        'headers': {'Location': url}
    }


if __name__ == "__main__":
    load_dotenv()

    event = {} # test case

    print(lambda_handler(event, None))
