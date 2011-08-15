
from libs.PovTask import PovTask

class PovJob():

    queued_tasks   = {}
    running_tasks  = {}
    finished_tasks = {}

    def __init__(self, job_id, job_info):
        self.job_id   = job_id

        self.pov_file = job_info['pov_file']
        self.output   = job_info['output_file']
        self.width    = int(job_info['width'])
        self.height   = int(job_info['height'])
        self.tasks    = int(job_info['tasks'])
        self.extras   = job_info['extras']

    def create_tasks(self):
        slice_width = self.width / self.tasks
        leftover    = self.width % self.tasks
        for i in range(self.tasks):
            task_num = i + 1
            start    = (i * slice_width) + 1
            end      = (i + 1) * slice_width
            if task_num == self.tasks:
                end += leftover
            self.queued_tasks[i]          = PovTask()
            self.queued_tasks[i].job_id   = self.job_id
            self.queued_tasks[i].task_id  = i
            self.queued_tasks[i].pov_file = self.pov_file
            self.queued_tasks[i].output   = "%s-%s-%s" % (self.output, start, end)
            self.queued_tasks[i].width    = self.width
            self.queued_tasks[i].height   = self.height
            self.queued_tasks[i].start    = start
            self.queued_tasks[i].end      = end

    def get_task(self):
        if len(self.queued_tasks) == 0:
            return False
        job_id, job = self.queued_tasks.popitem()
        self.running_tasks[job_id] = job
        return job

    def finished_task(self, task):
        if task.task_id not in self.running_tasks.keys():
            return False
        else:
            del(self.running_tasks[task.task_id])
            self.finished_tasks[task.task_id] = task

    def all_finished(self):
        if len(self.finished_tasks) == self.tasks:
            return True
        else:
            return False

    def get_output(self):
        output = []
        for key, task in self.finished_tasks.iteritems():
            output.append(task.get_output_file())
        return self._join_output(output)

    def _join_output(self, parts):
        #place holder for the moment
        output = " ".join(parts)
        return output
        

