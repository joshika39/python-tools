import requests
import json

api_key = "baee0492ff2cb6bf8a5ff7e340d2ac92"

test = requests.get('https://api.scripture.api.bible/v1/bibles', headers={'api-key': api_key})

bibles = json.loads(test.content)['data']

for bible_data in bibles:
    if bible_data['language']['id'] == "eng":
        print(bible_data['name'])
