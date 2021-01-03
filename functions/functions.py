import math
from datetime import datetime


def get_distance(point1, point2):
    # source : https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
    R = 6373.0  # radius of the earth

    lat1 = math.radians(point1.lat)
    lon1 = math.radians(point1.lon)
    lat2 = math.radians(point2.lat)
    lon2 = math.radians(point2.lon)

    dlon = lon2 - lon1  # calc diff
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2  # haversine formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


#######################################################################

def get_map(list_depots, list_plants, list_sites):
    import matplotlib.pyplot as plt

    list_depot_lon = []
    list_depot_lat = []

    list_plant_lon = []
    list_plant_lat = []

    list_sites_lon = []
    list_sites_lat = []

    for d in list_depots:
        list_depot_lon.append(d.lon)
        list_depot_lat.append(d.lat)

    for p in list_plants:
        list_plant_lon.append(p.lon)
        list_plant_lat.append(p.lat)

    for s in list_sites:
        list_sites_lon.append(s.lon)
        list_sites_lat.append(s.lat)

    plt.figure(figsize=(12, 8), dpi=100, facecolor='w', edgecolor='k')

    plt.scatter(list_sites_lon, list_sites_lat, marker='.', color='grey')
    plt.scatter(list_depot_lon, list_depot_lat, 100, color='blue')
    plt.scatter(list_plant_lon, list_plant_lat, 100, marker='X', color='green')

    plt.show()


######################################################################

def get_time():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return current_time
