import database
from crawl import get_by_hour
import csv


def set_data(month='201701'):
    traffic_list, _ = get_by_hour(month)
    with open('out/test.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for traffic in traffic_list:
            name = traffic['name']
            line_num = traffic['line_num']
            try:
                lat, lng = database.get_location(name, line_num)
            except Exception as e:
                print(e, traffic['name'], traffic['line_num'])
                continue
            ride = sum(traffic['ride'])
            alight = sum(traffic['alight'])
            csvwriter.writerow([name, line_num, lat, lng, ride, alight])
    print('successfully finished')


if __name__ == '__main__':
    set_data()
