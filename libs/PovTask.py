
class PovTask():

    job_id   = ''
    task_id  = ''
    pov_file = ''
    output   = ''
    width    = 0
    height   = 0
    start    = 0
    end      = 0
    finished = True

    def __str__(self):
        info = (self.job_id, self.task_id, self.width, self.height, self.start, self.end)
        return "%s-%s: %s,%s,  %s,%s" % (info)

    def store_pov_file(self):
        #pov file gets uploaded and stored somewhere
        #(amazon S3 for example)
        pass

    def get_pov_file(self):
        pass

    def store_output_file(self):
        pass

    def get_output_file(self):
        return self.output



