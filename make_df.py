import manage_db
from get_data import get_by_hour
import csv
import os


def set_data(month):
    traffic_list, _ = get_by_hour(month)

    output_dir = './out/'
    file_name = 'monthly_traffic_' + month + '.csv'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    csv_file = output_dir + file_name

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for traffic in traffic_list:
            name = traffic['name']
            line_num = traffic['line_num']
            try:
                lat, lng = manage_db.get_location(name, line_num)
            except Exception as e:
                print(e, traffic['name'], traffic['line_num'])
                continue
            ride = sum(traffic['ride'])
            alight = sum(traffic['alight'])
            csvwriter.writerow([name, line_num, lat, lng, ride, alight])
    print('successfully finished')


if __name__ == '__main__':
    set_data('201701')
