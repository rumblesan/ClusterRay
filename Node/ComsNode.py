#!/usr/bin/env python

import zmq

class NodeComs():

    zmq_context = None
    zmq_socket  = None

    def __init__(self, host, port):
        self.zmq_context = zmq.Context()
        self.zmq_socket  = self.zmq_context.socket(zmq.REQ)
        address = 'tcp://%s:%s' % (host, port)
        print address
        self.zmq_socket.connect(address)

    def send(self, message):
        try:
            self.zmq_socket.send_pyobj(message)
        except zmq.ZMQError:
            print "Error sending request"
            return

        try:
            reply = self.zmq_socket.recv()
        except zmq.ZMQError:
            return
        return reply



