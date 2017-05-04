import matplotlib.pyplot as plt
from crawl import get_by_hour_month


x_axis = [4.5, 5.5, 6.5, 7.5, 8.5]
result_set = get_by_hour_month()

for result in result_set:
    plt.plot(x_axis, result)

plt.ylabel('승차/하차 인원')
plt.show()
