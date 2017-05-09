import json
import strings
import urllib.request


url = 'http://openapi.seoul.go.kr:8088/%s/json/%s/1/1000/%s/'


def get_by_date(date):
    # settings
    api_key = '5059424d5764617237384455797051'
    api_name = 'CardSubwayStatsNew'
    api_endpoint = url % (api_key, api_name, date)  # get data as much as possible(1000)

    # retrieve data
    response = urllib.request.urlopen(api_endpoint)
    response_dict = json.loads(response.read().decode('utf-8'))
    station_list = []

    for item in response_dict['CardSubwayStatsNew']['row']:
        name = item['SUB_STA_NM']
        line_num = item['LINE_NUM']
        traffic_ride = int(item['RIDE_PASGR_NUM'])
        traffic_alight = int(item['ALIGHT_PASGR_NUM'])
        station = {'name': name, 'line_num': line_num, 'ride': traffic_ride, 'alight': traffic_alight}
        station_list.append(station)

    count = response_dict['CardSubwayStatsNew']['list_total_count']
    return station_list, count


def get_by_hour(month):
    # settings
    api_key = '48734e4c5264617235305a58565144'
    api_name = 'CardSubwayTime'
    api_endpoint = url % (api_key, api_name, month)  # get data as much as possible(1000)

    # retrieve data
    response = urllib.request.urlopen(api_endpoint)
    response_dict = json.loads(response.read().decode('utf-8'))
    traffic_list = []

    for item in response_dict['CardSubwayTime']['row']:
        name = item['SUB_STA_NM']
        traffic_ride = [int(item[key]) for key in strings.keys_traffic_ride]
        traffic_alight = [int(item[key]) for key in strings.keys_traffic_alight]
        line_num = item['LINE_NUM']
        traffic = {'name': name, 'line_num': line_num, 'ride': traffic_ride, 'alight': traffic_alight}
        traffic_list.append(traffic)

    count = response_dict['CardSubwayTime']['list_total_count']
    return traffic_list, count


if __name__ == '__main__':
    # get_by_date('20170101')
    get_by_hour('201701')
