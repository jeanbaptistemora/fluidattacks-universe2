import utils_logger

utils_logger.configure(
    app_type="tap",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)
__version__ = "1.0.0"
