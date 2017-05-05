import matplotlib.pyplot as plt
from crawl import get_by_hour_month
from matplotlib.legend_handler import HandlerLine2D
import numpy

traffic_list = get_by_hour_month()

for traffic in traffic_list:
    x_axis = numpy.arange(4.5, 28, 1)
    plt.title(traffic['name'])
    line_ride, = plt.plot(x_axis, traffic['ride'], 'c', label='승차')
    line_alight, = plt.plot(x_axis, traffic['alight'], 'm', label='하차')
    plt.ylabel('passengers')
    plt.legend(handler_map={line_ride: HandlerLine2D(numpoints=4)})
    plt.show()
