def get_distance(point1,point2):
    #source : https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
    R = 6373.0 #radius of the earth

    lat1 = math.radians(point1.lat)
    lon1 = math.radians(point1.lon)
    lat2 = math.radians(point2.lat)
    lon2 = math.radians(point2.lon)

    dlon = lon2 - lon1 #calc diff
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2 #haversine formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return(distance)
}