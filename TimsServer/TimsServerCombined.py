from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
import json
import datetime
import requests
import base64

#Defining The API Application
app = Flask(__name__)
cors = CORS(app, origins="*")
api = Api(app)


#Server information
server_file = "server_data.dat"
storage_file = "server_storage.csv"
api_url = "https://p10a156.pbm.ihost.com/powerai-vision/api/dlapis/7342cc0c-85aa-46bb-994f-f438cddb212e"
server_url = "http://127.0.0.1:5000/data"
website_server_file = "../../../../var/www/html/TimsLine/server_data.dat"
website = True

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
        basic_data = data.split(",")[3] + "," + data.split(",")[2]
        
        #Writes the arguments to the server file
        server_data = open(server_file, 'w')  
        server_data.write(basic_data)
        server_data.close()
        
        server_data = open(storage_file, 'a+')
        server_data.write("\n" + data)
        server_data.close()
        print(data)
        
        #Writes the arguments to the server file for the website
        if website:
            server_data = open(website_server_file, 'w')  
            server_data.write(basic_data)
            server_data.close()
        return data

    #Run when recieve a post rest api call
    def post(self):
        #Grabs the time when the post call is made
        img_time = datetime.datetime.now()

        #Get the values from the request
        val = list(request.files.values())
        
        #On Android
        if val == []:
            val = list(request.values.values())
        
            #Compensate for any missing padding
            #Should not be required anymore but still good to keep to be safe
            pad = 4 - (len(val[0]) % 4)
            if pad == 4:
                pad = 0
    
            #Decodes the image with base 64	
            image = base64.b64decode(val[0] + "=" * pad)
            files = {"files": ('image.jpg', image)}
        
        #On IOS
        else:
            files = {"files": ('image.jpg', val[0].read())}
            
        #Uncomment below and comment above if doing it from non application
        #files = request.files

        #Save the photo (comment out normally)
        '''f = open("image.jpg", "wb")
	f.write(image)
	f.close()'''

        #Sends an api call to AI Vision
        req = requests.post(url = api_url, files=files, verify=False)       
        response = json.loads(req.text)

        #Checks the amount of people in the line
        amount_in_line = len(response['classified'])
        
        #Builds the put call's parameters using the amount of people in line and the time of the original call        
        img_time_str = img_time.strftime("%d/%m/%Y,%I:%M %p")
        week_day = img_time.weekday() + 2
        if week_day > 7: 
            weekday -= 7
        server_data = "%d," % week_day + img_time_str + ",%d" % amount_in_line
        
        #Sends a put call to itself
        server_req = requests.put(url = server_url, params={"data": server_data})
        return server_data

#Runs the rest api application
api.add_resource(User, "/data")
app.run(host='0.0.0.0', debug=True)
#app.run(debug=True)
