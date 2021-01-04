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
        self.total_distance = 0
        self.routing_sequence = []
        self.distance_uptodate = True


###############################################################################
class Worknode:
    def __init__(self,node_type:  str, id:  str,object):
        self.name = node_type + '_' + id
        self.node_type = node_type
        self.lat = object.lat
        self.lon = object.lon