
from Povray import Povray
from libs.Manager import Manager

class RayManager(Manager):

    def __init__(self, max_rays=1):
        Manager.__init__(self, max_rays)

    def new_task(self, task_info):
        task_info['outputfile'] = str(task_info['id'])
        new_process = Povray(task_info)
        new_process.create_args()
        new_process.run()
        ray_number = self.add_task(new_process)
        return ray_number

    def finished(self, process):
        process.poll()
        return process.completed


