from fa_purity import (
    Cmd,
)
from utils_logger_2 import (
    set_main_log,
)
from utils_logger_2.env import (
    current_app_env,
    notifier_key,
    observes_debug,
)
from utils_logger_2.handlers import (
    BugsnagConf,
)


def set_logger(root_name: str, version: str) -> Cmd[None]:
    n_key = notifier_key()
    app_env = current_app_env()
    debug = observes_debug()
    conf = n_key.bind(
        lambda key: app_env.map(
            lambda env: BugsnagConf(
                "service",
                version,
                "./observes/service/success_indicators",
                False,
                key,
                env,
            )
        )
    )
    return debug.bind(
        lambda d: conf.bind(lambda c: set_main_log(root_name, c, d, False))
    )
