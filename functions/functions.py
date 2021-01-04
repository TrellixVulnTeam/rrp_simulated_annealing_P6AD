from datetime import datetime


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
    # from https://www.programiz.com/python-programming/datetime/current-time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

