# Third party libraries
import confuse

# Local libraries
from utils.aio import (
    unblock_cpu,
)
from utils.model import (
    LanguagesEnum,
    SkimsConfig,
    SkimsPathConfig,
)
from utils.logs import (
    log,
)


def _load(path: str) -> SkimsConfig:
    template = confuse.Configuration('skims', read=False)
    template.set_file(path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template({
            'group': confuse.String(pattern=r'^[a-z0-9]+$'),
            'language': confuse.Choice(LanguagesEnum),
            'path': confuse.Template({
                'exclude': confuse.Sequence(confuse.Filename(cwd='')),
                'include': confuse.Sequence(confuse.Filename(cwd='')),
            }),
        },
        ),
    )

    return SkimsConfig(
        group=config['group'],
        language=config['language'],
        path=SkimsPathConfig(
            exclude=config['path']['exclude'],
            include=config['path']['include'],
        ) if 'path' in config else None,
    )


async def load(path: str) -> SkimsConfig:
    skims_config: SkimsConfig = await unblock_cpu(_load, path)

    await log('debug', '%s', skims_config)

    return skims_config
