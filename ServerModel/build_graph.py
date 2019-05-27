import matplotlib.pyplot as plt
import random
import seaborn as sns
import pandas as pd
import datetime

# Round all times to a half hour increment: Takes string x and returns modified string
def half_hour(x):
    if int(x[3:]) > 30:
        return str(int(x[0:2]))+":30"
    else:
        return str(int(x[0:2]))

# Validate wether time is in the appropriate hour of operation of Tim Horton's at 8200 Warden Ave
# Takes a string and returns modified string
def validate_time(x):
    time = x

    if int(time[0:2]) >= 7 and int(time[0:2]) < 12  and time[-2:] == "AM":
        return half_hour(x[0:-3])
    elif int(time[0:2]) < 5 and time[-2:] == "PM":
        return half_hour(x[0:-3])
    elif int(time[0:2]) == 12 and time[-2:] == "PM":
        return half_hour(x[0:-3])
    else:
        return None

# Creates numeric versions of times (ie: 7:30 -> 7.5), used to sort the data frame by time
# Takes string returns float
def create_sort_keys(x):
    hour = int(x.split(":")[0])
    if hour < 7:
        hour = hour + 12
    if ":" in x:
        hour = hour +.5

    return hour

# Set up a half hour incremented list of times from 7 - 5
time = []

for x in range(10):
    t = x+7

    if t > 12:
        t = t - 12

    time.append(str(t))
    time.append(str(t)+":30")

# Take the server stored data from user image uploads and aggregate it by time averaging customer
# counts per half half hour
user_data = pd.read_csv("server_storage.csv")
user_data = user_data[['Time', 'NumberOfPeople']]
user_data['Time'] = user_data['Time'].apply(validate_time)
user_data = user_data.dropna()
user_data = user_data.groupby('Time').mean().round()
user_data['NumberOfPeople'] = user_data['NumberOfPeople'].astype(int)
user_data = user_data.reset_index(level=0)

# Fills in missing times in the data frame with zero values
for x in time:
    if not x in user_data['Time'].unique():
        user_data.loc[user_data['Time'].shape[0]] = [x,0]

# Create sort keys to organize dataframe chronologically
user_data['SortKey'] = user_data['Time'].apply(create_sort_keys)
user_data = user_data.sort_values(by=['SortKey'])

# Bring in the predictions file
predictions = pd.read_csv("predictions.csv")

## Create plot that will be used in the app to show the actual and predicted number of people
plt.figure(figsize = (17,13))
plt.rcParams.update({'font.size': 45})
plt.margins(x=0)
plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
sns.despine(left=True, bottom=True, right=True)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

yticks = plt.gca().yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

bars = plt.bar(user_data['Time'], user_data['NumberOfPeople'],color = ("#cfebdf", "#c7f2a7"), width=1.0, label = 'Actual')
line = plt.plot(predictions['Time'], predictions['NumberOfPeople'], "r-", alpha = .4, label='Predicted')
plt.ylabel("People")
plt.xlabel("Time of Day")
plt.legend()
plt.title("People At Tims Today")

for i,item in enumerate(bars[::1]):

    height = item.get_height()
    plt.text(item.get_x() + item.get_width()/2, item.get_height()+.1, str(int(height)),
                 ha='center', color='black', fontsize=30)

plt.savefig("graph.png")
##

# Check if it is 5 P.M or later and save the days aggregated data 
if datetime.datetime.now().time().hour >= 17:
    user_data = user_data.drop('SortKey', axis = 1)
    user_data.to_csv("aggregated_data.csv")
