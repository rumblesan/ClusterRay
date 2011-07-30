
from RayManager import RayManager

class JobManager():

    debug          = False
    RayManager     = None

    def __init__(self, max_jobs=1, debug=False):
        self.debug = debug
        self.RayManager = RayManager(max_jobs, debug)

    def add_job(self, job_info):
        job_info['outputfile'] = str(job_info['job_id'])
        self.RayManager.new_process(job_info)

    def get_finished_jobs(self):
        finished_jobs = self.RayManager.get_finished_tasks()
        job_list = []
        for id_num, job in finished_jobs.iteritems():
            job_list.append(job_return)
        return job_list

    def free_job_slots(self):
        return self.RayManager.free_task_slots()

