
from Povray import Povray

class RayManager():

    process_list = []
    process_num  = 1
    debug        = False
    running      = 0

    def __init__(self, debug):
        self.debug = debug

    def new_process(self, config_json):
        new_process = Povray(config_json, self.process_num)
        new_process.setup()
        new_process.create_args()
        new_process.run()
        self.process_list.append(new_process)
        if self.debug:
            print "Process %i added" % self.process_num
        self.process_num += 1
        self.running += 1

    def check_processes(self):
        for process in self.process_list:
            poll_value = process.poll()
            if self.debug:
                print "Process %i poll is %s" % (process.node_number, poll_value)

    def clear_processes(self):
        finished = [process for process in self.process_list if process.completed]
        self.process_list = [process for process in self.process_list if not process.completed]
        self.running -= len(finished)
        if self.debug:
            print "%i processes finished" % len(finished)
        for process in finished:
            print "%i  %s" % (process.node_number, process.get_image())
        if self.debug:
            print "%i processes still running" % len(self.process_list)


