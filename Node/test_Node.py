#!/usr/bin/env python

from Node import Node
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
    node = Node()
    while 1:
        if node.free_job_slots() and count < 5:
            new_job = get_job()
            node.add_job(new_job)
            count += 1
            print count
        node.get_finished_jobs()
        active_tasks = node.JobManager.RayManager.active_tasks
        print 'active_tasks', active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


