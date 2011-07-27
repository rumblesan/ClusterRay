
from RayManager import RayManager
from Manager import Manager

class JobManager(Manager):

    debug        = False

    def __init__(self, max_jobs=1, debug=False):
        self.debug = debug
        Manager.__init__(self, max_jobs)

    def add_job(self, job_info):
        pass

    def check_jobs(self):
        pass

