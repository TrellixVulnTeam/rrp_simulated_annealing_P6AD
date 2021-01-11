# creating basic classes for every element used
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import copy


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
        self.worst_edge_pair_distance = 0
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
                self.list_plants, self.list_pickups, self.list_dropoffs, self.total_pickups, self.total_dropoffs, self.total_tasks,
                self.distance, self.routing_sequence, self.worst_edge_pickup, self.worst_edge_dropoff ,
                self.worst_edge_pair_distance, self.edges, self.distance_uptodate]

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
                self.worst_edge_pair_distance, self.edges, self.distance_uptodate]

###############################################################################
class Worknode:
    def __init__(self,node_type:  str, id:  str,object):
        self.name = node_type + '_' + id
        self.node_type = node_type
        self.lat = object.lat
        self.lon = object.lon

#################################################################################

class Solution:
    def __init__(self,depot,dict_tours: dict, list_days, dev_curr='', dev_tot_old = ''):
        self.depot = depot
        self.dict_tours = dict_tours
        self.list_days = list_days
        #distance
        self.total_distance = 0
        self.dict_distance_daily = {}
        self.dict_avg_distance_per_task = {}
        #tasks
        self.total_tasks = 0
        self.dict_tasks_daily = {}
        self.dict_dropoffs_daily = {}
        self.dict_pickups_daily = {}
        # worst edges
        self.dict_worst_edge_distance = {}
        self.dict_worst_edge_pickup_distance = {}
        self.dict_worst_edge_dropoff_distance = {}
        #statistics
        self.dict_development_current = dev_curr
        self.dict_development_total = dev_tot_old
        #update
        self.update_values()


    def update_values(self):
        for day in self.list_days:
            #distance
            self.total_distance += self.dict_tours[self.depot.name][day].distance
            self.dict_distance_daily[day] = self.dict_tours[self.depot.name][day].distance
            #tasks
            self.total_tasks += self.dict_tours[self.depot.name][day].total_tasks
            self.dict_tasks_daily[day] = self.dict_tours[self.depot.name][day].total_tasks
            self.dict_dropoffs_daily[day] = self.dict_tours[self.depot.name][day].total_dropoffs
            self.dict_pickups_daily[day] = self.dict_tours[self.depot.name][day].total_pickups
            #avg distance per task
            if self.dict_tasks_daily[day] > 0:
                self.dict_avg_distance_per_task[day] = self.dict_distance_daily[day] /self.dict_tasks_daily[day]
            else:
                self.dict_avg_distance_per_task[day] = 0
                #worst edges
            self.dict_worst_edge_distance[day] = self.dict_tours[self.depot.name][day].worst_edge_pair_distance
            self.dict_worst_edge_pickup_distance[day] = self.dict_tours[self.depot.name][day].worst_edge_pickup_distance
            self.dict_worst_edge_dropoff_distance[day] = self.dict_tours[self.depot.name][day].worst_edge_dropoff_distance

    def plot_tasks(self,y_max: int):
        figure(num=None, figsize=(16, 12), dpi=160, facecolor='w', edgecolor='k')

        days = self.list_days
        dropoffs = [self.dict_dropoffs_daily[day] for day in days]
        pickups = [self.dict_pickups_daily[day] for day in days]

        width = 1  # the width of the bars: can also be len(x) sequence

        p_do = plt.bar(np.arange(len(days)), dropoffs, width)
        p_pi = plt.bar(np.arange(len(days)), pickups, width,
                     bottom=dropoffs)

        plt.ylabel('Tasks')
        plt.xlabel('Days from Day 0')
        plt.title('Tasks per day')
        plt.xticks(np.arange(0, len(days), 100))
        plt.yticks(np.arange(0, y_max, y_max/10))
        plt.legend((p_pi[0], p_do[0]), ('Pickups', 'Dropoffs'))

        plt.show()


    def plot_task_proportion(self):
        figure(num=None, figsize=(16, 12), dpi=160, facecolor='w', edgecolor='k')

        days = self.list_days
        dropoffs = []
        pickups = []

        for day in days:
            dropoff_value = self.dict_dropoffs_daily[day]
            pickup_value = self.dict_pickups_daily[day]
            total_value = dropoff_value + pickup_value

            if total_value > 0:
                dropoffs.append(dropoff_value/total_value)
                pickups.append(pickup_value/total_value)
            else:
                dropoffs.append(0)
                pickups.append(0)


        width = 1  # the width of the bars: can also be len(x) sequence

        p_do = plt.bar(np.arange(len(days)), dropoffs, width)
        p_pi = plt.bar(np.arange(len(days)), pickups, width,
                     bottom=dropoffs)

        plt.ylabel('Proportion of tasks')
        plt.xlabel('Days from Day 0')
        plt.title('Proportion of Tasks per Day')
        plt.yticks(np.arange(0, 1.05, 0.1))
        plt.xticks(np.arange(0, len(days), 100))
        plt.legend((p_pi[0], p_do[0]), ('Pickups', 'Dropoffs'))

        plt.show()



    def plot_distances(self,y_tot_max: int, y_avg_max: int):
        days = self.list_days
        distances = [self.dict_distance_daily[day] for day in days]
        avg_distance_task = [self.dict_avg_distance_per_task[day] for day in days]

        width = 1  # the width of the bars: can also be len(x) sequence

        fig, ax1 = plt.subplots(figsize=(16,12),dpi=160, facecolor='w', edgecolor='k')
        #p1 = plt.bar(np.arange(len(days)), distances, width)

        color = 'tab:blue'
        ax1.set_xlabel('Days from Day 0')
        ax1.set_ylabel('Tour Distance', color=color)
        ax1.bar(np.arange(len(days)), distances, width, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_yticks(np.arange(0, y_tot_max, y_tot_max/10))
        plt.xticks(np.arange(0, len(days), 100))

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:orange'
        ax2.set_ylabel('Avg. Distance per Task', color=color)  # we already handled the x-label with ax1
        ax2.plot(np.arange(len(days)), avg_distance_task, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_yticks(np.arange(0, y_avg_max, y_avg_max/10))

        plt.title('Distances per Day day')
        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        ax2.set_ylim(0, y_avg_max)

        plt.show()


    def plot_worst_edges(self,y_max: int):
        figure(num=None, figsize=(16, 12), dpi=160, facecolor='w', edgecolor='k')

        days = self.list_days
        pickups = [self.dict_worst_edge_pickup_distance[day] for day in days]
        dropoffs = [self.dict_worst_edge_dropoff_distance[day] for day in days]
        combined = [self.dict_worst_edge_dropoff_distance[day] + self.dict_worst_edge_distance[day] for day in days]
        pairs = [self.dict_worst_edge_distance[day] for day in days]

        width = 1  # the width of the bars: can also be len(x) sequence

        p_pa = plt.bar(np.arange(len(days)), pairs, width)
        p_do = plt.bar(np.arange(len(days)), dropoffs, width,
                     bottom=pairs)
        p_pi = plt.bar(np.arange(len(days)), pickups, width,
                     bottom=combined)

        plt.ylabel('Tasks')
        plt.xlabel('Days from Day 0')
        plt.title('Worst Edges per day')
        plt.xticks(np.arange(0, len(days), 100))
        plt.yticks(np.arange(0, y_max, y_max/10))
        plt.legend((p_pi[0], p_do[0], p_pa[0]), ('Worst Pickups', 'Worst Dropoffs','Worst Pairs'))

        plt.show()


