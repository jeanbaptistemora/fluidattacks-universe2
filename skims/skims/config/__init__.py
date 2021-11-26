import confuse
from model import (
    core_model,
)
import os
from typing import (
    Any,
    Optional,
    Set,
)
from utils.logs import (
    log_blocking,
)


def load_checks(config: Any) -> Set[core_model.FindingEnum]:
    # All checks by default, or the selected by the checks field
    return (
        {
            core_model.FindingEnum[finding]
            for finding in config.pop("checks")
            if finding in core_model.FindingEnum.__members__
        }
        if "checks" in config
        else set(core_model.FindingEnum)
    )


def load(group: Optional[str], path: str) -> core_model.SkimsConfig:
    template = confuse.Configuration("skims", read=False)
    template.set_file(path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template(
            {
                "apk": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                    },
                ),
                "checks": confuse.Sequence(confuse.String()),
                "http": confuse.Template(
                    {
                        "include": confuse.Sequence(confuse.String()),
                    }
                ),
                "language": confuse.Choice(core_model.LocalesEnum),
                "namespace": confuse.String(),
                "output": confuse.String(),
                "path": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                        "lib_path": confuse.OneOf([True, False]),
                        "lib_root": confuse.OneOf([True, False]),
                    },
                ),
                "ssl": confuse.Template(
                    {
                        "include": confuse.Sequence(
                            {
                                "host": confuse.String(),
                                "port": confuse.Integer(),
                            }
                        ),
                    }
                ),
                "working_dir": confuse.String(),
            }
        ),
    )

    try:
        config_apk = config.pop("apk", {})
        config_http = config.pop("http", {})
        config_path = config.pop("path", {})
        config_ssl = config.pop("ssl", {})

        if output := config.pop("output", None):
            output = os.path.abspath(output)

        skims_config = core_model.SkimsConfig(
            apk=core_model.SkimsAPKConfig(
                exclude=config_apk.pop("exclude", ()),
                include=config_apk.pop("include", ()),
            ),
            checks=load_checks(config),
            group=group,
            http=core_model.SkimsHttpConfig(
                include=config_http.pop("include", ()),
            ),
            language=core_model.LocalesEnum(config.pop("language", "EN")),
            namespace=config.pop("namespace"),
            output=output,
            path=core_model.SkimsPathConfig(
                exclude=config_path.pop("exclude", ()),
                include=config_path.pop("include", ()),
                lib_path=config_path.pop("lib_path", True),
                lib_root=config_path.pop("lib_root", True),
            ),
            ssl=core_model.SkimsSslConfig(
                include=tuple(
                    core_model.SkimsSslTarget(
                        host=entry.pop("host"),
                        port=entry.pop("port", 443),
                    )
                    for entry in config_ssl.pop("include", ())
                )
            ),
            start_dir=os.getcwd(),
            working_dir=os.path.abspath(config.pop("working_dir", ".")),
        )
    except KeyError as exc:
        raise confuse.ConfigError(f"Key: {exc.args[0]} is required")
    else:
        if config:
            unrecognized_keys: str = ", ".join(config)
            raise confuse.ConfigError(
                f"Some keys were not recognized: {unrecognized_keys}",
            )

    log_blocking("debug", "%s", skims_config)

    return skims_config
