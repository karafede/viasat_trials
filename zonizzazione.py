
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

#Connect to an existing database
# from ECOTripRM_ga
conn=db_connect.connect_EcoTripRM()
cur = conn.cursor()
gid= []
longitude =[]
latitude =[]
density=[]
p1 =[]
sep=","

for numZone in range(3400, 4001, 200):

    print("zoning: "+str(numZone))
    #Query to create db_residencePY
    cur.execute("DROP TABLE IF EXISTS zones.zone_py_temp CASCADE")
    cur.execute("CREATE  TABLE zones.zone_py_temp "
    "(gid integer  NOT NULL, "
    " zone integer  NOT NULL)");

    cur.execute("""
        SELECT gid, CASE WHEN p1 is null THEN 0 ELSE p1 END, ST_X(ST_Transform(ST_PointOnSurface(geom), 32632)), 
                ST_Y(ST_Transform(ST_PointOnSurface(geom), 32632)), 
                CASE WHEN p1 is null THEN 0 ELSE p1/(ST_Area(ST_Transform(geom, 32632))/1000000) END 
                FROM zones.istat_indicatori_sezcenc_prov_rm_map WHERE ST_IsValid(geom);
                 """)

    # SELECT * from zones.istat_indicatori_sezcenc_prov_rm_map WHERE NOT ST_isvalid(geom)
    records = cur.fetchall()
    i=0
    for row in records:
        gid.append(row[0])
        longitude.append(row[2])
        latitude.append(row[3])
        p1.append(row[1])
        density.append(1+int(row[4]))
        print(i, gid[i], longitude[i], latitude[i], density[i])
        i=i+1

# make array of couples of lon and lat
    X = np.array(list(zip(longitude, latitude)))
    dens=np.array(density)
    model = KMeans(n_clusters=numZone).fit(X, sample_weight=dens)
    #model = KMeans(n_clusters=numZone).fit(X)
    labels = model.labels_
    #print(len(labels))
    for lab in range(len(labels)):
        #print(lab, labels[lab], gid[lab])
        input = "(" + str(gid[lab]) + sep + str(labels[lab])+")";
        #print(input)
        cur.execute("INSERT INTO zones.zone_py_temp (gid, zone)" + " VALUES " + input + "");
    #plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis');
    print("creating "+str(numZone)+" zone table.....")
    cur.execute("DROP TABLE IF EXISTS zones.zone"+str(numZone)+"_py; "
                "CREATE TABLE zones.zone"+str(numZone)+"_py AS ( "
                "SELECT c.zone, sum(c.p1) as p1, sum(c.a2) as a2, sum(c.a6) as a6, sum(c.a7) as a7, sum(c.pf1) as pf1, sum(c.e1) as e1, sum(c.e3) as e3, "
                "(sum(c.p1)/ST_Area(ST_Union(ST_Transform(c.geom, 32632)))*(1000*1000)) ::integer as density, "
                "ST_Area(ST_Union(ST_Transform(c.geom, 32632)))::integer as area_m2, ST_Multi(ST_Union(c.geom)):: Geometry(MULTIPOLYGON, 4326) as geom "
                "FROM ( SELECT a.*, b.zone "
                "FROM zones.istat_indicatori_sezcenc_prov_rm_map a "
                "inner join zones.zone_py_temp b on a.gid=b.gid) c "
                "GROUP BY c.zone "
                "ORDER BY c.zone); "
                "DROP TABLE IF EXISTS zones.zone_py_temp;");
    conn.commit()
# Close communication with the database
cur.close()
conn.close()
