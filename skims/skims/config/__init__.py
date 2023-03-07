import confuse
from ctx import (
    STATE_FOLDER,
)
from model import (
    core_model,
)
import os
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)
import yaml


def load_checks(config: Any) -> set[core_model.FindingEnum]:
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


def load(group: str | None, path: str) -> core_model.SkimsConfig:
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
                "commit": confuse.String(),
                "dast": confuse.Template(
                    {
                        "aws_credentials": confuse.Sequence(
                            confuse.Template(
                                {
                                    "access_key_id": confuse.String(),
                                    "secret_access_key": confuse.String(),
                                }
                            )
                        ),
                        "http": confuse.Template(
                            {
                                "include": confuse.Sequence(confuse.String()),
                            }
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
                        "urls": confuse.Sequence(confuse.String()),
                        "ssl_checks": confuse.OneOf([True, False]),
                        "http_checks": confuse.OneOf([True, False]),
                    }
                ),
                "language": confuse.Choice(core_model.LocalesEnum),
                "namespace": confuse.String(),
                "output": confuse.Template(
                    {
                        "file_path": confuse.String(),
                        "format": confuse.OneOf(
                            [
                                _format.value
                                for _format in core_model.OutputFormat
                            ]
                        ),
                    }
                ),
                "execution_id": confuse.String(),
                "path": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                        "lib_path": confuse.OneOf([True, False]),
                        "lib_root": confuse.OneOf([True, False]),
                    },
                ),
                "working_dir": confuse.String(),
            }
        ),
    )

    try:
        config_apk = config.pop("apk", {})
        config_path = config.pop("path", {})
        config_dast = config.pop("dast", {}) or {}
        output = config.pop("output", None)

        skims_config = core_model.SkimsConfig(
            apk=core_model.SkimsAPKConfig(
                exclude=config_apk.pop("exclude", ()),
                include=config_apk.pop("include", ()),
            ),
            checks=load_checks(config),
            commit=config.pop("commit", None),
            dast=core_model.SkimsDastConfig(
                aws_credentials=[
                    core_model.AwsCredentials(
                        access_key_id=cred["access_key_id"],
                        secret_access_key=cred["secret_access_key"],
                    )
                    for cred in config_dast.get("aws_credentials", [])
                ],
                http=core_model.SkimsHttpConfig(
                    include=config_dast.pop("http", {}).pop("include", ()),
                ),
                ssl=core_model.SkimsSslConfig(
                    include=tuple(
                        core_model.SkimsSslTarget(
                            host=entry.pop("host"),
                            port=entry.pop("port", 443),
                        )
                        for entry in config_dast.pop("ssl", {}).pop(
                            "include", ()
                        )
                    )
                ),
                urls=tuple(url for url in config_dast.get("urls", ())),
                http_checks=config_dast.get("http_checks", False),
                ssl_checks=config_dast.get("ssl_checks", False),
            ),
            group=group,
            language=core_model.LocalesEnum(config.pop("language", "EN")),
            namespace=config.pop("namespace"),
            output=core_model.SkimsOutputConfig(
                file_path=os.path.abspath(output["file_path"]),
                format=core_model.OutputFormat(output["format"]),
            )
            if output
            else None,
            path=core_model.SkimsPathConfig(
                exclude=config_path.pop("exclude", ()),
                include=config_path.pop("include", ()),
                lib_path=config_path.pop("lib_path", True),
                lib_root=config_path.pop("lib_root", True),
            ),
            start_dir=os.getcwd(),
            working_dir=str(
                os.path.abspath(config.pop("working_dir", "."))
            ).replace("/home/makes/.skims", STATE_FOLDER),
            execution_id=config.pop("execution_id", None),
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


def dump_to_yaml(config: core_model.SkimsConfig) -> str:
    return yaml.dump(
        {
            "apk": {
                "exclude": list(config.apk.exclude),
                "include": list(config.apk.include),
            },
            "checks": [check.name for check in config.checks],
            "commit": config.commit,
            "dast": {
                "aws_credentials": [
                    {
                        "access_key_id": cred.access_key_id,
                        "secret_access_key": cred.secret_access_key,
                    }
                    for cred in config.dast.aws_credentials
                    if cred
                ],
                "http": {
                    "include": list(config.dast.http.include),
                },
                "ssl": {
                    "include": [
                        {
                            "host": ssl.host,
                            "port": ssl.port,
                        }
                        for ssl in config.dast.ssl.include
                    ],
                },
                "urls": list(config.dast.urls),
                "http_checks": config.dast.http_checks,
                "ssl_checks": config.dast.ssl_checks,
            }
            if config.dast
            else None,
            "language": config.language.value,
            "namespace": config.namespace,
            "output": {
                "file_path": config.output.file_path,
                "format": config.output.format.value,
            }
            if config.output
            else None,
            "execution_id": config.execution_id,
            "path": {
                "exclude": list(config.path.exclude),
                "include": list(config.path.include),
                "lib_path": config.path.lib_path,
                "lib_root": config.path.lib_root,
            },
            "working_dir": config.working_dir,
        }
    )
