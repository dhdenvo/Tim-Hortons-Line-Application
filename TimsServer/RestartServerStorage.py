#Very basic program but it does the job since
print("Resetting the server storage file")
f = open("server_storage.csv", "w")
f.write("Date,DayOfThe Week,Temperature,Weather,Time,NumberOfPeople,Longitude,Latitude")
f.close
print("Done Reset")