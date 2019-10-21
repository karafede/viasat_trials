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

#G=ox.graph_from_place('Rome, Italy')
#ox.plot_graph(g)
# using NetworkX to calculate the shortest path between two random nodes
#print(G.size)

#route = nx.shortest_path(G, np.random.choice(G.nodes),np.random.choice(G.nodes))
#ox.plot_graph_route(G, route, fig_height=10, fig_width=10)
#G_projected = ox.project_graph(G)
# save street network as GraphML file
#ox.save_graphml(G_projected, filename='network.graphml')
# save street network as ESRI shapefile
#ox.save_graph_shapefile(G_projected, filename='network-shape')
G1 = ox.load_graphml('network.graphml')
G2 = nx.Graph(G1)
from_n=np.random.choice(G2.nodes)
to_n=np.random.choice(G2.nodes)                       
route = nx.shortest_path(G2,from_n,to_n,weight='length')
lr=nx.shortest_path_length(G2, from_n,to_n,weight='length')
route1 = nx.dijkstra_path(G2,from_n,to_n,weight='length')
lr1=nx.dijkstra_path_length(G2, from_n,to_n,weight='length')
#route2 = nx.astar_path(G2,from_n,to_n,weight='length')
#lr2=nx.astar_path_length(G2, from_n,to_n,weight='length')
#ox.plot_graph_route(G2, route, fig_height=10, fig_width=10)
print(len(route))

print(G2.get_edge_data(265551871, 32630067))
#print(G2[265551871])
#print( G2[265551871][32630067])
print(G2.size(weight='length'), G2.number_of_edges(), G2.number_of_nodes())
      
print(lr, lr1)
for edge in G2.edges():     
    d=G2.get_edge_data(edge[0],edge[1])
    if(len(d.keys())>1):
      print(d)

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