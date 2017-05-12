import matplotlib.pyplot as plt
from get_data import traffic_by_hour
import numpy
import os
from gmplot import GoogleMapPlotter
import csv

def hourly_traffic(month):
    plot_len = 3
    plot_size = plot_len * plot_len
    traffic_list, count = traffic_by_hour(month)  # about 500 counts
    fig_num = int(count / plot_size)

    output_dir = './out/img'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

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
        path_to_save = '%s/hourly_traffic_%s.png' % (output_dir, "%.2d" % i)
        fig.savefig(path_to_save)
        print('saved %s' % path_to_save)
        plt.close()

    print('finished successfully')


class myPlotter(GoogleMapPlotter):
    def scatter(self, lats, lngs, color=None, size=None, marker=True, c=None, s=None, **kwargs):
        color = color or c
        kwargs["color"] = color
        settings = self._process_kwargs(kwargs)
        for lat, lng, s in zip(lats, lngs, size):
            if marker:
                self.marker(lat, lng, settings['color'])
            else:
                self.circle(lat, lng, s, **settings)


def price_map():
    gmap = myPlotter.from_geocode('Seoul')
    lat_list = []
    lng_list = []
    size_list = []
    with open('out/price/price_location_201701.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            lat_list.append(float(row[0]))
            lng_list.append(float(row[1]))
            size_list.append(float(row[4]) / 1000)
    gmap.scatter(lng_list, lat_list, '#3B0B39', size=size_list, marker=False)
    gmap.draw("out/test.html")


if __name__ == '__main__':
    # hourly_traffic('201701')
    price_map()
