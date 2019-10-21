
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

filename = "C:\\python\\projects\\giraffe\\viasat_data\\VST_ENEA_CT_20190411_150502.csv"

viasat_data = pd.read_csv(filename, header=0, parse_dates=[0], squeeze=True, skiprows=0)
print(viasat_data.head())

# verify if it is dataframe
print(type(viasat_data))
print(viasat_data.dtypes)

print(viasat_data.info())
print(viasat_data.columns)

# add headers
viasat_data.columns = ["idRequest","deviceId", "dateTime", "Latitude", "longitude",
              "speedKmh", "heading", "accuracyDop", "EngnineStatus", "Type", "Odometer"]

# field dateTime is a "type" object...but we want this as index (for the date_time structure)
# viasat_data.dateTime = pd.to_datetime(viasat_data.dateTime)
#
# viasat_data.set_index('dateTime', inplace=True)
# print(viasat_data.columns)
# print(viasat_data.head())
#
# viasat_data.plot(figsize=(15,10), linewidth=5, fontsize=20)
# plt.xlabel('dateTime', fontsize=20)
# plt.show()
#
# viasat_data[['speedKmh']].plot(figsize=(15,10), linewidth=5, fontsize=20)
# plt.xlabel('dateTime', fontsize=20)
# plt.show()

###########################################################################
