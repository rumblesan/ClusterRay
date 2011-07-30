
from Povray import Povray
from Manager import Manager

class RayManager(Manager):

    debug        = False

    def __init__(self, max_rays=1, debug=False):
        self.debug = debug
        Manager.__init__(self, max_rays)

    def new_process(self, job_info):
        job_info['outputfile'] = str(job_info['job_id'])
        new_process = Povray(job_info)
        new_process.create_args()
        new_process.run()
        ray_number = self.add_task(new_process)
        return ray_number

    def finished(self, process):
        process.poll()
        return process.completed


