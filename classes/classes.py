# creating basic classes for every element used
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class Depot:
    def __init__(self, name, lon, lat):
        self.name = name
        self.lon = lon
        self.lat = lat


##########################################################################

class Plant:
    def __init__(self, name, lon, lat):
        self.name = name
        self.lon = lon
        self.lat = lat


##########################################################################

class Site:
    def __init__(self, zipcode, lon, lat):
        self.name = str(round(zipcode)) + '/' + str(lon) + '/' + str(lat)  # concat key
        self.zip = zipcode
        self.lon = lon
        self.lat = lat


##########################################################################

class Job:
    def __init__(self, id, key, plant, silo, material, start, end, duration, site, prox_depot):
        self.name = id
        self.key = key
        self.plant = plant
        self.silo = silo
        self.material = material
        self.start = start
        self.end = end
        self.duration = duration
        self.site = site
        self.dropoff_day = 0
        self.dropoff_tour = ''
        self.dropoff_depot = ''
        self.pickup_day = 0
        self.pickup_tour = ''
        self.pickup_depot = ''
        self.prox_depot = prox_depot
        self.assigned = False


##########################################################################
class Tour:
    def __init__(self,depot,day):
        self.day = day
        self.depot = depot
        self.list_plants = []
        self.list_pickups = []
        self.list_dropoffs = []
        self.total_pickups = 0
        self.total_dropoffs = 0
        self.total_tasks = 0
        self.distance = 0
        self.routing_sequence = []
        self.dict_worst_edge_pair = {}
        self.worst_edge_pickup = ''
        self.worst_edge_dropoff = ''
        self.worst_edge_distance = 0
        self.worst_edge_pickup_distance = 0
        self.worst_edge_dropoff_distance = 0
        self.edges = 0
        self.distance_uptodate = True


    def update_totals(self):
        self.total_pickups = len(self.list_pickups)
        self.total_dropoffs = len(self.list_dropoffs)
        self.total_tasks = self.total_pickups + self.total_dropoffs


    def get_colums(self):
        return['day', 'depot', 'list_plants',  'list_pickups',
                'list_dropoffs', 'total_pickups', 'total_dropoffs','total_tasks',
               'distance', 'routing_sequence' ,'worst_edge_pickup',
               'worst_edge_distance', 'worst_edge_dropoff', 'edges','distance_uptodate']

    def get_all_values(self):
        return [self.day, self.depot,
               self.list_plants, self.list_pickups,  self.list_dropoffs, self.total_pickups, self.total_dropoffs, self.total_tasks,
               self.distance, self.routing_sequence, self.worst_edge_pickup, self.worst_edge_dropoff ,
                self.worst_edge_distance, self.edges,self.distance_uptodate]

    def get_all_value_readable(self):

        #read element names from object list
        read_plants = []
        for p in self.list_plants:
            read_plants.append(p.name)

        read_pickups = []
        for j in self.list_pickups:
            read_pickups.append(j.name)

        read_dropoffs = []
        for j in self.list_dropoffs:
            read_dropoffs.append(j.name)

        read_routing = []
        for wn in self.routing_sequence:
            read_routing.append(wn.name)

        #read nodenames if nodes are filled
        if self.worst_edge_pickup != '':
            read_worst_edge_pickup = self.worst_edge_pickup.name
        else:
            read_worst_edge_pickup = ''

        if self.worst_edge_dropoff != '':
            read_worst_edge_dropoff = self.worst_edge_dropoff.name
        else :
            read_worst_edge_dropoff = ''

        return [self.day, self.depot.name,
                read_plants, read_pickups, read_dropoffs, self.total_pickups, self.total_dropoffs, self.total_tasks,
                self.distance, read_routing, read_worst_edge_pickup, read_worst_edge_dropoff,
                self.worst_edge_distance, self.edges, self.distance_uptodate]

###############################################################################
class Worknode:
    def __init__(self,node_type:  str, id:  str,object):
        self.name = node_type + '_' + id
        self.node_type = node_type
        self.lat = object.lat
        self.lon = object.lon

#################################################################################
class Solution:
    def __init__(self,depot,dict_tours: dict, list_days):
        self.depot = depot
        self.dict_tours = dict_tours
        self.list_days = list_days

        self.total_distance = 0
        self.dict_distance_daily = {}
        self.total_tasks = 0
        self.dict_tasks_daily = {}
        self.dict_dropoffs_daily = {}
        self.dict_pickups_daily = {}

        self.update_values()


    def update_values(self):
        for day in self.list_days:
            self.total_distance += self.dict_tours[self.depot.name][day].distance
            self.dict_distance_daily[day] = self.dict_tours[self.depot.name][day].distance
            self.total_tasks += self.dict_tours[self.depot.name][day].total_tasks
            self.dict_tasks_daily[day] = self.dict_tours[self.depot.name][day].total_tasks
            self.dict_dropoffs_daily[day] = self.dict_tours[self.depot.name][day].total_dropoffs
            self.dict_pickups_daily[day] = self.dict_tours[self.depot.name][day].total_pickups

    def plot_tasks(self):

        days = self.list_days
        dropoffs = [self.dict_dropoffs_daily[day] for day in days]
        pickups = [self.dict_pickups_daily[day] for day in days]

        width = 1  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(np.arange(len(days)), dropoffs, width)
        p2 = plt.bar(np.arange(len(days)), pickups, width,
                     bottom=dropoffs)

        plt.ylabel('Tasks')
        plt.title('Tasks per day')
        plt.xticks(np.arange(0, len(days), 100))
        plt.yticks(np.arange(0, 100, 10))
        plt.legend((p1[0], p2[0]), ('Pickups', 'Dropoffs'))

        figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.show()