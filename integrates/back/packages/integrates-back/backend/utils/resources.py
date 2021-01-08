from backend import util


def clean_cache(project_name: str) -> None:
    util.queue_cache_invalidation(
        # resource entity related
        f'environments*{project_name}',
        f'files*{project_name}',
        # project entity related
        f'has*{project_name}',
        f'deletion*{project_name}',
        f'tags*{project_name}',
    )
