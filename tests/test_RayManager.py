#!/usr/bin/env python

from Node.RayManager import RayManager
from time import sleep
import sys
import json
import random


def get_task():
    data = {}
    data['inputfile']  = 'misc/fractal2.pov'
    data['id']         = str(random.randint(0,1000)) + 'output'
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
            new_task = get_task()
            manager.new_task(new_task)
            count += 1
            print count
        finished_tasks = manager.get_finished_tasks()
        for task in finished_tasks:
            print task
        active_tasks = manager.active_tasks
        print active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


