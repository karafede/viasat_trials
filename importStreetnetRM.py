#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 22:53:26 2018

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

#G=ox.graph_from_place('Savona, Italy',network_type='drive')
#ox.plot_graph(G)
# using NetworkX to calculate the shortest path between two random nodes

#route = nx.shortest_path(G, np.random.choice(G.nodes),np.random.choice(G.nodes))
#ox.plot_graph_route(G, route, fig_height=10, fig_width=10)
#G_projected = ox.project_graph(G)
# save street network as GraphML file
#ox.save_graphml(G_projected, filename='networkRM.graphml')
# save street network as ESRI shapefile
#ox.save_graph_shapefile(G_projected, filename='networkLazio-shape')

#street network from bounding box
#G = ox.graph_from_bbox(42.2511, 41.3860, 11.6586, 13.4578, network_type='drive_service')

G=ox.graph_from_address('Rome, Italy',distance=60000,network_type='drive')
#G_projected = ox.project_graph(G)

ox.plot_graph(G)
ox.save_graphml(G, filename='networkRM_Provincia_60km_epgs4326.graphml')
#street network from lat-long point
#This gets the street network within 0.75 km (along the network) of a latitude-longitude point:
#G = ox.graph_from_point((37.79, -122.41), distance=750, network_type='all')
#ox.plot_graph(G)