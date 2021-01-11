from datetime import datetime
import pickle as pickle
import logging
import sys
import pandas as pd
from classes import classes as cl
from functions import functions as fc
from functions import routing as rt
import copy
import math
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
def reassign_pickup(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return reassign_job('pickup',tour_org,tour_new, move_job)

def reassign_dropoff(tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #just call right reassign_job function
    return reassign_job('dropoff',tour_org,tour_new, move_job)

#################################################################################
def evaluate_move(job_type: str,tour_org: cl.Tour, tour_new: cl.Tour, move_job: cl.Job):
    #copy tours
    tour_org_copy = copy.copy(tour_org)
    tour_new_copy = copy.copy(tour_new)

    #retrieve distance values from old tours
    old_distance_tour_org = tour_org_copy.distance
    old_distance_tour_new = tour_new_copy.distance
    day_new = tour_new_copy.day

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
    new_distance_tour_org = tour_org.distance
    new_distance_tour_new = tour_new.distance
    distance_delta = new_distance_tour_org + new_distance_tour_new \
                     - old_distance_tour_org - old_distance_tour_new

    return distance_delta