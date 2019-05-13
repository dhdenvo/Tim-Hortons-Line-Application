import json
import requests
import datetime

api_url = "http://127.0.0.1:5000/data"
img = "test.jpg"
file = open(img, "rb")
img_time = datetime.datetime.now()

req = requests.post(url = api_url, files={"files": (img, file)}, verify=False)
response = json.loads(req.text)
print(response)