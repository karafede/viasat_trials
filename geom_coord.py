
import os
# check working directory
cwd = os.getcwd()
# change working directoy
os.chdir('C:/python/projects/giraffe/viasat_data')
cwd = os.getcwd()
cwd

import psycopg2
import db_connect


#Connect to an existing database
conn=db_connect.connect_viasat()
cur = conn.cursor()

# erase existing table
cur.execute("DROP TABLE IF EXISTS test_xy CASCADE")

# dateTime timestamp NOT NULL,
cur.execute("""
    CREATE TABLE test_xy(
    id serial,
    name character varying(255),
    x_coord numeric(38,8),
    y_coord numeric(38,8))
    """)

conn.commit()

cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (10, 'hello@dataquest.io', 'Some Name', '123 Fake St.'))

cur.execute("INSERT INTO test_xy(name, x_coord, y_coord) VALUES"
( 'Iowa Heartland Development', 1601700.38827856, 592924.23589906),
( 'Lumbermans Wholesale Company', 2303800.33381338, 501097.06751965),
( 'Plain Talk Publishing', 1610249.93843664, 579937.75662273),
( 'Burlington Northern Sante Fe', 2180668.53184913, 359288.89378747),
( '800 22nd Avenue', 2160559.50579430, 618667.01873098))

conn.commit()