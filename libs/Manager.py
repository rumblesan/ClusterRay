
class Manager():

    running_items  = {}

    item_number    = 1
    active_items   = 0
    max_items      = 0

    def __init__(self, max_items):
        self.max_items = max_items

    def free_space(self):
        if self.active_items == self.max_items:
            return False
        else:
            return True

    def add_item(self, new_item):
        if self.active_items == self.max_items:
            return False
        new_item_number = self._new_item_number()
        self.running_items[new_item_number] = new_item
        self.active_items += 1
        return new_item_number

    def _new_item_number(self):
        while 1:
            if self.running_items.has_key(self.item_number):
                self.item_number += 1
                if self.item_number > self.max_items:
                    self.item_number = 1
            else:
                break
        return self.item_number

    def get_finished_items(self):
        finished = []
        running  = {}
        for item_num, item in self.running_items.iteritems():
            if self.finished(item):
                finished.append(item.get_output_info())
            else:
                running[item_num] = item
        self.running_items  = running
        self.active_items = len(running)
        return finished




