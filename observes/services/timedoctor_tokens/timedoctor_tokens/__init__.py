# Local libraries
import utils_logger

utils_logger.configure(
    app_type="service",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)
