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
    visitable_nodes = site_nodes.copy()
    visitable_nodes.append(plant_node)
    all_nodes = visitable_nodes.copy()
    all_nodes.append(depot_node)

    for n in pickup_nodes:
        if n in dropoff_nodes:
            print("error with %s" % n)

    # create enough timeslots at least one plantslot after each site
    i_timeslots = len(all_nodes) * 2
    timeslots = []

    for i in range(i_timeslots):
        timeslots.append(i)

    # create distance dict
    distances = {}
    for n in all_nodes:
        distances[n] = {}

    for i in all_nodes:
        for j in all_nodes:
            distances[i][j] = get_distance(i, j)

    ################################### create model ###################################
    m = LpProblem("Routing", LpMinimize)

    ################################### create Variables ###################################
    x = LpVariable.dicts('edge', (all_nodes, all_nodes, timeslots), cat='Binary')
    y = LpVariable.dicts('load_truck', (timeslots), cat='Binary')
    z = LpVariable.dicts('load_silo', (timeslots), cat='Binary')

    # define constraints

    ################################### basic constraints ###################################

    # a node cannot have an edge with itself
    for i in visitable_nodes:
        m += LpAffineExpression([(x[i][i][t], 1) for t in timeslots]) == 0, 'no_selfvisit_%s' % i

    # flow in and out constraints node
    for j in site_nodes:
        m += LpAffineExpression(
            [(x[i][j][t], 1) for t in timeslots for i in all_nodes if i != j]) == 1, 'flow_in_%s' % j

    for i in site_nodes:
        m += LpAffineExpression(
            [(x[j][i][t], 1) for t in timeslots for j in all_nodes if i != j]) == 1, 'flow_out_%s' % i

    # fat every given time slot max one edge can be used
    for t in timeslots:
        m += LpAffineExpression(
            [(x[i][j][t], 1) for i in all_nodes for j in all_nodes]) <= 1, '1_edge_per_timeslot_%s' % t

    # sites and plant need to be left in subsequent timeslot after entering # not for the last timeslot to avoid key errors, should be handled by depot constraints
    max_time_index = len(timeslots) - 1

    for v in visitable_nodes:
        for t in range(0, max_time_index):
            k = t + 1
            m += LpAffineExpression([(x[i][v][t], 1) for i in all_nodes]) == LpAffineExpression(
                [(x[v][j][k], 1) for j in all_nodes]), 'subsequent_ts_for_{}_at_{}_object: {}'.format(v.node_type, t,
                                                                                                      v.name)

    # depot is the first origin
    m += LpAffineExpression([(x[depot_node][j][0], 1) for j in visitable_nodes]) == 1, 'depot first'

    # flow in and out  constraint for depot
    m += LpAffineExpression(
        [(x[i][depot_node][t], 1) for i in visitable_nodes for t in timeslots]) == 1, 'flow_in_depot'
    m += LpAffineExpression(
        [(x[depot_node][j][t], 1) for j in visitable_nodes for t in timeslots]) == 1, 'flow_out_depot'

    ################################### capacity constraints ###################################

    # silo on truck can only be filled if there's a silo on the truck
    for t in timeslots:
        m += z[t] <= y[t], 'silo_truck_link_t_%s' % t

    # silo on truck needs to be filled when visiting dropoff location
    for a in dropoff_nodes:
        for t in timeslots:
            m += LpAffineExpression([(x[i][a][t], 1) for i in all_nodes]) <= z[t], 'full_silo_enter_drop_{}_{}'.format(
                a.name, t)

    # truck is empty after visiting dropoff location
    for a in dropoff_nodes:
        for t in timeslots:
            m += LpAffineExpression([(x[a][j][t], 1) for j in all_nodes]) <= (
                    1 - y[t]), 'empty_truck_leaving_drop_{}_{}'.format(a.name, t)

    # pickup location can only be visted with an empty truck
    for b in pickup_nodes:
        for t in timeslots:
            m += LpAffineExpression([(x[i][b][t], 1) for i in all_nodes]) <= (
                    1 - y[t]), 'empty_truck_enter_pickup_{}_{}'.format(b.name, t)

    # pickup location can only be left with a full truck
    for b in pickup_nodes:
        for t in timeslots:
            m += LpAffineExpression([(x[b][j][t], 1) for j in all_nodes]) <= y[
                t], 'full_truck_leave_pickup_{}_{}'.format(b.name, t)

    # a pickup location can only be left with a empty silo(but still full truck)
    for b in pickup_nodes:
        for t in timeslots:
            m += LpAffineExpression([(x[b][j][t], 1) for j in all_nodes]) <= (
                    1 - z[t]), 'full_truck_empty_silo_leave_pickup_{}_{}'.format(b.name, t)

    # depot ist left with an empty truck
    m += y[0] == 0, 'inital_empty_truck'

    # the depot can only be entered with an empty truck
    for t in timeslots:
        m += LpAffineExpression([(x[i][depot_node][t], 1) for i in all_nodes]) <= (
                1 - y[t]), 'only_return_empty_t_%s' % t

    ################################### Objective function ###################################
    m += LpAffineExpression([(x[i][j][t], distances[i][j]) for i in all_nodes for j in all_nodes for t in timeslots])

    ################################### Evaluate  results ###################################
    m.solve()
    # print(LpStatus[m.status])

    routing_sequence = []
    edges = 0
    for t in timeslots:
        for i in all_nodes:
            for j in all_nodes:
                if i != j:
                    if x[i][j][t].varValue > 0:
                        # print("from {} to {} at {} - truck: {} - silo: {}".format(i.node_type,j.name,t,y[t].varValue,z[t].varValue))
                        routing_sequence.append(i)
                        edges += 1

    distance = m.objective.value()
    ################################### write back to tour ###################################

    tour.edges = edges
    tour.routing_sequence = routing_sequence
    tour.total_distance = distance
    tour.distance_uptodate = True
