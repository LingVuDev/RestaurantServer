import json

def get_google_credentials():
    try: 
        with open('src/login/google_credentials.json', 'r') as google_credentials:
            data = json.load(google_credentials)
            return data['web']
    except FileNotFoundError:
        print("No file google_credentials.json found. Please follow these instructions " + 
        "https://developers.google.com/identity/sign-in/web/sign-in to get the file")
