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
    # double plants need to be handled

    # create working nodes to level different object types
    depot_node = cl.Worknode('depot', tour.depot.name, tour.depot)
    plant_node = cl.Worknode('plant', tour.list_plants[0].name, tour.list_plants[0])  # only first plant is selected

    # format jobs to sites
    dropoff_nodes = []
    pickup_nodes = []

    for j in tour.list_dropoffs:
        wn_j = cl.Worknode('dropoff_job', j.name, j.site)
        dropoff_nodes.append(wn_j)
    for j in tour.list_pickups:
        wn_j = cl.Worknode('pickup_job', j.name, j.site)
        pickup_nodes.append(wn_j)

    # combined lists
    site_nodes = dropoff_nodes + pickup_nodes
    visitable_nodes = site_nodes
    visitable_nodes.append(plant_node)
    all_nodes = visitable_nodes
    all_nodes.append(depot_node)

    for n in pickup_nodes:
        if n in dropoff_nodes:
            print("error with %s" % n)

    # create enough timeslots at least one plantslot after each site
    i_timeslots = len(site_nodes) * 2
    timeslots = []

    for i in range(i_timeslots):
        timeslots.append(i)

    # create distance dict
    distances = {}
    for n in all_nodes:
        distances[n] = {}

    for i in all_nodes:
        for j in all_nodes:
            distances[i][j] = rt.get_distance(i, j)

    # create model
    m = LpProblem("Routing", LpMinimize)

    # create Variables
    x = LpVariable.dicts('edge', (all_nodes, all_nodes, timeslots), cat='Binary')
    y = LpVariable.dicts('load_truck', (timeslots), cat='Binary')
    z = LpVariable.dicts('load_silo', (timeslots), cat='Binary')

    # define constraints

    # a node cannot have an edge with itself
    for i in visitable_nodes:
        m += LpAffineExpression([(x[i][i][t], 1) for t in timeslots]) == 0, 'no_selfvisit_%s' % i

    # flow in and out constraints node
    for j in site_nodes:
        m += LpAffineExpression(
            [(x[i][j][t], 1) for t in timeslots for i in site_nodes if i != j]) == 1, 'flow_in_%s' % j
        m += LpAffineExpression(
            [(x[j][i][t], 1) for t in timeslots for i in site_nodes if i != j]) == 1, 'flow_out_%s' % j

    # sites and plant need to be left in subsequent timeslot after entering # not for the last timeslot to avoid key errors, should be handled by depot constraints
    for v in visitable_nodes:
        for t in range(len(timeslots) - 1):
            m += LpAffineExpression([(x[i][v][t], 1) for i in all_nodes if i != v]) == LpAffineExpression(
                [(x[v][j][t + 1], 1) for j in all_nodes if j != v]), 'subsequent_ts_in_out_v{}_t{}'.format(v.name, t)

    # Objective
    m += LpAffineExpression([(x[i][j][t], distances[i][j]) for i in all_nodes for j in all_nodes for t in timeslots])

    m.solve()
    print(m.status)


