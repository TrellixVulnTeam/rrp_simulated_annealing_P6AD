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
        self.id = id
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


##########################################################################
class Tour:
    def __init__(self,depot,day):
        self.day = day,
        self.depot = depot,
        self.list_nodes = []