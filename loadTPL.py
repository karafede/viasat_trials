#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 22:03:03 2018

@author: gaeval
"""

#import osmnx as ox
#city = ox.gdf_from_place('Berkeley, California')
#ox.plot_shape(ox.project_gdf(city))

import geopandas as gpd
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
import peartree as pt

#G=ox.graph_from_place('Rome, Italy',network_type='drive')
#ox.plot_graph(G)
# using NetworkX to calculate the shortest path between two random nodes
#print(G.size)

#route = nx.shortest_path(G, np.random.choice(G.nodes),np.random.choice(G.nodes))
#ox.plot_graph_route(G, route, fig_height=10, fig_width=10)
#G_projected = ox.project_graph(G)
# save street network as GraphML file
#ox.save_graphml(G_projected, filename='networkRM.graphml')
# save street network as ESRI shapefile
#ox.save_graph_shapefile(G_projected, filename='networkRM-shape')

#load Graph
G2 = ox.load_graphml('networkRM_TPL.graphml')