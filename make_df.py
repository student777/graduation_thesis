from get_data import traffic_by_hour, geopoint
from manage_db import get_location
import csv
import xlrd
import numpy


def traffic_location(month):
    csv_file = './out/dataframe/traffic_{}.csv'.format(month)

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['name', 'line_num', 'lat', 'lng', 'ride', 'alight'])
        traffic_list = traffic_by_hour(month)

        for traffic in traffic_list:
            name = traffic['name']
            line_num = traffic['line_num']
            lat, lng = get_location(name, line_num)
            ride = sum(traffic['ride'])
            alight = sum(traffic['alight'])
            csvwriter.writerow([name, line_num, lat, lng, ride, alight])
    print('traffic at {} successfully finished'.format(month))


def price_location(month, housing_type):
    csv_file = './out/dataframe/price_{}_{}.csv'.format(housing_type, month)

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['lat', 'lng', 'area', 'year_bulit', 'price'])
        book = xlrd.open_workbook('res/price_{}_{}.xlsx'.format(housing_type, month))
        sh = book.sheet_by_index(0)
        counter_total = 0
        counter_api = 0
        address_dict = {}
        number_rows = sh.nrows
        print('{}: Started fetching {} rows'.format(housing_type, number_rows))
        for rx in range(1, number_rows):
            counter_total += 1
            if counter_total % 100 == 0:
                print('{}: {}/{} completed'.format(housing_type, counter_total, number_rows))

            row = sh.row(rx)

            # Handle omitted data
            try:
                address, area, year_bulit, price = get_housing_info(row, housing_type)
            except ValueError as e:
                print(str(e), row)
                continue

            # To prevent address duplicates
            if address in address_dict.keys():
                lat, lng = address_dict[address]
            else:
                point = geopoint(address)
                counter_api += 1
                if point is None:  # HTTP 404 error
                    continue
                lat, lng = point
                address_dict[address] = point

            csvwriter.writerow([lat, lng, area, year_bulit, price])

        print('API used: {} counts'.format(counter_api))
    print('price {} at {} successfully finished'.format(housing_type, month))


def get_housing_info(row, housing_type):
    if housing_type == 'apartment_trade':
        address = row[0].value + ' ' + row[1].value
        area = float(row[5].value)
        price = int(row[8].value.replace(',', ''))
        year_bulit = int(row[10].value)
    elif housing_type == 'multi_trade':
        address = row[0].value + ' ' + row[1].value
        area = float(row[6].value)
        price = int(row[9].value.replace(',', ''))
        year_bulit = int(row[11].value)
    elif housing_type == 'single_trade':
        address = row[8].value
        area = float(row[3].value)
        price = int(row[6].value.replace(',', ''))
        year_bulit = int(row[7].value)
    elif housing_type == 'officetel_trade':
        address = row[0].value + ' ' + row[1].value
        area = float(row[5].value)
        price = int(row[8].value.replace(',', ''))
        year_bulit = int(row[10].value)
    elif housing_type == 'apartment_rent':
        address = row[0].value + ' ' + row[1].value
        area = float(row[6].value)
        price = int(row[9].value.replace(',', '')) + 100 * int(row[10].value.replace(',', ''))
        year_bulit = int(row[12].value)
    elif housing_type == 'single_rent':
        address = row[8].value
        area = float(row[1].value)
        price = int(row[5].value.replace(',', '')) + 100 * int(row[6].value.replace(',', ''))
        year_bulit = 0  # no data
    elif housing_type == 'multi_rent':
        address = row[0].value + ' ' + row[1].value
        area = float(row[6].value)
        price = int(row[9].value.replace(',', '')) + 100 * int(row[10].value.replace(',', ''))
        year_bulit = int(row[12].value)
    elif housing_type == 'officetel_rent':
        address = row[0].value + ' ' + row[1].value
        area = float(row[6].value)
        price = int(row[9].value.replace(',', '')) + 100 * int(row[10].value.replace(',', ''))
        year_bulit = int(row[12].value)
    elif housing_type == 'land_trade':
        # no address info
        pass
    else:
        pass
    return address, area, year_bulit, price


