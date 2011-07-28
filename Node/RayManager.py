
from Povray import Povray
from Manager import Manager

class RayManager(Manager):

    debug        = False

    def __init__(self, max_rays=1, debug=False):
        self.debug = debug
        Manager.__init__(self, max_rays)

    def new_process(self, config_json):
        new_process = Povray(config_json, self.process_num)
        new_process.create_args()
        new_process.run()
        self.process_list.append(new_process)
        ray_number = self.add_task(new_process)
        return ray_number

    def finished(self, process):
        process.poll()
        return process.completed


