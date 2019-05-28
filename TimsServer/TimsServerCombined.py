from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
import signal
import json
import datetime
import requests
import base64
import os

#Defining The API Application
app = Flask(__name__)
cors = CORS(app, origins="*")
api = Api(app)

def get_latlng(request, precision):
    #Get the parameters from the request
    long = request.args.get("long")
    lat = request.args.get("lat")

    #If one of the lat or long are not existent or they are in the radius of the default return the defaults
    if not long or not lat or (long in def_long_range and lat in def_long_range) or \
       (not long.replace(".", "", 1).replace("-", "", 1).isdigit()) or (not lat.replace(".", "", 1).replace("-", "", 1).isdigit()):
        long, lat = def_long, def_lat
    return round(float(lat), precision), round(float(long), precision)

#Create a radius around the longitude and latitude given
def get_coor_range(lat, long, radius, precision):
    #Create a list based on the radius and the precision for each longitude and latitude
    long_range = list(range(int(long * (10 ** precision) - radius), int(long * (10 ** precision) + radius)))
    lat_range = list(range(int(lat * (10 ** precision) - radius), int(lat * (10 ** precision) + radius)))
    #Make the ranges back into floats rather than large integers
    lat_range = [x / float(10 ** precision) for x in lat_range]
    long_range = [x / float(10 ** precision) for x in long_range]
    return lat_range, long_range

#Convert military time to twelve hour clock
def convert_mil_to_twelve(military):
    #Split between hour and minute
    hour = int(military.split(":")[0])
    #Calculate whether it is AM or PM
    twelve = "AM"
    if hour >= 12:
        twelve = "PM"
        hour -= 12
    #Return the twelve hour time
    return str(hour) + ":" + military.split(":")[1] + " " + twelve
    

#Server information
server_file = "server_data.dat"
storage_file = "server_storage.csv"
api_url = "https://p10a156.pbm.ihost.com/powerai-vision/api/dlapis/7342cc0c-85aa-46bb-994f-f438cddb212e"
server_url = "http://127.0.0.1:5000/data"
website_server_file = "../../../../var/www/html/TimsLine/server_data.dat"
website = True
auto_reset = True
location_precision = 3
#The location of 8200 Warden Lab
def_lat, def_long = 43.849027, -79.339243
def_lat_range, def_long_range = get_coor_range(def_lat, def_long, 3, location_precision)

# Create a URL route in the application for "/"
@app.route('/')

#The class that contains all of the rest api calls
#If a function is missing then it is qualified as not allowed for the url
class User(Resource):
    #Run when recieve a get rest api call
    #Reads off the data from the server file
    def get(self):
        #If a get request is made when it is 6 pm, the server shuts down
        #This is done so after 6 pm, the server shuts down
        if datetime.datetime.now().hour == 18 and auto_reset:
            os.kill(os.getpid(), signal.SIGINT)
        #Get the long and lat of the client
        lat, long = get_latlng(request, location_precision)
        
        #Find the server data and return it to the client
        server_data = open(storage_file, 'r')  
        data = server_data.read()
        server_data.close()
        
        #Break apart the storage data
        data_list = []
        for line in data.split("\n"):
            data_list.append(line.split(","))
        #Remove the last item if it is empty (trailing \n line in file)
        if data_list[-1] == ['']:
            data_list = data_list[:-1]
        #Remove header line and reverse list
        data_list = data_list[1:][::-1]
        #print("Person Location " + str(long) + " " + str(lat))
        #Create the ranges for the coordinates (with a radius of 3)
        lat_range, long_range = get_coor_range(lat, long, 3, location_precision)
        #Iterate through the file checking if the locations match
        for line in data_list:
            if float(line[-2]) in lat_range and float(line[-1]) in long_range:
                return line[3] + "," + convert_mil_to_twelve(line[2])
        return "No Line,Data"

    #Run when recieve a put rest api call
    #Writes the call arguments to the server file    
    def put(self):
        #Grabs the arguments from the call
        args = request.args
        data = args["data"]
        
        #Writes the data to the server storage file
        server_data = open(storage_file, 'a+')
        server_data.write("\n" + data)
        server_data.close()
        print(data)
        
        #Writes the arguments to the server file for the website
        if website and data.split(",")[-2] == def_lat and data.split(",")[-1] == def_long:
            basic_data = data.split(",")[3] + "," + convert_mil_to_twelve(data.split(",")[2])      
            server_data = open(website_server_file, 'w')  
            server_data.write(basic_data)
            server_data.close()
        return data

    #Run when recieve a post rest api call
    def post(self):
        #Grabs the time when the post call is made
        img_time = datetime.datetime.now()
        
        #Get long and lat of the client
        lat, long = get_latlng(request, location_precision)

        #Get the values from the request
        val = list(request.files.values())
        
        #On Android
        if val == []:
            val = list(request.values.values())
        
            if val == []:
                return "No Image Sent"
        
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
        img_time_str = img_time.strftime("%H:%M")
        img_day_str = img_time.strftime("%Y-%m-%d")        
        week_day = img_time.weekday() + 1
        
        if week_day == 7: 
            weekday -= 7
        
        server_data = img_day_str + ",%d," % week_day + img_time_str + ",%d," % amount_in_line + str(lat) + "," + str(long)
        
        #Sends a put call to itself
        server_req = requests.put(url = server_url, params={"data": server_data})
        return server_data

#Runs the rest api application
api.add_resource(User, "/data")
app.run(host='0.0.0.0', debug=True)
#app.run(debug=True)
