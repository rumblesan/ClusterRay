#!/usr/bin/env python

from RayManager import RayManager
from time import sleep
import sys
import json


def main():
    data = {}
    data['inputfile']  = 'fractal2.pov'
    data['outputfile'] = 'output.png'
    data['width']      = '1920'
    data['height']     = '1920'
    data['start']      = '1'
    data['end']        = '1920'
    data['extras']     = ["+FN", "-GA", "-D", "-V"]

    config_json = json.dumps(data)

    print "create process manager object"
    manager = RayManager(True)
    manager.new_process(config_json)
    manager.new_process(config_json)
    manager.new_process(config_json)
    manager.new_process(config_json)
    while 1:
        manager.check_processes()
        manager.clear_processes()
        if manager.running == 0:
            sys.exit()
        sleep(1)



if __name__ == '__main__':
    main()


