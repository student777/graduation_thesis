import json
import strings
import urllib.request


def get_by_date(date='20170102'):
    # settings
    api_key = strings.api_keys['date']
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


def get_by_hour(month):
    # settings
    api_key = strings.api_keys['hour_month']
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayTime/1/1000/%s/' % (api_key, month)  # get data as much as possible(1000)

    # retrieve data
    response = urllib.request.urlopen(url)
    response_dict = json.loads(response.read().decode('utf-8'))

    traffic_list = []

    for item in response_dict['CardSubwayTime']['row']:
        name = item['SUB_STA_NM']
        traffic_ride = [item[key] for key in strings.keys_traffic_ride]
        traffic_alight = [item[key] for key in strings.keys_traffic_alight]
        line_num = item['LINE_NUM']
        traffic = {'name': name, 'ride': traffic_ride, 'alight': traffic_alight, 'line_num': line_num}
        traffic_list.append(traffic)

    count = response_dict['CardSubwayTime']['list_total_count']
    return traffic_list, count
