#!/usr/bin/env python

from RayManager import RayManager
from JobQueue import JobQueue

class Node():

    def __init__(self):
        self.JobManager = JobManager()
        self.JobQueue   = JobQueue()

    def check_for_jobs(self):
        #checks the JobQueue object for new jobs
        if self.JobQueue.jobs_available():
            job_info = self.JobQueue.get_job()
            self.JobManager.add_job(job_info)

    def get_finished_jobs(self):
        #get finished jobs from JobManager
        finished = self.JobManager.get_finished_jobs()
        for job in finished:
            if job['status'] == 'OK':
                self.good_job(job)
            else:
                self.bad_job(job)

    def good_job(self, job):
        #if those processes finished ok, send back the info
        print job

    def bad_job(self, job):
        #if those processes didn' finished ok, alert the Master
        print job


