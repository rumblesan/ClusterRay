#!/usr/bin/env python

import zmq

class MasterComs():

    zmq_context     = None
    zmq_socket      = None
    message_action  = None

    def __init__(self, host, port):
        context = zmq.Context()
        self.zmq_socket  = context.socket(zmq.REP)
        address = 'tcp://%s:%s' % (host, port)
        print address
        self.zmq_socket.bind(address)

    def register_action(self, action):
        #this is where we register our callback
        #when a message is received we call this function
        self.message_action = action

    def run_action(self, message):
        #this is used to run the action
        if self.message_action == None:
            return "Action not registered"
        else:
            return self.message_action(message)

    def check(self):
        while True:
            try:
                message = self.zmq_socket.recv_pyobj(zmq.NOBLOCK)
            except zmq.ZMQError:
                break

            #call the callback here
            reply = self.run_action(message)
            try:
                self.zmq_socket.send(reply, zmq.NOBLOCK)
            except zmq.ZMQError:
                print "Error sending reply"


