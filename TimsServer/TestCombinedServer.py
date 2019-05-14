import json
import requests
import datetime

api_url = "http://drv-ctp6.canlab.ibm.com/:5000/data"
get = False

if (get):
    req = requests.get(url = api_url)
else:    
    img = "test.jpg"
    file = open(img, "rb")
    img_time = datetime.datetime.now()
    req = requests.post(url = api_url, files={"files": (img, file)}, verify=False)
    
print(req)
response = json.loads(req.text)
print(response)