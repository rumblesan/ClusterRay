#!/usr/bin/env python

from RayManager import RayManager
from time import sleep
import sys
import json
import random


def get_job():
    data = {}
    data['inputfile']  = 'fractal2.pov'
    data['outputfile'] = str(random.randint(0,1000)) + 'output.png'
    data['width']      = '500'
    data['height']     = str(400 + random.randint(0, 400))
    data['start']      = '1'
    data['end']        = '500'
    data['extras']     = ["+FN"]
    return data

def main():

    count = 0
    print "create process manager object"
    manager = RayManager(2)
    while 1:
        if manager.free_task_slots() and count < 5:
            new_job = get_job()
            manager.new_process(new_job)
            count += 1
            print count
        finished_jobs = manager.get_finished_tasks()
        for id_num, job in finished_jobs.iteritems():
            print (id_num, job.return_value)
        active_tasks = manager.active_tasks
        print active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


