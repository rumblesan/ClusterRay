#!/usr/bin/env python

import zmq

class MasterComs():

    zmq_context     = None
    zmq_socket      = None
    message_actions = {}

    def __init__(self, host, port):
        context = zmq.Context()
        self.zmq_socket  = context.socket(zmq.REP)
        address = 'tcp://%s:%s' % (host, port)
        self.zmq_socket.bind(address)

    def register_action(self, name, function):
        #this is where we register our callbacks
        #when a message is received we call the right function
        self.message_actions[name] = function

    def run_action(self, message):
        #this is used to run the action
        if message.action not in self.message_actions.keys():
            return "Action not registered"
        else:
            return self.message_actions[message.action](message)

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


