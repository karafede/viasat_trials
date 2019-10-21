#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 2019

@author: fkaragul
"""

#import osmnx as ox
#city = ox.gdf_from_place('Berkeley, California')
#ox.plot_shape(ox.project_gdf(city))

import os
# os.chdir('C:\\giraffe\\viasat_data\\gv_net')
os.chdir('C:\\python\\projects\\giraffe\\viasat_data\\reti_VALENTI\\gv_net')

import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.cm as cm

B = ox.graph_from_place('Bracciano, Italy',network_type='walk')
# ox.plot_graph(B)

B = ox.graph_from_place('Bracciano, Italy',network_type='bike')
# ox.plot_graph(B)

B = ox.graph_from_place('Bracciano, Italy',network_type='all_private')
# ox.plot_graph(B)

B = ox.graph_from_place('Bracciano, Italy',network_type='drive')
# ox.plot_graph(B)

# You can also specify several different network types:
# drive - get drivable public streets (but not service roads)
# drive_service - get drivable streets, including service roads
# walk - get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
# bike - get all streets and paths that cyclists can use
# all - download all non-private OSM streets and paths
# all_private - download all OSM streets and paths, including private-access ones

basic_stats = ox.basic_stats(B)
print(basic_stats['circuity_avg'])
# ans: [1.1167206203103612]
# In this street network, the streets are 12% more circuitous than the straight-lines paths would be.

extended_stats = ox.extended_stats(B)
print(extended_stats['pagerank_max_node'])

# Create place boundary shapefiles from OpenStreetMap
Bracciano_shp = ox.gdf_from_place('Bracciano, Italy')
ox.save_gdf_shapefile(Bracciano_shp)

# using NetworkX to calculate the shortest path between two random nodes
route = nx.shortest_path(B, np.random.choice(B.nodes),np.random.choice(B.nodes))
ox.plot_graph_route(B, route, fig_height=10, fig_width=10)

# save street network as GraphML file
B_projected = ox.project_graph(B)
ox.save_graphml(B_projected, filename='network_Bracciano_6km_epgs4326.graphml')

# save street network as ESRI shapefile (includes NODES and EDGES)
ox.save_graph_shapefile(B_projected, filename='networkBracciano-shape')

#street network from bounding box
#G = ox.graph_from_bbox(42.2511, 41.3860, 11.6586, 13.4578, network_type='drive_service')

# G=ox.graph_from_address('Rome, Italy',distance=60000,network_type='drive')
G=ox.graph_from_address('Rome, Italy',distance=6000,network_type='drive')
Bracciano = ox.graph_from_address('Bracciano, Italy',distance=6000,network_type='drive')
# Bracciano = ox.graph_from_address('Bracciano, Italy',distance=6000)

#G_projected = ox.project_graph(G)
ox.plot_graph(Bracciano)

# ox.save_graphml(G, filename='networkRM_Provincia_60km_epgs4326.graphml')
ox.save_graphml(Bracciano, filename='network_Bracciano_6km_epgs4326.graphml')

#street network from lat-long point
# This gets the street network within 0.75 km (along the network) of a latitude-longitude point:
# G = ox.graph_from_point((37.79, -122.41), distance=750, network_type='all')
# ox.plot_graph(G)
