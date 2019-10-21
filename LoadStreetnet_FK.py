#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  23 2019

@author: fkaragul
"""

import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import os

# os.chdir('C:\\giraffe\\viasat_data\\gv_net')
os.chdir('C:\\python\\projects\\giraffe\\viasat_data\\reti_VALENTI\\gv_net')
os.getcwd()

#load Graph
Bracciano = ox.load_graphml('network_Bracciano_6km_epgs4326.graphml')

# way class: mean, max, min  (make a DICTIONARY) these are the "keys"
# these numbers are the speeds on different type of road
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


print(type(way_dict))
# execute some operation to create a "highway" field if this does not exist in the "edge" file
edge_file = Bracciano.edges(keys=True,data=True)
print(type(edge_file))

# "highway" is a key
# "maxspeed" is a key
# "residential" is a key
# "secondary", "50", etc.....are attribute values


# weight/cost assignment
# u and v are the start and ending point of each edge (arc).
for u, v, key, attr in Bracciano.edges(keys=True, data=True):
    # select first way type from list
    if type(attr["highway"]) is list:
        # verify if the attribute field is a list (it might happen)
        attr["highway"] = str(attr["highway"][0])  # first element of the list
        print(attr["highway"], 'uuuuuuuuuuuuu')
    # verify if the attribute exists, the way type in the dictionary
    if attr["highway"] not in way_dict.keys():
        speedlist = way_dict.get("other")
        speed = speedlist[0] * 1000 / 3600
        # create a new attribute in the field "highway"
        attr['cost'] = attr.get("length") / speed
        print(attr.get("highway"), speedlist[0], attr.get("cost"), '^^^^^^^^^^^')
    # add the "attr_dict" to the edge file
    Bracciano.add_edge(u, v, key, attr_dict=attr)
    continue

if 'maxspeed' in set(attr.keys()) and len(attr.get("maxspeed")) < 4:
    if type(attr.get("maxspeed")) is list:
        speedList = [int(i) for i in attr.get("maxspeed")]
        speed = np.mean(speedList) * 1000 / 3600
        attr['cost'] = attr.get("length") / speed
        # print(attr.get("highway"), attr.get("maxspeed"), attr.get("cost"),'========')
    else:
        speed = float(attr.get("maxspeed")) * 1000 / 3600
        attr['cost'] = attr.get("length") / speed
        # print(attr.get("highway"), attr.get("maxspeed"), attr.get("cost"),'°°°°°°°°°')
    Bracciano.add_edge(u, v, key, attr_dict=attr)
else:  # read speed from way class dictionary
    speedlist = way_dict.get(attr["highway"])
    speed = speedlist[0] * 1000 / 3600
    attr['cost'] = attr.get("length") / speed
    # print(attr.get("highway"), speedlist[0], attr.get("cost"),'-----------')
    Bracciano.add_edge(u, v, key, attr_dict=attr)

# highways_to_keep = ['motorway', 'trunk', 'primary']
# H = nx.MultiDiGraph()
#
# for u,v,key,attr in Bracciano.edges(keys=True,data=True):
#     if attr['highway'] in highways_to_keep:
#         H.add_edge(u,v,key,attr_dict=attr)
# H.graph = Bracciano.graph


# the function nx.Graph() does not include attributes
# Bracciano = nx.Graph(Bracciano)


### difference between MultiDiGraph and Graph
# G = nx.MultiDiGraph()
# G.add_node(1)
# G.nodes
# G.add_nodes_from([2,3])
# G.add_nodes_from(range(100,110))
# G.nodes
# H=nx.Graph()
# H.add_path([0,1,2,3,4,5,6,7,8,9])
# G.add_nodes_from(H)
# G = nx.Graph(G)


from_n=np.random.choice(Bracciano.nodes)
to_n=np.random.choice(Bracciano.nodes)
# calculate the shortest path between two points...meters )this is a list of nodes based on the shortest time
route = nx.shortest_path(Bracciano,from_n,to_n, weight='cost')
# calculate the length of the route
lr = nx.shortest_path_length(Bracciano, from_n,to_n, weight='cost')
print(lr)
# route = nx.shortest_path(Bracciano,from_n,to_n,weight='length')
# create pairs of edge for the shortest route
path_edges = list(zip(route,route[1:]))

lunghezza=[]
# route_length_km = sum([Bracciano.edges[u][v][0]['length'] for u, v in zip(route, route[1:])]) / 1000.

for l in path_edges:
  lunghezza.append(Bracciano [l[0]] [l[1]] [0]['length'])  # get only the length for each arch between 2 path edges, [0] it the key = 0
print("km:{0:.3f} h:{1:.3f} vm:{2:.0f}".format(sum(lunghezza)/1000, lr/3600, sum(lunghezza)/1000/lr*3600))  # units == km

route1 = nx.dijkstra_path(Bracciano,from_n,to_n,weight='cost')
lr1 = nx.dijkstra_path_length(Bracciano, from_n,to_n,weight='cost')

#route2 = nx.astar_path(Bracciano,from_n,to_n,weight='length')
#lr2=nx.astar_path_length(Bracciano, from_n,to_n,weight='length')

ox.plot_graph_route(Bracciano, route, route_color='green', fig_height=12, fig_width=12)

# make an interactive map
path = ox.plot.plot_route_folium(Bracciano, route, route_color='green')
path.save('Bracciano_min_path.html')
# print(len(route), type(Bracciano))

#print(G2[265551871])
#print( G2[265551871][32630067])
#print(G2.size(weight='length'), G2.number_of_edges(), G2.number_of_nodes())
      
#print(lr, lr1)


# save shp file AGAIN street network as ESRI shapefile (includes NODES and EDGES and new attributes)
ox.save_graph_shapefile(Bracciano, filename='networkBracciano-shape')

#print(way_dict["residential"][2])

# get way_dictionary with speed osmnx
way_dict={}
for u,v,key,attr in Bracciano.edges(keys=True,data=True):
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

print('num_nodi',Bracciano.number_of_nodes())
print('num_archi',Bracciano.number_of_edges())


#print((attr_edge))

# print edges (only highway attribute)
edges = ox.graph_to_gdfs(Bracciano, nodes=False, edges=True)

for i in edges['highway']:
    if i is not list:
        print(edges['highway'])


# calculate basic and extended network stats, merge them together, and display
stats = ox.basic_stats(Bracciano)
extended_stats = ox.extended_stats(Bracciano, ecc=True, bc=True, cc=True)
# get a color for each node
def get_color_list(n, color_map='plasma', start=0, end=1):
    return [cm.get_cmap(color_map)(x) for x in np.linspace(start, end, n)]

def get_node_colors_by_stat(Bracciano, data, start=0, end=1):
    df = pd.DataFrame(data=pd.Series(data).sort_values(), columns=['value'])
    df['colors'] = get_color_list(len(df), start=start, end=end)
    df = df.reindex(Bracciano.nodes())
    return df['colors'].tolist()

nc = get_node_colors_by_stat(Bracciano, data=extended_stats['betweenness_centrality'])
fig, ax = ox.plot_graph(Bracciano, node_color=nc, node_edgecolor='gray', node_size=20, node_zorder=2)

# make an interactive map
# path = ox.plot_route_folium(Bracciano, route, route_color='green')
# path.save('Bracciano_min_path.html')
