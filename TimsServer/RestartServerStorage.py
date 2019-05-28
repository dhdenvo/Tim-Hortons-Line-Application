#Very basic program but it does the job since
print("Resetting the server storage file")
f = open("server_storage.csv", "w")
f.write("Date,DayOfTheWeek,Time,NumberOfPeople,Latitude,Longitude")
f.close
print("Done Reset")