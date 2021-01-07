# creating basic classes for every element used

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
        self.worst_edge_pickup = ''
        self.worst_edge_dropoff = ''
        self.worst_edge_distance = 0
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