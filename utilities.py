from math import pi, cos
import operator


def new_lat_long(latitude, longitude, dy, dx, f):
    earth = 6378.137
    new_lat = f(latitude, (dy / earth) * (180 / pi))
    new_long = f(longitude, (dx / earth) * (180 / pi) / cos(latitude * pi / 180))
    return round(new_lat, 6), round(new_long, 6)


if __name__ == '__main__':
    # Lat
    # 51.549369
    # 51.454752
    # Long
    # -0.002275
    # -0.236769

    print(new_lat_long(51.549369, -0.002275, 0.1, 0.1, operator.add))
    print(new_lat_long(51.454752, -0.236769, 0.1, 0.1, operator.sub))
