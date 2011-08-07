#!/usr/bin/env python

class Master():

    def __init__(self, node_coms, client_coms, node_manager, job_manager):
        self.job_manager  = job_manager
        self.node_coms    = node_coms
        self.node_manager = node_manager
        self.client_coms  = client_coms

        self.message_actions()

    def message_actions(self):
        #this function deals with the request actions
        #message action are:-
        #    HANDSHAKE
        #    NEWTASK
        #    HEARTBEAT
        #    FINISHED
        actions = {}
        actions['NEWTASK'] = self.job_manager.get_job
        actions['FINISHED'] = self.job_manager.finished_job
        #actions['HEARTBEAT'] = 
        #actions['HANDSHAKE'] = 
        for name, function in actions.iteritems():
            self.node_coms.register_action(name, function)

    def check_for_jobs(self):
        #checks for incoming jobs that will be split into
        #tasks and distributed to the Nodes
        self.client_coms.get_jobs()

    def add_job(self, job_info):
        #add a new job to the job manager
        #job manager deals with splitting it up into tasks
        self.job_manager.add_job(job_info)

    def get_messages(self):
        #gets any messages sent by the Nodes
        self.node_coms.check()

    def check_nodes(self):
        #checks the node manager to make sure all Nodes
        #are still functioning
        self.node_coms.check()


