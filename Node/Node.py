#!/usr/bin/env python

class Node():

    def __init__(self, master_coms, taskmanager):
        self.taskmanager = taskmanager
        self.master_coms = master_coms

    def free_task_slots(self):
        return self.taskmanager.free_space()

    def check_for_tasks(self):
        #checks the taskqueue object for new tasks
        if self.master_coms.tasks_available():
            task_info = self.master_coms.get_task()
            self.add_task(task_info)

    def add_task(self, task_info):
        self.taskmanager.new_task(task_info)

    def get_finished_tasks(self):
        #get finished tasks from taskmanager
        finished = self.taskmanager.get_finished_items()
        for task in finished:
            if task['status'] == 'OK':
                self.good_task(task)
            else:
                self.bad_task(task)

    def good_task(self, task):
        #if those processes finished ok, send back the info
        print "Good task"
        print task

    def bad_task(self, task):
        #if those processes didn' finished ok, alert the Master
        print "Bad Task"
        print task

    def heartbeat(self):
        #sends message back to Master to say Node is still alive
        print 'heartbeat'


