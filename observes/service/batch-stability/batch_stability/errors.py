class BatchSucceededJob(Exception):
    pass


class BatchFailedJob(Exception):
    pass


class BatchUnknownExitCode(Exception):
    pass


class BatchCancelledJob(Exception):
    pass


class BatchUnstartedJob(Exception):
    pass
