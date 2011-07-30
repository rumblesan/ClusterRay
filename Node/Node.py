#!/usr/bin/env python

from JobManager import JobManager
from JobQueue import JobQueue

class Node():

    def __init__(self):
        self.JobManager = JobManager(4)
        self.JobQueue   = JobQueue()

    def free_job_slots(self):
        return self.JobManager.free_job_slots()

    def check_for_jobs(self):
        #checks the JobQueue object for new jobs
        if self.JobQueue.jobs_available():
            job_info = self.JobQueue.get_job()
            self.add_job(job_info)

    def add_job(self, new_job):
        self.JobManager.add_job(new_job)

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

    def heartbeat(self):
        #sends message back to Master to say Node is still alive
        print 'heartbeat'

def main():
    node = Node()
    while 1:
        if node.free_job_slots():
            node.check_for_jobs()
        node.get_finished_jobs()
        node.heartbeat()
        sleep(5)

if __name__ == '__main__':
    main()
