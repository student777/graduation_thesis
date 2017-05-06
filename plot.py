import matplotlib.pyplot as plt
from crawl import get_by_hour
import numpy
import os

month = '201701'
output_path = './out'
plot_len = 3
plot_size = plot_len * plot_len
traffic_list, count = get_by_hour(month)  # about 500 counts
fig_num = int(count / plot_size)

if not os.path.isdir(output_path):
    os.makedirs(output_path)


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
    path_to_save = '%s/traffic_month_%s.png' % (output_path, i)
    fig.savefig(path_to_save)
    print('saved %s' % path_to_save)
    plt.close()

print('finished successfully')
