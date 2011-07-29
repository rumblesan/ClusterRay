
from RayManager import RayManager
import os

class JobManager():

    debug          = False
    RayManager     = None
    job_info       = {}

    def __init__(self, max_jobs=1, debug=False):
        self.debug = debug
        self.RayManager = RayManager(max_jobs, debug)

    def add_job(self, job_info):
        job_info['outputfile'] = str(job_info['job_id'])
        job_number = self.RayManager.new_process(job_info)
        self.job_info[job_number] = job_info

    def get_finished_jobs(self):
        finished_jobs = self.RayManager.get_finished_tasks()
        print finished_jobs
        job_list = []
        if len(finished_jobs) > 0:
            for id_num, job in finished_jobs.iteritems():
                job_return = {}
                job_return['job_id']   = self.job_info[id_num]['job_id']
                if job.return_value == 0:
                    job_return['status'] = 'OK'
                    job_return['job_file'] = job.get_image()
                else:
                    file_name = job.get_image()
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    job_return['status'] = 'ERROR'
                job_list.append(job_return)
        return job_list



    def free_job_slots(self):
        return self.RayManager.free_task_slots()

