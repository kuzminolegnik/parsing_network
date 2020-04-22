import requests
from getpass import getpass
import json

username = input('Please enter users name: ')
password = getpass('Please enter users password: ')

response = requests.get('https://api.github.com/user', auth=(username, password))
data = response.json()

print(data["repos_url"])
response = requests.get(data["repos_url"])

with open('result.json', 'w') as json_file:
    json.dump(response.json(), json_file)