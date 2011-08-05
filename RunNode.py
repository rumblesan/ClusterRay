#!/usr/bin/env python

from RayManager import RayManager
from TaskQueue import TaskQueue
from Node import Node

def main():
    taskmanager = RayManager()
    taskqueue   = TaskQueue()
    node        = Node(taskqueue, taskmanager)
    while 1:
        if node.free_task_slots():
            node.check_for_tasks()
        node.get_finished_tasks()
        node.heartbeat()
        sleep(5)

if __name__ == '__main__':
    main()
