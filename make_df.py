from get_data import traffic_by_hour, geopoint, check_location
import csv
import xlrd


def traffic_location(month):
    csv_file = './out/dataframe/traffic_' + month + '.csv'

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        traffic_list, _ = traffic_by_hour(month)
        counter = 0
        counter_total = len(traffic_list)
        for traffic in traffic_list:
            counter += 1
            if counter % 100 == 0:
                print('{}/{} completed'.format(counter, counter_total))

            name = traffic['name']
            line_num = traffic['line_num']
            lat, lng, is_Seoul = check_location(name, line_num)
            if not is_Seoul:
                continue

            ride = sum(traffic['ride'])
            alight = sum(traffic['alight'])
            csvwriter.writerow([name, line_num, lat, lng, ride, alight])
    print('traffic at {} successfully finished'.month)


def price_location(month, housing_type):
    csv_file = './out/dataframe/price_{}_{}.csv'.format(housing_type, month)

    with open(csv_file, 'w', newline='') as cf:
        csvwriter = csv.writer(cf, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        book = xlrd.open_workbook('res/price_{}_{}.xlsx'.format(housing_type, month))
        sh = book.sheet_by_index(0)
        counter_total = 0
        counter_api = 0
        address_dict = {}
        number_rows = sh.nrows
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
        year_bulit = int(row[10].value)
    elif housing_type == 'single_trade':
        address = row[8].value
        area = float(row[4].value)
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


if __name__ == '__main__':
    # traffic_location('201701')
    # price_location('201701', 'apartment_rent')
    # price_location('201701', 'apartment_trade')
    # price_location('201701', 'multi_trade')
    # price_location('201701', 'multi_rent')
    # price_location('201701', 'multi_trade')
    # price_location('201701', 'officetel_rent')
    price_location('201701', 'officetel_trade')
    # price_location('201701', 'single_rent')
    # price_location('201701', 'single_trade')
