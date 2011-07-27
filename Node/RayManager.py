
from Povray import Povray
from Manager import Manager

class RayManager(Manager):

    debug        = False

    def __init__(self, max_rays=1, debug=False):
        self.debug = debug
        Manager.__init__(self, max_rays)

    def new_process(self, config_json):
        new_process = Povray(config_json, self.process_num)
        new_process.setup()
        new_process.create_args()
        new_process.run()
        self.process_list.append(new_process)
        self.add_task(new_process)

    def check_processes(self):
        for process in self.process_list:
            poll_value = process.poll()

    def clear_processes(self):
        self.process_list = [process for process in self.process_list if not process.completed]
        self.running -= len(finished)
        for process in finished:
            print "%i  %s" % (process.node_number, process.get_image())
        if self.debug:
            print "%i processes still running" % len(self.process_list)

    def finished(self, task):
        return task.completed


