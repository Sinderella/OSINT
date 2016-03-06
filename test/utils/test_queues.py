from osint.utils.queues import WorkerQueue


class TestWorkerQueue(object):
    def __init__(self):
        self.wq = None

    def setup(self):
        self.wq = WorkerQueue()
        assert self.wq.get_total() == 0
        assert self.wq.get_done() == 0

    def teardown(self):
        del self.wq

    def test_get_total(self):
        self.wq.put('test')
        assert self.wq.get_total() == 1

    def test_get_done(self):
        self.test_get_total()
        self.wq.task_done()
        assert self.wq.get_done() == 1

    def test_reset_count(self):
        self.test_get_done()
        self.wq.reset_count()
        assert self.wq.get_total() == 0
        assert self.wq.get_done() == 0
