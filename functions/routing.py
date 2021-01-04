import pandas as pd
!pip install pulp
from pulp import *
import math
from classes import classes as cl

#######################################################################

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

def routing(tour: cl.Tour):
    #double plants need to be handled

    depot_node = tour.depot
    plant_node = tour.list_plants[0] #only first plant is selected

    list_dropoff_nodes = tour.list_dropoffs
    list_pickup_nodes = tour.list_pickups

    #combined lists
    list_site_nodes = list_dropoff_nodes + list_pickup_nodes
    list_visitable_nodes = list_site_nodes
    list_visitable_nodes.append(plant_node)
    list_all_nodes = list_visitable_nodes
    list_all_nodes.append(depot_node)

    #create enough timeslots at least one plantslot after each site
    i_timeslots = len(list_site_nodes) * 2
    list_timeslots = []

    for i in range(i_timeslots):
        list_timeslots.append(i)

    # create Variables
    x = LpVariable.dicts('edge',)