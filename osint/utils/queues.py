from Queue import Queue


class WorkerQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        self.added = 0
        self.done = 0

    def get_total(self):
        return self.added

    def get_done(self):
        return self.done

    def reset_count(self):
        self.added = 0
        self.done = 0

    def put(self, item, block=True, timeout=None):
        self.added += 1
        return Queue.put(self, item, block, timeout)

    def task_done(self):
        self.done += 1
        return Queue.task_done(self)
