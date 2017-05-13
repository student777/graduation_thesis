import matplotlib.pyplot as plt
from get_data import traffic_by_hour
import numpy
from gmplot import GoogleMapPlotter
import csv
import os


def hourly_traffic(month):
    plot_len = 3
    plot_size = plot_len * plot_len
    traffic_list, count = traffic_by_hour(month)  # about 500 counts
    fig_num = int(count / plot_size)

    for i in range(0, fig_num):
        i_from = i * plot_size
        i_to = i_from + plot_size
        traffic_list_sliced = traffic_list[i_from:i_to]
        fig, ax = plt.subplots(plot_len, plot_len, figsize=(16, 12), dpi=80)
        j = 0

        for traffic in traffic_list_sliced:
            j = j + 1
            ax = plt.subplot(plot_len, plot_len, j)
            x_axis = numpy.arange(4.5, 28, 1)
            ax.set_title('%s역 %s' % (traffic['name'], traffic['line_num']))
            ax.plot(x_axis, traffic['ride'], 'c', label='ride')
            ax.plot(x_axis, traffic['alight'], 'm', label='alight')
            ax.set_xlabel('hour')
            ax.set_ylabel('passengers')

        plt.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)
        fig.suptitle('지하철 역별 승차/하차 인원수')
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        # make dir
        output_dir = './out/plot/traffic_hourly_{}'.format(month)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        path_to_save = '{}}/{}.png'.format(output_dir, "%.2d" % i)
        fig.savefig(path_to_save)
        print('saved %s' % path_to_save)
        plt.close()

    print('finished successfully')


class myPlotter(GoogleMapPlotter):
    def scatter(self, data, colnum_info, color, **kwargs):
        kwargs["color"] = color
        settings = self._process_kwargs(kwargs)
        with open(data, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            size_list = []
            for row in reader:
                size = float(row[colnum_info['size']])
                size_list.append(size)
            a, b = min(size_list), max(size_list)

            csvfile.seek(0)  # reset the file to the beginning
            for row in reader:
                lat = float(row[colnum_info['lat']])
                lng = float(row[colnum_info['lng']])
                size = float(row[colnum_info['size']])
                size_adjusted = self.cal_size(size, a, b)
                self.circle(lat, lng, size_adjusted, **settings)

    def cal_size(self, size, a, b):
        c, d = 100, 1000
        size_adjusted = (size - a) * (d - c) / (b - a) + c
        return size_adjusted


def price_map(month, housing_type):
    gmap = myPlotter.from_geocode('Seoul')
    data = './out/dataframe/price_{}_{}.csv'.format(housing_type, month)
    colnum_info = {'lat': 1, 'lng': 0, 'size': 4}
    color = '3B0B39'
    gmap.scatter(data, colnum_info, color)
    gmap.draw("out/plot/price_{}_{}.html".format(housing_type, month))


def traffic_map(month):
    data = './out/dataframe/traffic_{}.csv'.format(month)

    # draw ride traffic
    gmap = myPlotter.from_geocode('Seoul')
    colnum_info = {'lat': 2, 'lng': 3, 'size': 4}
    color = '#12a778'
    gmap.scatter(data, colnum_info, color)
    gmap.draw("out/plot/traffic_ride_{}.html".format(month))

    # draw alight traffic
    gmap2 = myPlotter.from_geocode('Seoul')
    color = 'green'
    colnum_info = {'lat': 2, 'lng': 3, 'size': 5}
    gmap2.scatter(data, colnum_info, color)
    gmap2.draw("out/plot/traffic_alight_{}.html".format(month))


if __name__ == '__main__':
    # hourly_traffic('201701')
    price_map('201701', 'apartment_trade')
    # traffic_map('201701')
