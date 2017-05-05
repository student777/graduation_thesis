import json
import strings
import urllib.request


def get_by_date():
    # settings
    api_key = strings.api_keys['date']
    date = '20170102'
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayStatsNew/1/1/%s/' % (api_key, date)  # get data as much as possible(1000)

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
    api_key = strings.api_keys['hour']
    date = '201701'
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayTime/1/1/%s/' % (api_key, date)

    # retrieve data
    response = urllib.request.urlopen(url)
    response_dict = json.loads(response.read().decode('utf-8'))

    traffic_list = []

    for item in response_dict['CardSubwayTime']['row']:
        name = item['SUB_STA_NM']
        traffic_ride = [item[key] for key in strings.keys_traffic_ride]
        traffic_alight = [item[key] for key in strings.keys_traffic_alight]
        traffic = {'name': name, 'ride': traffic_ride, 'alight': traffic_alight}
        traffic_list.append(traffic)

    print('total count: %i' % response_dict['CardSubwayTime']['list_total_count'])

    return traffic_list
