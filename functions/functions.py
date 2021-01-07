from datetime import datetime
import pickle as pickle
import logging
import sys
import pandas as pd


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


########################################################################
# from https://stackoverflow.com/questions/39155206/nameerror-global-name-path-is-not-defined

def save_object(obj, filename) -> object:
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as input:
        loaded_object = pickle.load(input)
    return loaded_object


def quick_save(dict_objects: dict, path: str, prefix):
    print_log("Starting quicksave at {}".format(get_time()))
    sys.setrecursionlimit(100000)

    for object in dict_objects:
        # export all data objects

        save_object(object, path + '/quicksave/' + prefix + '{}.pkl'.format(object))

    print_log("Done with persitation at {}".format(get_time()))

def persistate(dict_objects: dict, path: str, prefix):
    print_log("Starting persitation at {}".format(get_time()))
    sys.setrecursionlimit(100000)

    # if everything is handed over, create tour_df
    if 'dict_depot' in dict_objects:
        if 'list_days' in dict_objects:
            if 'dict_tours' in dict_objects:

                tour_cols = dict_objects['dict_depots']['Embsen'][17042].get_colums()

                # create df with objects and readable df for solution
                i = 0
                tour_df = pd.DataFrame([tour_cols])
                tour_df.columns = tour_cols
                tour_df_readable = pd.DataFrame([tour_cols])
                tour_df_readable.columns = tour_cols

                for depot in dict_objects['dict_depots']:
                    for day in dict_objects['list_days']:
                        t = dict_objects['dict_depots'][depot][day]
                        tour_df.loc[i] = t.get_all_values()
                        tour_df_readable.loc[i] = t.get_all_value_readable()
                        i += 1

                # export tabular tour data
                tour_df.to_csv(path + '/tour_df.csv')
                tour_df_readable.to_csv(path + '/tour_df_readable.csv')

    for object in dict_objects:
        # export all data objects
        save_object(object, path + '/' + prefix + '{}.pkl'.format(object))

    print_log("Done with persitation at {}".format(get_time()))


########################################################################
def print_log(info: str):
    logging.info(info)
    print(info)


########################################################################
def day_navigation(day: int, index_delta: int, list_days: list):
    # to be able to navigate in the days
    day_index = list_days.index(day)
    new_index = day_index + index_delta

    return (list_days[new_index])

########################################################################
