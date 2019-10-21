
import os
# check working directory
cwd = os.getcwd()
# change working directoy
os.chdir('C:/python/projects/giraffe/viasat_data')
cwd = os.getcwd()
cwd

import psycopg2
import db_connect
from sklearn.metrics import silhouette_score
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import math
import pandas as pd
import csv
import datetime

filename = 'C:\python\projects\giraffe\viasat_data\VST_ENEA_CT_20190411_150502.csv'

'''
# # copy data from .csv file directly into the db
# cur = conn.cursor()
# f = open(r'C:\python\projects\giraffe\viasat_data\VST_ENEA_CT_20190411_150502_no_timestamp.csv', 'r')
# # f = open(r'C:\python\projects\giraffe\viasat_data\VST_ENEA_CT_20190411_150502.csv', 'r')
# cur.copy_from(f, 'viasat_py_temp', sep=',')
# f.close()
# conn.commit()
'''

# open db from PostgreSQL

#Connect to an existing database
conn=db_connect.connect_viasat()
cur = conn.cursor()

# select few fields
cur.execute("SELECT deviceId, longitude,Latitude, datetime FROM public.viasat_py_temp")
# make a dataframe
table=pd.DataFrame(cur.fetchall(),columns=['deviceId','longitude','Latitude', "datetime"])

#################################################################
######### COLUMN NAMES ##########################################
#################################################################
# If you just want the COLUMN NAMES
cur.execute("SELECT * FROM public.viasat_py_temp LIMIT 0")
colnames_db = [desc[0] for desc in cur.description]
type(colnames_db)
################################################################
################################################################

# filtering by date
cur.execute("SELECT * FROM public.viasat_py_temp WHERE datetime BETWEEN '2019-04-11 12:24:27' AND '2019-04-11 12:40:00' ")
# make a dataframe
table=pd.DataFrame(cur.fetchall(), columns= colnames_db)


# Select all rows
cur.execute("SELECT * FROM public.viasat_py_temp")
# make a dataframe
table=pd.DataFrame(cur.fetchall(),columns= colnames_db)


# cur.execute("SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('public.viasat_py_temp')")


print("Print each row and it's columns values")
cur.execute("SELECT * FROM public.viasat_py_temp")
table_by_records=cur.fetchall()
for row in table_by_records:
       print("deviceId = ", row[0], )
       print("datatime = ", row[1])
       print("Latitude  = ", row[2],
       print("longitude = ", row[3]),"\n")


# https://pynative.com/python-postgresql-select-data-from-table/

# count number of vehicles by ID
cur.execute("SELECT deviceid, count(deviceid) "
            "FROM public.viasat_py_temp"
            " group by deviceid")
table=pd.DataFrame(cur.fetchall())


cur.execute("SELECT deviceid,speedkmh, count(deviceid)"
            " FROM public.viasat_py_temp"
            " group by deviceid, speedkmh")
df=pd.DataFrame(cur.fetchall())

conn.close()
cur.close()
