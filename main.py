#!/usr/bin/python3
# ADSB vertical slicer
# LICENSE Apache 2.0
# copyright 2022 by coniferconifer
#
# I'm interested in 3D route of air crafts flying over my head.
# This program generates latitude-altitude sliced scatter plot of air crafts
# of two different time range, i.e. business and travel hours(blue) and midnight (red).
#
# Prepare CSV data as follows
# Install RTL-SDR software on Jetson or Raspberry pi or Windows. (I used Jetson nano)
#
# Install dump1090 from https://github.com/MalcolmRobb/dump1090
# Run dump1090 as a network server.
# $ ./dump1090 --net
# Open another terminal,
# Run for 7200sec to make csv
# $ timeout 7200 nc localhost 30003 > adsb1.csv
# Run once again to get CSV in midnight
# $ timeout 7200 nc localhost 30003 > adsb2.csv
# Edit this code and give these two csv


import pandas as pd
import matplotlib.pyplot as plt

def makeCrossSection(baselon, delta, filename, col):
    dat = pd.read_csv(filename, header=None, index_col=col)
    flight = dat[dat[1] == 3]  # MSG==3 includes latitude,longitude and height in feet
    flight2 = flight[flight[15] < baselon + delta]  # select data from specified longitude
    flight3 = flight2[flight2[15] >= baselon]
    x = flight3[14]  # latitude
    y = flight3[11]  # altitude
    print(flight3)
    print(flight3[[14, 15]])
    return x, y

if __name__ == '__main__':
    baselon = 135.8  # latitude to get vertical slice
    delta = 0.05  # baseline  to baseline + delta will be plotted
    adsb1 = 'adsb202201081729.csv'  # adsb1.csv
    adsb2 = 'adsb202201082242.csv'  # adsb2.csv
    x, y = makeCrossSection(baselon, delta, adsb1, 9)
    plt.scatter(x, y, s=200, c='blue', alpha=0.10)
    x, y = makeCrossSection(baselon, delta, adsb2, 9)
    plt.scatter(x, y, s=200, c="red", alpha=0.10)
    Title = "Flight cross section at Lon=" + str(baselon) + " delta=" + str(delta)
    plt.suptitle(Title)
    plt.title("blue: 2022/1/8 17:29-19:29,red:22:58-24:58")
    plt.xlabel("Latitude")
    plt.ylabel("Flight Altitude")
    plt.grid(True)
    plt.savefig('adsb.jpg')
