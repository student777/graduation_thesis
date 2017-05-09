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

    # update data
    c.execute('update stations set lat=37.282881, lng=127.6263823 where name="여주";')
    c.execute('update stations set lat=37.4764956, lng=127.627492 where name="지평";')
    conn.commit()
    conn.close()


def get_location(name, line_num):
    station = check_station(name, line_num)
    # fetch data
    conn = sqlite3.connect('out/db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT lat, lng FROM stations where name=? and line_num=?', station)
    station_info = c.fetchone()
    conn.close()
    return station_info


def check_station(name, line_num):
    # unsupported line_num
    if line_num in ['E', 'G', 'I', 'I2', 'S', 'U']:
        raise Exception

    '''diffrence between the line name of two APIs'''
    # 1) remove string in brackets
    start = name.find('(')
    end = name.find(')')
    if start != -1 and end != -1:
        name = name[:start]

    # 2) name / line_num difference
    if name == '서울역':
        if line_num == '경의선':
            return '서울(경의중앙선)', 'K'
        else:
            name = '서울'
    elif name in ['서빙고', '한남', '옥수', '응봉']:
        return name, 'K'
    elif name == '양평' and line_num == '중앙선':
        return '양평(경의중앙선)', 'K'
    elif name == '이수' and line_num == '7호선':
        return '총신대입구(이수)', '7'
    elif name == '총신대입구' and line_num == '4호선':
        return '총신대입구(이수)', '4'
    elif name == '신촌' and line_num == '경의선':
        return '신촌(경의중앙선)', 'K'
    elif name in ['이촌', '왕십리'] and line_num == '경원선':
        return name, 'K'
    elif name == '쌍용':
        return '쌍용(나사렛대)', '1'

    # 3) line number difference
    line_num_map = {'1호선': '1', '경부선': '1', '경인선': '1', '장항선': '1', '경원선': '1',
                    '2호선': '2',
                    '3호선': '3', '일산선': '3',
                    '4호선': '4', '과천선': '4', '안산선': '4',
                    '5호선': '5',
                    '6호선': '6',
                    '7호선': '7',
                    '8호선': '8',
                    '9호선': '9', '9호선2단계': '9',
                    '공항철도 1호선': 'A',
                    '분당선': 'B',
                    '경춘선': 'G',
                    '수인선': 'SU',
                    '경의선': 'K', '중앙선': 'K',
                    '경강선': 'KK',
                    }

    if line_num not in line_num_map:
        raise KeyError

    return name, line_num_map[line_num]
