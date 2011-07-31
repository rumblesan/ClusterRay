

class JobQueue():

    jobs = []
    next_job = None

    def __init__(self):
        pass

    def jobs_available(self):
        if len(self.jobs) == 0:
            return False
        else:
            return True

    def get_job(self):
        if not len(self.jobs) == 0:
            return self.jobs.pop(0)

    def job_completed(self, job_info):
        pass

    def job_errored(self, job_info):
        pass

    def send_heartbeat(self):
        pass

