#Very basic program but it does the job since
print("Resetting the server storage file")
f = open("server_storage.csv", "w")
f.write("Date,Day Of The Week,Temperature,Weather,Time,Number Of People,Longitude,Latitude")
f.close
print("Done Reset")