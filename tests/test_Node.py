#!/usr/bin/env python

from Node.Node import Node
from Node.ComsNode import NodeComs
from Node.RayManager import RayManager
from time import sleep
import sys
import json
import random


def get_task():
    data = {}
    data['inputfile']  = 'misc/fractal2.pov'
    data['id']         = str(random.randint(0,1000)) + 'output'
    data['width']      = '500'
    data['height']     = str(400 + random.randint(0, 400))
    data['start']      = '1'
    data['end']        = '500'
    data['extras']     = ["+FN"]
    return data

def main():
    taskmanager = RayManager(2)
    coms   = NodeComs('127.0.0.1', '8888')
    count = 0
    print "create task manager object"
    node = Node(coms, taskmanager)
    while 1:
        if node.free_task_slots() and count < 5:
            new_task = get_task()
            node.add_task(new_task)
            count += 1
            print count
        node.get_finished_tasks()
        active_tasks = node.taskmanager.active_items
        print 'active_tasks', active_tasks
        if count == 5 and active_tasks == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


