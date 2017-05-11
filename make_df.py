import manage_db
from get_data import traffic_by_hour, location
import csv
import os
import xlrd


output_dir = './out/'


def traffic_location(month):
    file_name = 'monthly_traffic_' + month + '.csv'
    csv_file = output_dir + file_name

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        traffic_list, _ = traffic_by_hour(month)
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


def price_location(month):
    file_name = 'price_location_' + month + '.csv'
    csv_file = output_dir + file_name

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        book = xlrd.open_workbook('res/price/201701/seoul/아파트(매매).xlsx')
        sh = book.sheet_by_index(0)
        for rx in range(sh.nrows):
            row = sh.row(rx)
            address = row[0].value + ' ' + row[1].value
            lat, lng = location(address)
            area = float(row[5].value)
            price = int(row[8].value.replace(',', ''))
            year_bulit = int(row[10].value)
            csvwriter.writerow([lat, lng, area, year_bulit, price])
    print('successfully finished')


if __name__ == '__main__':
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # traffic_location('201701')
    price_location('201701')
