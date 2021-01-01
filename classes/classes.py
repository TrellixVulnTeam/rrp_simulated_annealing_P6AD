"creating basic classes for every element used"

class Depot:
    def __init__(self,name,lon,lat):
        self.name = name
        self.lon = lon
        self.lat = lat


##########################################################################

class Plant:
    def __init__(self,name,lon,lat):
        self.name = name
        self.lon = lon
        self.lat = lat


##########################################################################

class Site: 
    def __init__(self,key,zip,lon,lat)
        self.key = str(zip) + str(lon) + str(lat)
        self.zip = zip
        self.lon = lon
        self.lat = lat

##########################################################################

class Job: 
    def __init__(self,id,key,plant,silo,material,start,duration,site):
        self.id = id
        self.key = key
        self.plant = plant
        self.silo = silo
        self.material = material
        self.start = start
        self.duration = duration
        self.site = site