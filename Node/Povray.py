
from subprocess import Popen, PIPE
import os
import json
import shutil


class Povray():

    process      = None
    args         = []
    return_value = None
    completed    = False

    def __init__(self, config_json, node_number):

        config_info = json.loads(config_json)

        self.node_number = node_number
        self.workingdir  = "/var/PovNode/node" + str(self.node_number)

        self.command     = "povray"

        self.extras      = config_info['extras']

        self.inputfile   = config_info['inputfile']
        self.outputfile  = config_info['outputfile']

        self.width       = config_info['height']
        self.height      = config_info['width']

        self.start_col   = config_info['start']
        self.end_col     = config_info['end']

    def create_args(self):
        self.args.append(self.command)
        self.args.append("+I" + self.inputfile)
        self.args.append("+O" + self.outputfile)
        self.args.append("+W" + self.width)
        self.args.append("+H" + self.height)
        self.args.append("+SC" + self.start_col)
        self.args.append("+EC" + self.end_col)
        self.args.extend(self.extras)

    def setup(self):
        if os.path.exists(self.workingdir):
            shutil.rmtree(self.workingdir)
        os.makedirs(self.workingdir)
        shutil.copy(self.inputfile, os.path.join(self.workingdir, self.inputfile))
        os.chdir(self.workingdir)

    def cleanup(self):
        os.chdir('..')
        shutil.rmtree(self.workingdir)

    def run(self):
        self.process = Popen(self.args, stdin=None, stdout=PIPE, stderr=PIPE)

    def poll(self):
        value =  self.process.poll()
        if value == None:
            return False
        else:
            self.return_value = value
            self.completed = True
            return True

    def communicate(self):
        return self.process.communicate()

    def get_image(self):
        return os.path.join(self.workingdir, self.outputfile)

    def __del__(self):
        self.cleanup()


