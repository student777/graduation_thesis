import matplotlib.pyplot as plt
import matplotlib.cm
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from get_data import traffic_by_hour
import numpy
import os


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


def price_map():
    m = Basemap(resolution='f', projection='merc', llcrnrlon=121.763985, llcrnrlat=32.428539, urcrnrlon=131.185036, urcrnrlat=42.701393)
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#dfdfdf', lake_color='#46bcec')
    m.drawcoastlines()
    lons = [-4,-2,-1,1]
    lats = [49.6,50,51,54]
    x, y = m(lons, lats)
    m.scatter(x, y, marker='o', color='m', s=[10,20,30,40])
    plt.show()



if __name__ == '__main__':
    # hourly_traffic('201701')
    price_map()
