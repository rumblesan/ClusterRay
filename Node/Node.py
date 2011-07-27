#!/usr/bin/env python

from RayManager import RayManager
from NodeComs import NodeComs

class Node():

    def __init__(self):
        self.manager   = JobManager()
        self.job_queue = JobQueue()

    def check_for_jobs(self):
        pass

    def new_job(self):
        pass

    def check_processes(self):
        pass

    def good_job(self):
        pass

    def bad_job(self):
        pass

    def event_loop(self):
        pass


