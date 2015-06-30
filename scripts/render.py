import json
import requests


with open('README.md', 'r') as readme:
    text = readme.read()
payload = json.dumps({'text': text})
response = requests.post('https://api.github.com/markdown', data=payload)
with open('index.html', 'w+') as index_html:
    index_html.write(response.text)
