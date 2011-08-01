#!/usr/bin/env python

class Master():

    def __init__(self, node_coms, jobmanager):
        self.jobmanager = jobmanager
        self.node_coms  = node_coms

    def check_for_jobs(self):
        #checks for incoming jobs that will be split into
        #tasks and distributed to the Nodes
        pass

    def add_job(self, task_info):
        #add a new job to the job manager
        #job manager deals with splitting it up into tasks
        pass

    def get_finished_tasks(self):
        #get finished tasks from the Nodes
        #give them to the job manager
        pass

    def get_finished_jobs(self):
        #check the job manager for finished jobs
        #a job will be finished once the job manager has
        #all the tasks assigned to it
        pass

    def check_nodes(self):
        #check that the nodes have sent heartbeat messages
        #if any haven't for too long then kill that Node
        #then send its jobs out to other Nodes
        pass


