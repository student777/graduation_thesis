import json
import strings
import urllib.request
import ssl


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


def geopoint(address):
    # settings
    client_id = "P9BDCV5cHm4ftrb06dsg"
    client_secret = "NmqczBy4aW"
    url = "https://openapi.naver.com/v1/map/geocode?query=" + urllib.parse.quote(address)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    # retrieve data
    try:
        response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    except urllib.error.HTTPError as e:
        print(e)
        return
    rescode = response.getcode()
    if rescode == 200:
        response_dict = json.loads(response.read().decode('utf-8'))
        print(response_dict)
        location = response_dict['result']['items'][0]['point']
    else:
        print("Error Code:" + rescode)
    return location['x'], location['y']


def geopoint_reverse(lat, lng):
    # settings
    client_id = "P9BDCV5cHm4ftrb06dsg"
    client_secret = "NmqczBy4aW"
    url = "https://openapi.naver.com/v1/map/reversegeocode?query={},{}".format(lng, lat)
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    # retrieve data
    try:
        response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    except urllib.error.HTTPError as e:
        print(e)
        return
    rescode = response.getcode()
    if rescode == 200:
        response_dict = json.loads(response.read().decode('utf-8'))
        location = response_dict['result']['items'][0]['addrdetail']['sido']
    else:
        print("Error Code:" + rescode)
    return location


if __name__ == '__main__':
    # traffic_by_date('20170101')
    # traffic_by_hour('201701')
    print(geopoint_reverse(37.540693, 127.070230) == '서울특별시')
