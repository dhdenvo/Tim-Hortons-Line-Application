#https://p10a156.pbm.ihost.com/powerai-vision/api/dlapis/7342cc0c-85aa-46bb-994f-f438cddb212e
import json
import requests
import datetime

api_url = "https://p10a156.pbm.ihost.com/powerai-vision/api/dlapis/7342cc0c-85aa-46bb-994f-f438cddb212e"
img = "test.jpg"
file = open(img, "rb")
img_time = datetime.datetime.now()

req = requests.post(url = api_url, files={"files": (img, file)}, verify=False)

#print(req)
response = json.loads(req.text)
print(response)
#print(response['classified'])
#print(len(response['classified']))

amount_in_line = len(response['classified'])
img_time = "Date: " + img_time.strftime("%a, %b %d, %Y") + " & Time: " + img_time.strftime("%I:%M:%S %p")
server_data = "Number Of People: %d & " % amount_in_line + img_time

server_url = "http://127.0.0.1:5000/data"
server_req = requests.put(url = server_url, params={"data": server_data})
#print(server_req)
#print(json.loads(server_req.text))
#print(server_url)



