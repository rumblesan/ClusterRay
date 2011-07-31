

class TaskQueue():

    tasks = []
    next_task = None

    def __init__(self):
        pass

    def tasks_available(self):
        if len(self.tasks) == 0:
            return False
        else:
            return True

    def get_task(self):
        if not len(self.tasks) == 0:
            return self.tasks.pop(0)

    def task_completed(self, task_info):
        pass

    def task_errored(self, task_info):
        pass

    def send_heartbeat(self):
        pass

