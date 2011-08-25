
from libs.PovTask import PovTask

class PovJob():

    task_list = {}
    finished  = 0
    completed = False

    def __init__(self, job_info):
        self.job_id   = job_info['job_id']
        self.job_name = job_info['job_name']
        self.tasks    = job_info['tasks']

        pov_data      = job_info['job_data']
        self.pov_file = pov_data['pov_file']
        self.output   = pov_data['output_file']
        self.width    = pov_data['width']
        self.height   = pov_data['height']
        self.extras   = pov_data['extras']

    def create_tasks(self):
        slice_width = self.width / self.tasks
        leftover    = self.width % self.tasks
        for i in range(self.tasks):
            task_num = i + 1
            start    = (i * slice_width) + 1
            end      = (i + 1) * slice_width
            if task_num == self.tasks:
                end += leftover
            self.task_list[i]          = PovTask()
            self.task_list[i].job_id   = self.job_id
            self.task_list[i].task_id  = i

            self.task_list[i].job_data = {}
            self.task_list[i].job_data['pov_file']  = self.pov_file
            self.task_list[i].job_data['file_name'] = "%s-%s-%s" % (self.output, start, end)
            self.task_list[i].job_data['width']     = self.width
            self.task_list[i].job_data['height']    = self.height
            self.task_list[i].job_data['start']     = start
            self.task_list[i].job_data['end']       = end

    def get_tasks(self):
        return self.task_list.values()

    def finished_task(self, task):
        task_id = task.task_id
        self.task_list[task_id].final_data = task.final_data
        self.finished += 1
        if self.finished == self.tasks:
            self.completed = True

    def final_output(self):
        output = ''
        for ids, task in self.task_list.iteritems():
            output += task.final_data['file']
        return output


