#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 14:28:19 2018

@author: gaeval
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 14:55:30 2018

@author: gaeval
"""
#import osmnx as ox
#city = ox.gdf_from_place('Berkeley, California')
#ox.plot_shape(ox.project_gdf(city))

import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from dataview import DataView

#load Graph
import os
# os.chdir('C:\\giraffe\\viasat_data\\gv_net')
os.chdir('C:\\giraffe\\viasat_data\\reti_VALENTI\\gv_net')
os.getcwd()

#load Graph
Bracciano = ox.load_graphml('network_Bracciano_6km_epgs4326.graphml')
edge_file = Bracciano.edges(keys=True,data=True)


#way class: mean, max, min
way_dict={
        "residential" : [ 30 , 50 , 10 ],
        "secondary" :   [ 40 , 90 , 30 ],
        "primary" :     [ 50 , 70 , 20 ],
        "tertiary" :    [ 35 , 70 , 10 ],
        "unclassified" :[ 40 , 60 , 10 ],
        "secondary_link": [ 40 , 55 , 30 ],
        "trunk" :       [ 70 , 90 , 40 ],
        "tertiary_link": [ 35 , 50 , 30 ],
        "primary_link" : [ 50 , 90 , 40 ],
        "motorway_link": [ 80 , 100 , 30 ],
        "trunk_link" :   [ 42 , 70 , 40 ],
        "motorway" :     [ 110 , 130 , 40 ],
        "living_street": [ 20 , 50 , 30 ],
        "road" :         [ 30 , 30 , 30 ],
        "other" :         [ 30 , 30 , 30 ]
        }

#weigth/cost assignment
for u,v,key,attr in Bracciano.edges(keys=True,data=True):
    #select first way type from list    
    if type(attr["highway"]) is list:
       attr["highway"]=str(attr["highway"][0])
       #print(attr["highway"],'uuuuuuuuuuuuu')
    #verifica esistenza way tipe in dict
    if attr["highway"] not in way_dict.keys():
       speedlist=way_dict.get("other")
       speed=speedlist[0]*1000/3600
       attr['cost']=attr.get("length")/speed     
       #print(attr.get("highway"), speedlist[0], attr.get("cost"),'^^^^^^^^^^^')
       Bracciano.add_edge(u,v,key,attr_dict=attr)
       continue
    
    if 'maxspeed' in set(attr.keys()) and len(attr.get("maxspeed"))<4:
        if type(attr.get("maxspeed")) is list:
            speedList = [int(i) for i in attr.get("maxspeed")]
            speed=np.mean(speedList)*1000/3600  
            attr['cost']=attr.get("length")/speed
            #print(attr.get("highway"), attr.get("maxspeed"), attr.get("cost"),'========') 
        else: 
            speed=float(attr.get("maxspeed"))*1000/3600
            attr['cost']=attr.get("length")/speed            
            #print(attr.get("highway"), attr.get("maxspeed"), attr.get("cost"),'°°°°°°°°°') 
        Bracciano.add_edge(u,v,key,attr_dict=attr)
    else:#read speed from way class dictionary
        speedlist=way_dict.get(attr["highway"])
        speed=speedlist[0]*1000/3600
        attr['cost']=attr.get("length")/speed     
        #print(attr.get("highway"), speedlist[0], attr.get("cost"),'-----------')
        Bracciano.add_edge(u,v,key,attr_dict=attr)


#link paralleli (da più sorgenti) da rimuovere (Key > 1)
toberemoved=[]       
for u,v,key,attr in Bracciano.edges(keys=True,data=True):
    if key>0:
        data=Bracciano.get_edge_data(u,v)
        costo=0
        chiave=0
        for key, value in data.items():
            if(value['cost']>costo):
                  chiave=key
                  costo=value['cost']
        nome_tuple = (u, v, chiave)
        print(nome_tuple)
        toberemoved.append(nome_tuple)
for link in toberemoved:
    Bracciano.remove_edge(link[0],link[1],key=link[2])

'''        
for u,v,key,attr in G2.edges(keys=True,data=True):
    if attr['highway'] in highways_to_keep:
        H.add_edge(u,v,key,attr_dict=attr)
H.graph = G2.graph
'''       
#G2 = nx.Graph(G1)
from_n=np.random.choice(G2.nodes)
to_n=np.random.choice(G2.nodes)                       
route = nx.shortest_path(G2,from_n,to_n,weight='cost')
lr=nx.shortest_path_length(G2, from_n,to_n,weight='cost')
print(lr)
route = nx.shortest_path(G,from_n,to_n,weight='length')
path_edges = list (zip(route,route[1:]))
lunghezza=[]
#route_length_km = sum([G2.edge[u][v][0]['length'] for u, v in zip(route, route[1:])]) / 1000.
for l in path_edges: 
  lunghezza.append(G2[l[0]][l[1]][0]['length'])
print("km:{0:.3f} h:{1:.3f} vm:{2:.0f}".format(sum(lunghezza)/1000, lr/3600, sum(lunghezza)/1000/lr*3600))
route1 = nx.dijkstra_path(G2,from_n,to_n,weight='cost')
lr1=nx.dijkstra_path_length(G2, from_n,to_n,weight='cost')
#route2 = nx.astar_path(G2,from_n,to_n,weight='length')
#lr2=nx.astar_path_length(G2, from_n,to_n,weight='length')
ox.plot_graph_route(G2, route, route_color='green', fig_height=12, fig_width=12)
#ox.plot_route_folium(G2, route, route_color='green')

#print(len(route), type(G2))

#print(G2[265551871])
#print( G2[265551871][32630067])
#print(G2.size(weight='length'), G2.number_of_edges(), G2.number_of_nodes())
      
#print(lr, lr1)


#print(way_dict["residential"][2])

'''
#get way_dictionary with speed osmnx
way_dict={}
for u,v,key,attr in G2.edges(keys=True,data=True):
    if 'maxspeed' in set(attr.keys()) and type(attr.get("highway")) is not list:
        way=attr.get("highway")
        speed=None
        if type(attr.get("maxspeed")) is not list:
           speed=int(attr.get("maxspeed"))
        else:
            speedList = [int(i) for i in attr.get("maxspeed")]
            speed=np.mean(speedList)
        if way in way_dict.keys():
           lista=[]
           lista=way_dict.get(way)
           lista.append(speed)
           way_dict[way]=lista
        else:
            lista=[]
            lista.append(speed)
            way_dict[way]=lista
        #print(attr.get("highway"), attr.get("maxspeed"))
way_dict['other']=[ 20 , 20 , 20 ]
for i in way_dict.keys():
    print(i,': [',int(np.mean(way_dict.get(i))), ',', int(np.max(way_dict.get(i))),',', int(np.min(way_dict.get(i))),']')     
'''    


   
    
print('num_nodi',G2.number_of_nodes())
print('num_archi',G2.number_of_edges())    
#print((attr_edge))
'''
edges = ox.graph_to_gdfs(G2, nodes=False, edges=True)

for i in edges['highway']:
    if i is not list:
        
print(edges['highway'])
'''


'''
highways_to_keep = ['motorway', 'trunk', 'primary']
H = nx.MultiDiGraph()

for u,v,key,attr in G2.edges(keys=True,data=True):
    if attr['highway'] in highways_to_keep:
        H.add_edge(u,v,key,attr_dict=attr)
H.graph = G2.graph

'''

'''
# calculate basic and extended network stats, merge them together, and display
stats = ox.basic_stats(G2)
extended_stats = ox.extended_stats(G2, ecc=True, bc=True, cc=True)
# get a color for each node
def get_color_list(n, color_map='plasma', start=0, end=1):
    return [cm.get_cmap(color_map)(x) for x in np.linspace(start, end, n)]

def get_node_colors_by_stat(G, data, start=0, end=1):
    df = pd.DataFrame(data=pd.Series(data).sort_values(), columns=['value'])
    df['colors'] = get_color_list(len(df), start=start, end=end)
    df = df.reindex(G.nodes())
    return df['colors'].tolist()

nc = get_node_colors_by_stat(G2, data=extended_stats['betweenness_centrality'])
fig, ax = ox.plot_graph(G2, node_color=nc, node_edgecolor='gray', node_size=20, node_zorder=2)

'''