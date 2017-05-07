import csv
import sqlite3


def setup_db():
    conn = sqlite3.connect('out/db.sqlite3')
    c = conn.cursor()
    c.execute('create table stations( name varchar(30), line_num varchar(10), lat real, long real)')

    with open('data/station_location.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in list(reader)[1:]:
            station_info = row[1], row[2], row[7], row[8]
            c.execute('INSERT INTO stations VALUES (?, ?, ?, ?)', station_info)
            conn.commit()

    conn.close()
