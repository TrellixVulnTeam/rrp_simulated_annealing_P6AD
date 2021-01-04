import pandas as pd
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

#!pip install pulp
from pulp import *

def routing(tour: cl.Tour):
    #double plants need to be handled
    depot_node = tour.depot
    plant_node = tour.list_plants[0] #only first plant is selected

    dropoff_nodes = tour.list_dropoffs
    pickup_nodes = tour.list_pickups

    #combined lists
    site_nodes = dropoff_nodes + pickup_nodes
    vis_nodes = site_nodes
    vis_nodes.append(plant_node)
    all_nodes = vis_nodes
    all_nodes.append(depot_node)

    #create enough timeslots at least one plantslot after each site
    i_timeslots = len(site_nodes) * 2
    timeslots = []

    for i in range(i_timeslots):
        timeslots.append(i)

    #create model
    m = LpProblem("Routing", LpMinimize)

    # create Variables
    x = LpVariable.dicts('edge', (all_nodes, all_nodes, timeslots), cat='Binary')



    # Objective
    m += LpAffineExpression([(x[i][j][t], 1) for i in all_nodes for j in all_nodes for t in timeslots])



    m.solve()
    print(m.status)



routing(dict_tours['Embsen'][17042])
