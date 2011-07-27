#!/usr/bin/env python

from RayManager import RayManager
from NodeComs import NodeComs

class Node():

    def __init__(self):
        self.manager   = JobManager()
        self.job_queue = JobQueue()

    def check_for_jobs(self):
        #checks the JobQueue object for new jobs
        pass

    def new_job(self):
        #adds a new job to the JobManager object
        pass

    def get_finished_jobs(self):
        #get finished jobs from JobManager
        pass

    def good_job(self):
        #if those processes finished ok, send back the info
        pass

    def bad_job(self):
        #if those processes didn' finished ok, alert the Master
        pass


