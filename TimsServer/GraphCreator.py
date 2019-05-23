import matplotlib.pyplot as plt
import random
import seaborn as sns
import pandas as pd
import datetime

# Round values to half hour
def half_hour(x):
    if int(x[3:]) > 30:
        return str(int(x[0:2]))+":30"
    else:
        return str(int(x[0:2]))

#Make sure times are valid for Tim Horton's hours
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

#Create number values to sort the dataframe
def create_sort_keys(x):
    hour = int(x.split(":")[0])
    if hour < 7:
        hour = hour + 12
    if ":" in x:
        hour = hour +.5

    return hour

# Create time array to check for missing times in user data
time = []

for x in range(10):
    t = x+7

    if t > 12:
        t = t - 12

    time.append(str(t))
    time.append(str(t)+":30")

# Import and process user data
user_data = pd.read_csv("server_storage.csv")
user_data = user_data[['Time', 'Number Of People']]
user_data['Time'] = user_data['Time'].apply(validate_time)
user_data = user_data.dropna()
user_data = user_data.groupby('Time').mean().round()
user_data['Number Of People'] = user_data['Number Of People'].astype(int)
user_data = user_data.reset_index(level=0)

for x in time:
    if not x in user_data['Time'].unique():
        user_data.loc[user_data['Time'].shape[0]] = [x,0]

user_data['SortKey'] = user_data['Time'].apply(create_sort_keys)
user_data = user_data.sort_values(by=['SortKey'])

# Get model prediction data
predictions = pd.read_csv("predictions.csv")

# Create Dashboard of data for app and save it
plt.figure(figsize = (16,10))
plt.rcParams.update({'font.size': 45})
plt.margins(x=0)
plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
sns.despine(left=True, bottom=True, right=True)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

yticks = plt.gca().yaxis.get_major_ticks()
yticks[0].label1.set_visible(False)

bars = plt.bar(user_data['Time'], user_data['Number Of People'],color = ("#cfebdf", "#c7f2a7"), width=1.0, label = 'Actual')
line = plt.plot(predictions['Time'], predictions['Number Of People'], "r-", alpha = .4, label='Predicted')
plt.ylabel("People")
plt.xlabel("Time of Day")
plt.legend()
plt.title("People At Tims Today")

for i,item in enumerate(bars[::1]):

    height = item.get_height()
    plt.text(item.get_x() + item.get_width()/2, item.get_height()+.1, str(int(height)),
                 ha='center', color='black', fontsize=30)

plt.savefig("graph.png")

if datetime.datetime.now().time().hour >= 16:
    user_data = user_data.drop('SortKey', axis = 1)
    user_data.to_csv("end_of_data.csv")
