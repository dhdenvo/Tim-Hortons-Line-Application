from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

server_file = "server_data.dat"

# Create a URL route in the application for "/"
@app.route('/')


class User(Resource):
    def get(self, data):
        server_data = open(server_file, 'r')  
        data = server_data.read()
        server_data.close()
        return data
    
    def put(self, data):
        #data = request.get_json(force=True)
        server_data = open(server_file, 'w')  
        server_data.write(data)
        server_data.close()
        return data
    
    def post(self, data):
        pass    
    
    def delete(self, data):
        pass

api.add_resource(User, "/<string:data>")
#api.add_resource(User, "/")
app.run(debug=True)