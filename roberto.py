# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:53:30 2018

@author: Valenti
"""

import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import projections as pj
#import matplotlib as plt
import matplotlib.pyplot as plt


G = ox.load_graphml('networkRM_epgs4326.graphml')
charger1=(41.819110,  12.437210)
charger2=(41.809120, 12.445940)
charger3=(41.826840, 12.454720)

ch1_n = ox.get_nearest_node(G, charger1)
ch2_n = ox.get_nearest_node(G, charger2)
ch3_n = ox.get_nearest_node(G, charger3)
print(ch1_n, ch2_n, ch3_n)
df = pd.read_csv('rob.csv', sep=';')
s = list();
for i in range(len(df)):
   s.append(None)
df['distanza_ch1_mt']=s
df['distanza_ch2_mt']=s
df['distanza_ch3_mt']=s


for i in range(len(df)):
    print("{0:.1f}%".format(float(i)/len(df)*100))
    start =(float(df['latitudine'][i])/10**6, float(df['longitudine'][i])/10**6)
    from_n = ox.get_nearest_node(G, start)
    #print(from_n)
    lr1=nx.dijkstra_path_length(G, from_n, ch1_n, weight='length')
    lr2=nx.dijkstra_path_length(G, from_n, ch2_n, weight='length')
    lr3=nx.dijkstra_path_length(G, from_n, ch3_n, weight='length')
    df.at[i, 'distanza_ch1_mt'] = int(lr1)
    df.at[i, 'distanza_ch2_mt'] = int(lr2)
    df.at[i, 'distanza_ch3_mt'] = int(lr3)
    

print(df.shape)
df.to_csv('roberto.csv', sep=';',index=False)


'''
#print(df['longitudine'][0])
#load Graph
#G2 = ox.load_graphml('networkRM_epgs4326.graphml')
ch1 = ox.get_nearest_node(G, charger1)
ch2 = ox.get_nearest_node(G, charger2)
ch3 = ox.get_nearest_node(G, charger3)
'''