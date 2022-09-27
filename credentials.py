import pickle
from google.auth.transport.requests import Request

def google_api_credentials(token_file):
    _credentials = None

    try:
        with open(token_file, 'rb') as token:
            _credentials = pickle.load(token)

        if _credentials and _credentials.expired and _credentials.refresh_token:
            _credentials.refresh(Request())
            print("Authentication credentials refresh.")
            with open(token_file, 'wb') as token:
                pickle.dump(_credentials, token) # refreshed credentials save

    except Exception as e:
        print(e)
        assert()

    return _credentials

if __name__ == '__main__':
    _creds = google_api_credentials("token.pickle")
