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
        self.total_jobs = 0
        self.total_distance = 0
        self.routing_sequence = []
        self.edges = 0
        self.distance_uptodate = True

    def get_colums(self):
        return(['day', 'depot', 'list_plants',  'list_pickups',
                'list_dropoffs', 'total_jobs', 'total_distance', 'routing_sequence' ,'edges','distance_uptodate'])

    def get_all_values(self):
        return([self.day, self.depot,
               self.list_plants, self.list_pickups,  self.list_dropoffs,
               self.total_distance, self.routing_sequence, self.edges,self.distance_uptodate])

    def get_all_value_readable(self):
        read_depot = self.depot.name

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
            read_routing.apped(wn.name)

        return ([self.day, self.depot.name,
                read_plants, read_pickups, read_dropoffs,
                self.total_distance, read_routing, self.edges, self.distance_uptodate])

###############################################################################
class Worknode:
    def __init__(self,node_type:  str, id:  str,object):
        self.name = node_type + '_' + id
        self.node_type = node_type
        self.lat = object.lat
        self.lon = object.lon