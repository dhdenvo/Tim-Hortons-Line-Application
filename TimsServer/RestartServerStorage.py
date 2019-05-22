#Very basic program but it does the job since
print("Resetting the server storage file")
f = open("server_storage.csv", "w")
f.write("Day Of The Week,Date,Time,Number Of People")
f.close
print("Done Reset")