def cluster_station(month):
    traffic_list = traffic_by_hour(month)
    station_work_list = []
    station_home_list = []
    station_others_list = []
    for traffic in traffic_list:
        name = traffic['name']
        line_num = traffic['line_num']
        station = name + ' ' + line_num
        i = numpy.argmax(traffic['ride']) + 4  # Seoul api starts from 4a .m.
        j = numpy.argmax(traffic['alight']) + 4
        if i in [18, 19, 20] and j in [7, 8, 9]:
            station_work_list.append(station)
        elif i in [7, 8, 9] and j in [18, 19, 20]:
            station_home_list.append(station)
        else:
            station_others_list.append(station)

    print(', '.join(station_work_list))
    print(', '.join(station_home_list))
    print(', '.join(station_others_list))
    print('Clustering traffic at {} successfully finished'.format(month))


class Grid():
    rows = 20
    cols = 20
    node_values = numpy.zeros((rows, cols))

    def __init__(self, month):
        file_name = 'out/dataframe/traffic_{}.csv'.format(month)
        with open(file_name, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            next(reader)
            lat_list = []
            lng_list = []
            for row in reader:
                lat_list.append(float(row[2]))
                lng_list.append(float(row[3]))
            top, bottom = max(lat_list), min(lat_list)
            left, right = max(lng_list), min(lng_list)

            self.lat_list = numpy.linspace(bottom, top, self.rows)
            self.lng_list = numpy.linspace(left, right, self.cols)

            # set traffic to node
            csv_file.seek(0)
            next(reader)
            for row in reader:
                lat, lng = float(row[2]), float(row[3])
                traffic = int(row[4]) + int(row[5])
                i, j = self.find_node_index(lat, lng)
                self.set_node_traffic(i, j, traffic)

    def find_node_index(self, lat, lng):
        i = numpy.argsort(numpy.abs(self.lat_list - lat))[0]  # get closest lat index
        j = numpy.argsort(numpy.abs(self.lng_list - lng))[0]
        return i, j

    def set_node_traffic(self, i, j, traffic):
        self.node_values[i][j] += traffic


def traffic_grid(month):
    # get grid from traffic data
    grid = Grid(month)

    # write dataframe
    csv_file = './out/dataframe/traffic_grid_{}.csv'.format(month)
    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['lat', 'lng', 'traffic'])
        for i in range(grid.rows):
            for j in range(grid.cols):
                lat, lng = grid.lat_list[i], grid.lng_list[j]
                traffic = grid.node_values[i][j]
                csvwriter.writerow([lat, lng, traffic])

    print('traffic grid at {} successfully finished'.format(month))


def price_grid(month, housing_type):
    # get grid from traffic data
    grid = Grid(month)

    # read price dataframe
    input_file = 'out/dataframe/price_{}_{}.csv'.format(housing_type, month)
    output_file = 'out/dataframe/price_{}_grid_{}.csv'.format(housing_type, month)
    with open(input_file, newline='') as csv_input:
        reader = csv.reader(csv_input, delimiter=',', quotechar='|')
        next(reader)
        with open(output_file, 'w', newline='') as csv_output:
            csvwriter = csv.writer(csv_output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['traffic', 'area', 'year_built', 'price'])
            for row in reader:
                area, year_bulit, price = float(row[2]), int(row[3]), int(row[4])
                lat, lng = float(row[0]), float(row[1])
                i, j = grid.find_node_index(lat, lng)
                traffic = int(grid.node_values[i][j])
                csvwriter.writerow([traffic, area, year_bulit, price])
    print('Price grid {} at {} successfully finished'.format(housing_type, month))


if __name__ == '__main__':
    # traffic_location('201701')
    # price_location('201701', 'apartment_rent')
    # price_location('201701', 'apartment_trade')
    # price_location('201701', 'multi_trade')
    # price_location('201701', 'multi_rent')
    # price_location('201701', 'multi_trade')
    # price_location('201701', 'officetel_rent')
    # price_location('201701', 'officetel_trade')
    # price_location('201701', 'single_rent')
    # price_location('201701', 'single_trade')
    # cluster_station('201701')
    # traffic_grid('201701')
    # price_grid('201701', 'apartment_rent')
    # price_grid('201701', 'apartment_trade')
    # price_grid('201701', 'multi_trade')
    price_grid('201701', 'multi_rent')
    # price_grid('201701', 'multi_trade')
    # price_grid('201701', 'officetel_rent')
    # price_grid('201701', 'officetel_trade')
    # price_grid('201701', 'single_rent')
    # price_grid('201701', 'single_trade')
