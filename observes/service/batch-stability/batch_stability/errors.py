class BatchSucceededJob(Exception):
    pass


class BatchFailedJob(Exception):
    pass


class BatchCancelledJob(Exception):
    pass


class BatchUnstartedJob(Exception):
    pass
