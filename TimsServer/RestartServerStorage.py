import os

#Very basic program but it does the job since
print("Resetting the server storage file")
f = open("server_storage.csv", "w")
f.write("Date,DayOfTheWeek,Time,NumberOfPeople,Latitude,Longitude")
f.close
print("Done Reset")

for graph in os.listdir("./Graphs/"):
    print(graph)
    if os.path.isfile("./Graphs/" + graph) and graph != "NoGraph.png":
        os.remove("./Graphs/" + graph)
        print("File Removed!")