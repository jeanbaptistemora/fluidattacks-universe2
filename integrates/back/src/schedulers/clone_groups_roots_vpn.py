# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from schedulers.clone_groups_roots import (
    clone_groups_roots,
)


async def main() -> None:
    await clone_groups_roots(queue_with_vpn=True)
