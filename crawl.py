import json
import urllib.request


# settings
key = '5059424d5764617237384455797051'
line_num = 2
date = '20170102'
url = 'http://openapi.seoul.go.kr:8088/%s/json/CardSubwayStatsNew/1/1000/%s' % (key, date)  # get data as much as possible(1000)

# retrieve data
f = urllib.request.urlopen(url)
data = json.loads(f.read().decode('utf-8'))
for item in data['CardSubwayStatsNew']['row']:
    # line_1 only
    if not item['LINE_NUM'] in ['1호선', '경부선', '경인선', '장항선']:
        continue
    print('%s    %i    %i' % (item['SUB_STA_NM'], item['RIDE_PASGR_NUM'], item['ALIGHT_PASGR_NUM']))

print('total count: %i' % data['CardSubwayStatsNew']['list_total_count'])
# print(data)
