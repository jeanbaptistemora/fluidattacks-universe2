from schedulers.clone_groups_roots import (
    clone_groups_roots,
)


async def main() -> None:
    await clone_groups_roots(queue_with_vpn=True)
