import utils_logger

utils_logger.configure(
    app_type="common",
    asynchronous=False,
    release_stage="development",
)
LOG = utils_logger.main_log(__name__, debug=True)
