import json
import strings
import urllib.request
from urllib.parse import quote


def traffic_by_date(date):
    # settings
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayStatsNew/1/1000/%s/'
    api_key = '5059424d5764617237384455797051'
    api_endpoint = url % (api_key, date)  # get data as much as possible(1000)

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


def traffic_by_hour(month):
    # settings
    url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayTime/1/1000/%s/'
    api_key = '48734e4c5264617235305a58565144'
    api_endpoint = url % (api_key, month)  # get data as much as possible(1000)

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


def location(address):
    # settings
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s'
    api_endpoint = url % quote(address)

    # retrieve data
    response = urllib.request.urlopen(api_endpoint)
    response_dict = json.loads(response.read().decode('utf-8'))
    location = response_dict['results'][0]['geometry']['location']
    return location['lat'], location['lng']


if __name__ == '__main__':
    # traffic_by_date('20170101')
    traffic_by_hour('201701')
