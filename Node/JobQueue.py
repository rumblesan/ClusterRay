

class JobQueue():

    jobs = []

    def __init__():
        pass

    def jobs_available(self):
        if len(self.jobs) == 0:
            return False
        else:
            return True

    def get_job(self):
        if not len(self.jobs) == 0:
            return self.jobs.pop(0)

    def job_completed(job_info):
        pass

    def job_errored(job_info):
        pass
