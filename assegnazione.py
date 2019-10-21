# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:06:05 2018

@author: Valenti
"""


import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import projections as pj
import csv
#import matplotlib as plt
import matplotlib.pyplot as plt
#conta righe in file di input
lines = 0
with open("odday27_11_2015_test.csv", 'r') as fin:
    for line in fin:
        lines = lines + 1
fin.close
print("travel number:",lines)
sep=';'
G = ox.load_graphml('networkRM_Provincia_60km_epgs4326.graphml')
#aggiunta attributo flow
for u,v,key,attr in G.edges(keys=True,data=True):
    attr['flow']=0
    G.add_edge(u,v,key,attr_dict=attr)

with open("odday27_11_2015_out_test.csv", "w") as fout:
    with open("odday27_11_2015_test.csv", 'r') as fin:
        conta_righe=0
        fin.readline()   # skip the first line
        for line in fin:
            cells = line.split(";")     
            idtraj=cells[0]
            idterm=cells[1]
            from_coo=(float(cells[4])/(10**6),  float(cells[5])/(10**6))
            to_coo=(float(cells[6])/(10**6), float(cells[7])/(10**6))
            timedate=str(cells[8]) #2013-05-06 06:18:04;
            from_n = ox.get_nearest_node(G, from_coo)
            to_n = ox.get_nearest_node(G, to_coo)
            conta_righe+=1
            if (from_n != to_n):
                try:
                    route=nx.shortest_path(G,from_n,to_n,weight='cost')
                    path_edges = list (zip(route,route[1:]))
                    print("{0:.1f}%".format(conta_righe/lines*100))
                    for edg in path_edges:
                        data=G.get_edge_data(edg[0], edg[1], key=0)
                        data['flow']+=1
                        G.add_edge(edg[0],edg[1],0,attr_dict=data)
                    route_str = '_'.join(str(e) for e in route)
                    row=str(idtraj)+sep+str(idterm)+sep+route_str+sep+timedate
                    fout.write(row + '\n')
                except nx.NetworkXNoPath:
                    print('No path')
                    continue
fin.close
fout.close   
# save street network as GraphML file
ox.save_graphml(G, filename='networkRM_Provincia_60km_epgs4326_flow.graphml')
# save street network as ESRI shapefile
ox.save_graph_shapefile(G, filename='networkRM_Provincia_60kmFlow')
'''
G = ox.load_graphml('networkRM_Provincia_60km_epgs4326_flow.graphml')

from_n = ox.get_nearest_node(G, charger3)
to_n = ox.get_nearest_node(G, charger1)
route = nx.shortest_path(G,from_n,to_n,weight='length')
ox.plot_graph_route(G, route, route_color='green', fig_height=12, fig_width=12)
'''