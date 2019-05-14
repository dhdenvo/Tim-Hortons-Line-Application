from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request
import json
import datetime
import requests

#Defining The API Application
app = Flask(__name__)
api = Api(app)

#Server information
server_file = "server_data.dat"
api_url = "https://p10a156.pbm.ihost.com/powerai-vision/api/dlapis/7342cc0c-85aa-46bb-994f-f438cddb212e"
server_url = "http://127.0.0.1:5000/data"

# Create a URL route in the application for "/"
@app.route('/')

#The class that contains all of the rest api calls
#If a function is missing then it is qualified as not allowed for the url
class User(Resource):
    #Run when recieve a get rest api call
    #Reads off the data from the server file
    def get(self):
        server_data = open(server_file, 'r')  
        data = server_data.read()
        server_data.close()
        return data
    
    #Run when recieve a put rest api call
    #Writes the call arguments to the server file    
    def put(self):
        #Grabs the arguments from the call
        args = request.args
        data = args["data"]
        #Writes the arguments to the server file
        server_data = open(server_file, 'w')  
        server_data.write(data)
        server_data.close()
        return data
    
    #Run when recieve a post rest api call
    def post(self):
        #Grabs the time when the post call is made
        img_time = datetime.datetime.now()      
        #Sends an api call to AI Vision
        req = requests.post(url = api_url, files=request.files, verify=False)       
        response = json.loads(req.text)
        #Checks the amount of people in the line
        amount_in_line = len(response['classified'])
        #Builds the put call's parameters using the amount of people in line and the time of the original call        
        img_time = "Date: " + img_time.strftime("%a, %b %d, %Y") + " & Time: " + img_time.strftime("%I:%M:%S %p")
        server_data = "Number Of People: %d & " % amount_in_line + img_time
        #Sends a put call to itself
        server_req = requests.put(url = server_url, params={"data": server_data})
    
#Runs the rest api application
api.add_resource(User, "/data")
app.run(host='0.0.0.0', port=8286, debug=True)