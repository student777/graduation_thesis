import os

# make directories
output_dirs = ['./out/plot/price/',
               './out/plot/traffic_hourly/201701/',
               './out/plot/traffic_monthly/',
               './out/dataframe/']
for output_dir in output_dirs:
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
