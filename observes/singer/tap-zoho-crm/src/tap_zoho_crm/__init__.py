import utils_logger

utils_logger.configure(
    app_type="tap",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)
