from datetime import datetime
import pickle as pickle
import logging


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
#from https://stackoverflow.com/questions/39155206/nameerror-global-name-path-is-not-defined

def save_object(obj, filename) -> object:
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as input:
        loaded_object = pickle.load(input)
    return loaded_object

def quick_save(file_prefix, string_exp_path :str,dict_depots: dict,dict_sites: dict,dict_plants: dict,dict_jobs: dict,dict_tours: dict):
    #specified quicksafe for all dicts
    save_object(dict_depots, string_exp_path + '/quicksave/{}_dict_depots.pkl'.format(file_prefix))
    save_object(dict_sites, string_exp_path + '/quicksave/{}_dict_sites.pkl'.format(file_prefix))
    save_object(dict_plants, string_exp_path + '/quicksave/{}_dict_plants.pkl'.format(file_prefix))
    save_object(dict_jobs, string_exp_path + '/quicksave/{}_dict_jobs.pkl'.format(file_prefix))
    save_object(dict_tours, string_exp_path + '/quicksave/{}_dict_tours.pkl'.format(file_prefix))


########################################################################
def print_log(info :str):
    logging.info(info)
    print(info)

########################################################################
def day_navigation(day: int,index_delta: int, list_days: list):
    #to be able to navigate in the days
    day_index = list_days.index(day)
    new_index = day_index + index_delta

    return(list_days[new_index])

########################################################################


