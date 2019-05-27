import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

# Convert time of day to numeric representation
def time_to_number(x):
    hour = x

    if ':' in hour:
        hour = int(x.split(':')[0])
        hour = hour +.5

    return float(hour)

# Get the daily customer data and process it to be used for training
def get_data():
    x = pd.read_csv("aggregated_data.csv")
    x['Date'] = pd.to_datetime(x['Date'])
    x['Month'] = x['Date'].dt.month.astype(int)
    x = x.drop(['Date',"Unnamed: 0", "Longitude", "Latitude"], axis=1)
    x["Time"] = x["Time"].apply(time_to_number)
    x = x[x['DayOfTheWeek'] > 0]
    x = x[x['DayOfTheWeek'] < 6]
    return x

# Load up data and seperate into features and target variables
customers = get_data()
customers = customers.drop(['Temperature'], axis = 1)
X = customers.drop('NumberOfPeople', axis=1)
y = customers['NumberOfPeople']


# Load up the model
filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# Train the model
loaded_model.fit(X,y)

# Save the model
pickle.dump(loaded_model, open(filename, 'wb'))
