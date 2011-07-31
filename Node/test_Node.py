#!/usr/bin/env python

from Node import Node
from TaskQueue import TaskQueue
from RayManager import RayManager
from time import sleep
import sys
import json
import random


def get_task():
    data = {}
    data['inputfile']  = 'fractal2.pov'
    data['id']         = str(random.randint(0,1000)) + 'output'
    data['width']      = '500'
    data['height']     = str(400 + random.randint(0, 400))
    data['start']      = '1'
    data['end']        = '500'
    data['extras']     = ["+FN"]
    return data

def main():
    taskmanager = RayManager(2)
    taskqueue   = TaskQueue()
    count = 0
    print "create task manager object"
    node = Node(taskqueue, taskmanager)
    while 1:
        if node.free_task_slots() and count < 5:
            new_task = get_task()
            node.add_task(new_task)
            count += 1
            print count
        node.get_finished_tasks()
        active_tasks = node.taskmanager.active_tasks
        print 'active_tasks', active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


