
from subprocess import Popen, PIPE
import os
import shutil


class Povray():

    process      = None
    defaults     = ["-GA", "-D", "-V"]
    args         = []
    return_value = None
    completed    = False

    def __init__(self, ray_info):

        self.command     = "povray"

        self.extras      = ray_info['extras']

        self.inputfile   = ray_info['inputfile']
        self.outputfile  = ray_info['outputfile']

        self.width       = ray_info['height']
        self.height      = ray_info['width']

        self.start_col   = ray_info['start']
        self.end_col     = ray_info['end']

    def create_args(self):
        self.args.append(self.command)
        self.args.append("+I" + self.inputfile)
        self.args.append("+O" + self.outputfile)
        self.args.append("+W" + self.width)
        self.args.append("+H" + self.height)
        self.args.append("+SC" + self.start_col)
        self.args.append("+EC" + self.end_col)
        self.args.extend(self.extras)
        self.args.extend(self.defaults)

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
        return self.outputfile


