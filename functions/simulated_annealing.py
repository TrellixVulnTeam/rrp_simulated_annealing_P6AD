from datetime import datetime
import pickle as pickle
import logging
import sys
import pandas as pd
from classes import classes as cl
import numpy as np
from functions import functions as fc
from functions import routing as rt
import copy
import math
import random
import plotly.graph_objects as go

#################################################################################
class Geometric_Schedule:
    def __init__(self,temp_initial: int, q: float, l: int):
     self.temp_initial = temp_initial
     self.q = q
     self.l = l
     self.dict_development = {0: temp_initial}

    def get_temp(self, step: int):
     temp_new = self.temp_initial * self.q ** math.floor(step/self.l)
     self.dict_development[step] = temp_new
     return temp_new

#################################################################################
class NormalizedExponentialAcceptance:
    def __init__(self,distance_inital: float):
        self.distance_inital = distance_inital

    def get_acc(self,temperature: float, distance_delta):
        #negative delta -> better solution -> accept
        if distance_delta < 0:
            return True
        else:
            bol_curr = np.random.uniform() < math.exp(-distance_delta/(self.distance_inital * temperature))
            return bol_curr

class ExponentialAcceptance:
    def __init__(self,distance_inital: float):
        self.distance_inital = distance_inital

    def get_acc(self,temperature: float, distance_delta):
        #negative delta -> better solution -> accept
        if distance_delta < 0:
            return True
        else:
            bol_curr = np.random.uniform() < math.exp(-distance_delta/temperature)
            return bol_curr


#################################################################################
def reassign_job(job_type: str,tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):

    #retrieve distance values from old tours
    old_distance_tour_org = tour_org.distance
    old_distance_tour_new = tour_new.distance
    day_new = tour_new.day

    # move job to new tour
    if job_type == "dropoff":
        tour_org.list_dropoffs.remove(move_job)
        tour_new.list_dropoffs.append(move_job)
    elif job_type == "pickup":
        tour_org.list_pickups.remove(move_job)
        tour_new.list_pickups.append(move_job)
    else: raise ValueError('Job type: {} not recognized.'.format(job_type))

    # adjust values in Tour class
    tour_org.update_totals()
    tour_new.update_totals()
    tour_org.distance_uptodate = False
    tour_new.distance_uptodate = False

    # route new
    rt.routing(tour_org)
    rt.routing(tour_new)

    # adjust values in Job class
    if job_type == "dropoff":
        move_job.dropoff_day = day_new
    elif job_type == "pickup":
        move_job.pickup_day = day_new
    else: raise ValueError('Job type: {} not recognized.'.format(job_type))


    # retrieve distance values from new tours
    new_distance_tour_org = tour_org.distance
    new_distance_tour_new = tour_new.distance
    distance_delta = new_distance_tour_org + new_distance_tour_new \
                     - old_distance_tour_org - old_distance_tour_new

    return distance_delta

#################################################################################
def reassign_job_min(job_type: str, tour_org: cl.Tour, copy_org: cl.Tour, tour_new: cl.Tour, copy_new: cl.Tour, move_job: cl.Job):


    day_new = tour_new.day

    # overwrite values in Tour class
    tour_org = copy.copy(copy_org)
    tour_new = copy_new

    # adjust values in Job class
    if job_type == "dropoff":
        move_job.dropoff_day = day_new
    elif job_type == "pickup":
        move_job.pickup_day = day_new
    else:
        raise ValueError('Job type: {} not recognized.'.format(job_type))

    # retrieve distance values from new tours

    return None
#################################################################################
def reassign_pickup(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return reassign_job('pickup',tour_org,tour_new, move_job)

def reassign_dropoff(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return reassign_job('dropoff',tour_org,tour_new, move_job)

#################################################################################
def evaluate_move(job_type: str,tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #copy tours
    tour_org_copy = tour_org.hardcopy()
    tour_new_copy = tour_new.hardcopy()

    #retrieve distance values from old tours
    old_distance_tour_org = tour_org_copy.distance
    old_distance_tour_new = tour_new_copy.distance
    #day_new = tour_new_copy.day

    # move job to new tour
    if job_type == "dropoff":
        tour_org_copy.list_dropoffs.remove(move_job)
        tour_new_copy.list_dropoffs.append(move_job)
    elif job_type == "pickup":
        tour_org_copy.list_pickups.remove(move_job)
        tour_new_copy.list_pickups.append(move_job)
    else: raise ValueError('Job type: {} not recognized.'.format(job_type))

    # adjust values in Tour class
    tour_org_copy.update_totals()
    tour_new_copy.update_totals()
    tour_org_copy.distance_uptodate = False
    tour_new_copy.distance_uptodate = False

    # route new
    rt.routing(tour_org_copy)
    rt.routing(tour_new_copy)

    # retrieve distance values from new tours
    new_distance_tour_org = tour_org_copy.distance
    new_distance_tour_new = tour_new_copy.distance
    distance_delta = new_distance_tour_org + new_distance_tour_new \
                     - old_distance_tour_org - old_distance_tour_new

    return distance_delta

#################################################################################
def evaluate_pickup(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return evaluate_move('pickup',tour_org,tour_new, move_job)

def evaluate_dropoff(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return evaluate_move('dropoff',tour_org,tour_new, move_job)


#################################################################################

def find_pair_move(depot: str,dict_tours_temp: dict, list_days: list):
    pickup_found = False
    dropoff_found = False
    try_count = 0

    while pickup_found == False or dropoff_found == False:
        # retrieve random days
        day_org = random.choice(list_days)
        day_new_pickup = random.choice(list_days)
        day_new_dropoff = random.choice(list_days)

        # read random tour and move_job into local variables
        tour_org = dict_tours_temp[depot][day_org]

        # find a fitting dropoff job
        if tour_org.dict_worst_edge_pair['pickup']:
            move_job_pickup = tour_org.dict_worst_edge_pair['pickup']
            pickup_found = True
        else:
            continue

        while day_new_pickup < move_job_pickup.end:
            day_new_pickup = random.choice(list_days)
            try_count += 1
            # if not possible break after 1000 tries
            if try_count > 500: break

        # check if there is a dropoff job
        if tour_org.dict_worst_edge_pair['dropoff']:
            move_job_dropoff = tour_org.dict_worst_edge_pair['dropoff']
            dropoff_found = True
        else:
            continue

        while day_new_dropoff > move_job_dropoff.start:
            day_new_dropoff = random.choice(list_days)
            try_count += 1
            # if not possible break after 1000 tries
            if try_count > 500: break

        # retrieve new tours
        pickup_tour_new = dict_tours_temp[depot][day_new_pickup]
        dropoff_tour_new = dict_tours_temp[depot][day_new_dropoff]
        # check if list_plants is filled otherwise repeat
        if not pickup_tour_new.list_plants:
            pickup_found = False
        if not dropoff_tour_new.list_plants:
            dropoff_found = False


    return tour_org, move_job_pickup, move_job_dropoff, pickup_tour_new, dropoff_tour_new