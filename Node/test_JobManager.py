#!/usr/bin/env python

from JobManager import JobManager
from time import sleep
import sys
import json
import random


def get_job():
    data = {}
    data['inputfile']  = 'fractal2.pov'
    data['job_id'] = str(random.randint(0,1000)) + 'output'
    data['width']      = '500'
    data['height']     = str(400 + random.randint(0, 400))
    data['start']      = '1'
    data['end']        = '500'
    data['extras']     = ["+FN"]
    return data

def main():

    count = 0
    print "create job manager object"
    manager = JobManager(2)
    while 1:
        if manager.free_job_slots() and count < 5:
            new_job = get_job()
            manager.add_job(new_job)
            count += 1
            print count
        finished_jobs = manager.get_finished_jobs()
        for job in finished_jobs:
            print (job['status'], job['job_file'])
        active_tasks = manager.RayManager.active_tasks
        print 'active_tasks', active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


