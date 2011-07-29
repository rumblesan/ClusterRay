
class Manager():

    running_tasks  = {}

    task_number    = 1
    active_tasks   = 0
    max_tasks      = 0

    def __init__(self, max_tasks):
        self.max_tasks = max_tasks

    def free_task_slots(self):
        if self.active_tasks == self.max_tasks:
            return False
        else:
            return True

    def add_task(self, new_task):
        if self.active_tasks == self.max_tasks:
            return False
        new_task_number = self._new_task_number()
        self.running_tasks[new_task_number] = new_task
        self.active_tasks += 1
        return new_task_number

    def _new_task_number(self):
        while 1:
            if self.running_tasks.has_key(self.task_number):
                self.task_number += 1
                if self.task_number > self.max_tasks:
                    self.task_number = 1
            else:
                break
        return self.task_number

    def get_finished_tasks(self):
        finished = {}
        running  = {}
        for task_num, task in self.running_tasks.iteritems():
            if self.finished(task):
                finished[task_num] = task
            else:
                running[task_num] = task
        self.running_tasks  = running
        self.active_tasks = len(running)
        return finished




