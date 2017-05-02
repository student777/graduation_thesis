import json
import urllib.request


def get_by_date():
    # settings
    key = '5059424d5764617237384455797051'
    date = '20170102'
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayStatsNew/1/1000/%s/' % (key, date)  # get data as much as possible(1000)

    # retrieve data
    f = urllib.request.urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    for item in data['CardSubwayStatsNew']['row']:
        # line_1 only
        if not item['LINE_NUM'] in ['1호선', '경부선', '경인선', '장항선']:
            continue
        print('%s    %i    %i' % (item['SUB_STA_NM'], item['RIDE_PASGR_NUM'], item['ALIGHT_PASGR_NUM']))

    print('total count: %i' % data['CardSubwayStatsNew']['list_total_count'])


def get_by_hour_month():
    # settings
    key = '48734e4c5264617235305a58565144'
    date = '201701'
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayTime/1/5/%s/' % (key, date)

    # retrieve data
    f = urllib.request.urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    print('역명    04승    04하    04승    04하')
    for item in data['CardSubwayTime']['row']:
        print('%s    %i    %i    %i    %i' % (item['SUB_STA_NM'], item['FOUR_RIDE_NUM'], item['FOUR_ALIGHT_NUM'], item['FOUR_RIDE_NUM'], item['FOUR_ALIGHT_NUM']))

    print('total count: %i' % data['CardSubwayTime']['list_total_count'])
