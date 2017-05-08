import csv
import sqlite3


def setup_db():
    conn = sqlite3.connect('out/db.sqlite3')
    c = conn.cursor()

    # create table
    c.execute('create table stations( name varchar(30), line_num varchar(10), lat real, lng real)')

    # insert data
    with open('res/station_location.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in list(reader)[1:]:
            station_info = row[1], row[2], row[7], row[8]
            c.execute('INSERT INTO stations VALUES (?, ?, ?, ?)', station_info)
            conn.commit()

    conn.close()


def get_location(name, line_num):
    # check line_num
    allowed_line_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'E', 'G', 'I', 'I2', 'K', 'KK', 'S', 'SU', 'U']
    if line_num not in allowed_line_num:
        print('wrong line_num')
        return

    # fetch data
    conn = sqlite3.connect('out/db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT lat, lng FROM stations where name=? and line_num=?', (name, line_num))
    row = c.fetchone()
    conn.close()
    return row
