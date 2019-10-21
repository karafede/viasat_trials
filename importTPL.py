#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 19:05:37 2018

@author: gaeval
"""

import geopandas as gpd
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
import peartree as pt

path = '/Users/valenti/py_work/romatpl/rome_static_gtfs.zip'

# Automatically identify the busiest day and
# read that in as a Partidge feed
feed = pt.get_representative_feed(path)

# Set a target time period to
# use to summarize impedance
start = 7*60*60  # 7:00 AM
end = 10*60*60  # 10:00 AM

# Converts feed subset into a directed
# network multigraph
#if there are two bus stops that are close together 
#the connection_threshold is defaulted to 50 meters.
#walk_speed_kmph is default to 4.5 kilometers per hour. 
G = pt.load_feed_as_graph(feed, start, end, connection_threshold=200,walk_speed_kmph=4.0)
#G_projected = ox.project_graph(G)
ox.plot_graph(G)
origin = [41.867876, 12.519082]  
destination = [41.889517, 12.506139]  
point1 = (42.891310, -78.871355)
print(ox.get_nearest_node(G, origin))
#G_projected = ox.project_graph(G)
# save street network as GraphML file
#ox.save_graphml(G_projected, filename='networkRM.graphml')